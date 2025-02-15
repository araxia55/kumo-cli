import typer
from datetime import datetime, timezone
from typing import List

import boto3
import botocore.exceptions
from cachetools import cached, TTLCache
from utils import print_table, get_username

cache = TTLCache(maxsize=100, ttl=300)  # Cache up to 100 items for 300 seconds

app = typer.Typer()
default_region = 'us-east-1'
ec2 = boto3.client('ec2', region_name=default_region)

@cached(cache)
@app.command()
def list_instance(region: str = typer.Option("us-east-1", help="AWS region to list the instances in")):
    """List all EC2 instances with user who launched them and other details"""
    response = ec2.describe_instances()
    headers = ["Instance ID", "Name", "Launched By", "State", "Running Time", "Public IP", "Private IP", "Region"]
    rows = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            public_ip = instance.get('PublicIpAddress', '—')
            private_ip = instance.get('PrivateIpAddress', '—')

            # Retrieve instance tags
            tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}

            # Get the instance name
            name = tags.get('Name', 'Unnamed')

            # Get the username of who launched the instance
            launched_by = tags.get('LaunchedBy', 'Unknown')

            # Calculate running time
            if 'LaunchTime' in instance and state == 'running':
                launch_time = instance['LaunchTime']
                now = datetime.now(timezone.utc)
                running_time = now - launch_time
                days = running_time.days
                hours, remainder = divmod(running_time.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                running_time_str = f"{days}d {hours}h {minutes}m"
            else:
                running_time_str = '—'

            # Add row to the table
            rows.append([instance_id, name, launched_by, state, running_time_str, public_ip, private_ip, region])

    # Print the table
    print_table(headers, rows, title="EC2 Instance(s)")

@app.command()
def start_instance(instance_id: str):
    """Start an EC2 instance"""
    # Get the username of the AWS user who started the instance(s)
    username = get_username()

    response = ec2.start_instances(InstanceIds=[instance_id])
    instance_info = response['StartingInstances'][0]

    # Extract details of the started instance
    instance_id = instance_info['InstanceId']
    previous_state = instance_info['PreviousState']['Name']
    current_state = instance_info['CurrentState']['Name']

    # Prepare data for the table
    headers = ["Instance ID", "Previous State", "Current State", "Started By"]
    rows = [[instance_id, previous_state, current_state, username]]

    # Print the table
    print_table(headers, rows, title="Started EC2 Instance(s)")

@app.command()
def stop_instance(instance_id: str):
    """Stop an EC2 instance"""
    # Get the username of the AWS user who stopped the instance(s)
    username = get_username()
    
    response = ec2.stop_instances(InstanceIds=[instance_id])
    instance_info = response['StoppingInstances'][0]

    # Extract details of the stopped instance
    instance_id = instance_info['InstanceId']
    previous_state = instance_info['PreviousState']['Name']
    current_state = instance_info['CurrentState']['Name']

    # Prepare data for the table
    headers = ["Instance ID", "Previous State", "Current State", "Stopped By"]
    rows = [[instance_id, previous_state, current_state, username]]

    # Print the table
    print_table(headers, rows, title="Stopped EC2 Instance(s)")

@app.command()
def terminate_instance(
    instance_ids: List[str] = typer.Argument(..., help="One or more Instance IDs to terminate"),
    force: bool = typer.Option(False, "--force", "-f", help="Force termination without confirmation"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate termination without making changes")
):
    headers = ["Instance ID", "Previous State", "Current State", "Terminated By"]
    rows = []

    """
    Terminate one or more EC2 instances
    """
    # Get the username of the AWS user who terminated the instance(s)
    username = get_username()
    
    if dry_run:
        typer.echo("Dry run enabled. The following instances would be terminated:")
        for instance_id in instance_ids:
            print(f"- {instance_id}")
        raise typer.Exit()
    
    if not force:
        instance_list = ', '.join(instance_ids)
        confirm = typer.confirm(f"Are you sure you want to terminate the following instances: {instance_list}?")
        if not confirm:
            typer.echo("Termination cancelled.")
            raise typer.Abort()

    try:
        response = ec2.terminate_instances(InstanceIds=instance_ids)
        terminated_instances = response.get('TerminatingInstances', [])
        for instance in terminated_instances:
            instance_id = instance['InstanceId']
            previous_state = instance['PreviousState']['Name']
            current_state = instance['CurrentState']['Name']
            rows.append([instance_id, previous_state, current_state, username])
        print_table(headers, rows, title="Terminated EC2 Instance(s)")
    except botocore.exceptions.ClientError as e:
        print(f"[bold red]An error occurred:[/bold red] {e}")
        raise typer.Exit(code=1)

@app.command()
def launch_instance(
    ami_id: str = "ami-085ad6ae776d8f09c",  # Default AMI ID
    instance_type: str = "t2.micro",        # Default instance type
    key_name: str = "my-key-pair",          # Default key pair name
    security_group: str = "default",        # Default security group
    instance_name: str = typer.Option("MyEC2Instance", help="Name of the EC2 instance"),
    region: str = typer.Option("us-east-1", help="AWS region to launch the instance in")
):
    """Launch a new EC2 instance with additional parameters and default values"""
    header = ["Instance ID", "Name", "Launched By", "Public IP", "Region"]
    rows = []
    # Get the username of the AWS user who launched the instance(s)
    username = get_username()

    response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        KeyName=key_name,
        SecurityGroups=[security_group],
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': instance_name},
                    {'Key': 'LaunchedBy', 'Value': username}
                ]
            }
        ]
    )
    
    instance_id = response['Instances'][0]['InstanceId']
    # Wait for instance to initialize
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])
    # Reload instance data
    reservations = ec2.describe_instances(InstanceIds=[instance_id]).get("Reservations")
    instance = reservations[0]['Instances'][0]
    public_ip = instance.get('PublicIpAddress')
    rows.append([instance_id, instance_name, username, public_ip, region])
    print_table(header, rows, title="Launched EC2 Instance(s)")

@cached(cache)
@app.command()
def list_amis(
    os_type: str = typer.Option(None, help="Filter AMIs by operating system (windows or linux)"),
    owner: str = typer.Option("self", help="Owner of the AMI (self, amazon, or aws-marketplace)")
):
    """List all available AMIs, with an optional OS filter"""
    response = ec2.describe_images(Owners=['amazon'])
    headers = ["Image ID", "Name", "Creation Date", "State", "OS", "Architecture"]
    rows = []

    for image in response['Images']:
        image_id = image['ImageId']
        name = image.get('Name', 'Unnamed')
        creation_date = image['CreationDate']
        state = image['State']
        architecture = image.get('Architecture', 'unknown')
        
        # Determine the operating system of the AMI
        platform_details = image.get('PlatformDetails', 'unknown')  # Default to unknown if not specified
        platform = image.get('Platform', 'unknown')  # Sometimes PlatformDetails may not be present

        print(f"Image ID: {image_id}, Name: {name}, Platform Details: {platform_details}, Platform: {platform}")  # Debugging output

        # Filter by operating system if os_type is provided
        if os_type and (os_type.lower() not in platform_details.lower() and os_type.lower() not in platform.lower()):
            continue

        # Add row to the table
        rows.append([image_id, name, creation_date, state, platform_details or platform, architecture])

        # Sort rows by Creation Date in descending order
        rows.sort(key=lambda x: x[2], reverse=True)

    if rows:
        # Print the table
        print_table(headers, rows, title="Available AMIs")
    else:
        print("No AMIs found matching the criteria.")

    
if __name__ == "__main__":
    app()

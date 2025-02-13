import typer
import boto3
from rich import print  # For better console output
from rich.table import Table 
from datetime import datetime, timezone
from typing import List
import botocore.exceptions

app = typer.Typer()

ec2 = boto3.client('ec2')

from rich.table import Table
from datetime import datetime, timezone

@app.command()
def list_instances():
    """List all EC2 instances with user who launched them and other details"""
    response = ec2.describe_instances()
    table = Table(title="EC2 Instances")

    table.add_column("Instance ID", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Launched By", style="green")
    table.add_column("State", style="green")
    table.add_column("Running Time", style="blue")
    table.add_column("Public IP", style="yellow")
    table.add_column("Private IP", style="yellow")

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

            table.add_row(instance_id, name, launched_by, state, running_time_str, public_ip, private_ip)

    print(table)

@app.command()
def start_instance(instance_id: str):
    """Start an EC2 instance"""
    response = ec2.start_instances(InstanceIds=[instance_id])
    print(response)

@app.command()
def stop_instance(instance_id: str):
    """Stop an EC2 instance"""
    response = ec2.stop_instances(InstanceIds=[instance_id])
    print(response)

@app.command()
def terminate_instances(
    instance_ids: List[str] = typer.Argument(..., help="One or more Instance IDs to terminate"),
    force: bool = typer.Option(False, "--force", "-f", help="Force termination without confirmation"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate termination without making changes")
):
    """
    Terminate one or more EC2 instances
    """
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
            print(f"[red]Instance {instance_id} changed from {previous_state} to {current_state}[/red]")
    except botocore.exceptions.ClientError as e:
        print(f"[bold red]An error occurred:[/bold red] {e}")
        raise typer.Exit(code=1)

@app.command()
def create_instance(ami_id: str, instance_type: str):
    """Create a new EC2 instance"""
    response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1
    )
    instance_id = response['Instances'][0]['InstanceId']
    print(f"Instance created with ID: {instance_id}")

@app.command()
def launch_instance(
    ami_id: str = "ami-085ad6ae776d8f09c",  # Default AMI ID
    instance_type: str = "t2.micro",        # Default instance type
    key_name: str = "my-key-pair",          # Default key pair name
    security_group: str = "default",        # Default security group
    instance_name: str = typer.Option("MyEC2Instance", help="Name of the EC2 instance")
):
    """Launch a new EC2 instance with additional parameters and default values"""
    import boto3

    # Get the username of the AWS user
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    arn = identity['Arn']
    # The ARN can be in the format arn:aws:iam::ACCOUNT-ID:user/username
    # We extract the username by splitting the ARN
    username = arn.split('/')[-1]

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
    print(f"Instance launched with ID: {instance_id}, Name: {instance_name}, Launched By: {username}")
    
    instance_id = response['Instances'][0]['InstanceId']
    # Wait for instance to initialize
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])
    # Reload instance data
    reservations = ec2.describe_instances(InstanceIds=[instance_id]).get("Reservations")
    instance = reservations[0]['Instances'][0]
    public_ip = instance.get('PublicIpAddress')
    print(f"Instance launched with ID: {instance_id}, Name: {instance_name}, Public IP: {public_ip}")

@app.command()
def list_amis(owner: str = typer.Argument("self"), os: str = typer.Option(None, help="Filter by operating system: windows or linux")):
    """List AMI IDs"""
    filters = []
    if os:
        if os.lower() == "windows":
            filters.append({"Name": "platform", "Values": ["windows"]})
        elif os.lower() == "linux":
            filters.append({"Name": "name", "Values": ["*-linux-*", "*-ubuntu-*", "*-centos-*"]})

    response = ec2.describe_images(Owners=[owner], Filters=filters)
    for image in response['Images']:
        print(f"AMI ID: {image['ImageId']}, Name: {image['Name']}, Description: {image.get('Description', 'No description')}, Platform: {image.get('Platform', 'linux')}")

if __name__ == "__main__":
    app()

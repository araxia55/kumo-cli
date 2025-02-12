import typer
import boto3
from rich import print  # For better console output

app = typer.Typer()

ec2 = boto3.client('ec2')

@app.command()
def list_instances():
    """List all EC2 instances"""
    response = ec2.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(f"Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}")

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
def terminate_instance(instance_id: str):
    """Terminate an EC2 instance"""
    response = ec2.terminate_instances(InstanceIds=[instance_id])
    print(response)

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
def launch_instance(ami_id: str, instance_type: str, key_name: str, security_group: str):
    """Launch a new EC2 instance with additional parameters"""
    response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        KeyName=key_name,
        SecurityGroups=[security_group],
        MinCount=1,
        MaxCount=1
    )
    instance_id = response['Instances'][0]['InstanceId']
    print(f"Instance launched with ID: {instance_id}")

if __name__ == "__main__":
    app()

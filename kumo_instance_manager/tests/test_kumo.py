import sys
import os
from unittest.mock import patch
import pytest
from datetime import datetime, timezone
from moto import mock_ec2

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import the list_instance function
from kumo_instance_manager.kumo import list_instance

@pytest.fixture
def mock_boto_client():
    with patch('kumo_instance_manager.kumo.boto3.client') as mock_boto_client:
        yield mock_boto_client

# Mocking AWS EC2 service
@mock_ec2
def test_list_instance_structure(mock_boto_client):
    # Set up mock EC2 client and create instances
    ec2 = boto3.client('ec2', region_name='us-east-1')
    ec2.run_instances(
        ImageId='ami-085ad6ae776d8f09c',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName='my-key-pair',
        SecurityGroups=['default'],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': 'TestInstance22'},
                    {'Key': 'LaunchedBy', 'Value': 'administrator-ganbatte'}
                ]
            }
        ]
    )

    # Call the function and get the result
    result = list_instance(region='us-east-1')

    # Perform structure assertions
    for instance in result:
        assert len(instance) == 8
        assert isinstance(instance[0], str)  # Instance ID
        assert isinstance(instance[1], str)  # Name
        assert isinstance(instance[2], str)  # Launched By
        assert isinstance(instance[3], str)  # State
        assert isinstance(instance[4], str)  # Running Time
        assert isinstance(instance[5], str)  # Public IP
        assert isinstance(instance[6], str)  # Private IP
        assert isinstance(instance[7], str)  # Region

    print(f"Actual Result: {result}")

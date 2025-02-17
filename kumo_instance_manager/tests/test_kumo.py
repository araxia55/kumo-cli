import sys
import os
from unittest.mock import patch
import pytest
from datetime import datetime, timezone

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import the list_instance function
from kumo_instance_manager.kumo import list_instance

# Mocking the boto3 client
@pytest.fixture
def mock_boto_client():
    with patch('kumo_instance_manager.kumo.boto3.client') as mock_boto_client:
        yield mock_boto_client

# Mocking AWS credentials
@pytest.fixture(autouse=True)
def mock_aws_creds(monkeypatch):
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'testing')
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'testing')
    monkeypatch.setenv('AWS_SECURITY_TOKEN', 'testing')
    monkeypatch.setenv('AWS_SESSION_TOKEN', 'testing')

# Test function for list_instance with structure assertions
def test_list_instance_structure(mock_boto_client):
    # Mock response from describe_instances
    mock_boto_client.return_value.describe_instances.return_value = {
        'Reservations': [
            {
                'Instances': [
                    {
                        'InstanceId': 'i-00a4bda1797cae8b4',
                        'State': {'Name': 'running'},
                        'PublicIpAddress': '54.159.202.155',
                        'PrivateIpAddress': '172.31.82.202',
                        'Tags': [
                            {'Key': 'Name', 'Value': 'TestInstance22'},
                            {'Key': 'LaunchedBy', 'Value': 'administrator-ganbatte'}
                        ],
                        'LaunchTime': datetime(2025, 1, 1, tzinfo=timezone.utc)
                    }
                ]
            }
        ]
    }

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

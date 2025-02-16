import sys
import os
from unittest.mock import patch
import pytest
from datetime import datetime, timezone

# Add the kumo_instance_manager directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../kumo_instance_manager')))

# Now you can import the list_instance function
from kumo import list_instance

# Mocking the boto3 client
@pytest.fixture
def mock_boto_client():
    with patch('kumo.boto3.client') as mock_boto_client:
        yield mock_boto_client

# Test function for list_instance
def test_list_instance(mock_boto_client):
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
                        'LaunchTime': datetime(2023, 1, 1, tzinfo=timezone.utc)
                    }
                ]
            }
        ]
    }

    # Expected result
    expected_result = [
        [
            'i-00a4bda1797cae8b4', 'TestInstance22', 'administrator-ganbatte', 'running', 
            '0d 0h 0m', '54.159.202.155', '172.31.82.202', 'us-east-1'
        ]
    ]

    # Call the function and print the result
    result = list_instance(region='us-east-1')
    print(f"Actual Result: {result}")
    print(f"Expected Result: {expected_result}")
    
    # Compare the result with the expected result
    assert result == expected_result

import boto3
from rich.table import Table 
from rich.console import Console

def print_table(headers, rows, title="Table"):
    """
    Prints a table to the console using the rich library.
    
    Args:
        headers (list): List of column headers.
        rows (list): List of rows, where each row is a list of cell values.
        title (str): Title of the table (optional).
    """
    console = Console()
    table = Table(title=title)

    # Add columns to the table
    for header in headers:
        table.add_column(header)

    # Add rows to the table
    for row in rows:
        # Convert all items in rows to strings
        row = [str(cell) for cell in row]
        table.add_row(*row)

    # Print the table to the console
    console.print(table)

def get_username():
    """Retrieve the username of the AWS user who invoked the function"""
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    arn = identity['Arn']
    # The ARN can be in the format arn:aws:iam::ACCOUNT-ID:user/username
    username = arn.split('/')[-1]
    return username

# Initialise default region
def initialize_boto3_client(service, region='us-east-1'):
    return boto3.client(service, region_name=region)
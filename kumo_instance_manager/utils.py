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
        table.add_row(*row)

    # Print the table to the console
    console.print(table)

# setup.py
from setuptools import setup, find_packages

setup(
    name='kumo-cli',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'boto3',
        'typer',
        'pytest',
        # Add other dependencies if needed
    ],
    entry_points={
        'console_scripts': [
            'kumo-cli=kumo_instance_manager.kumo:app',
        ],
    },
)

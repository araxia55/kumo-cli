from setuptools import setup, find_packages

setup(
    name='kumo_instance_manager',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'typer',
        'boto3',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'kumo-cli=kumo_instance_manager.kumo:app',
        ],
    },
)

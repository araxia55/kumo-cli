# KumoCLI

![Project Logo](./kumo_instance_manager/assets/kumo-penguin.png)

## Table of Contents
- [About the Project](#about-the-project)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Command Examples](#command-examples)
- [Contributing](#contributing)

## About
The **KumoCLI** Project is a versatile command-line interface tool designed to simplify and streamline interactions with Amazon Web Services (AWS) resources. Named after the Japanese word for "cloud," KumoCLI embodies the spirit of agility and efficiency in cloud management. This tool empowers users to manage their AWS infrastructure seamlessly, leveraging the power of Python, AWS SDK (Boto3) and leveraging the **Typer** module for an awesome CLI experience.

In a whimsical twist, the project's branding includes a logo featuring a brave penguin warrior slashing through clouds, symbolizing the efficiency and power of KumoCLI in mastering the cloud landscape.

With KumoCLI, cloud management becomes a breeze, allowing users to focus on innovation and growth without getting bogged down by operational complexities. Whether you're an AWS novice or a seasoned cloud architect, KumoCLI offers a user-friendly, powerful interface to manage your cloud resources effortlessly.

## Features
- **Instance Management:** Launch, Start, stop, and list EC2 instances with detailed information, including instance IDs, states, IP addresses, and more.

- **AMI Management:** List available AMIs, with optional filters for operating system (Linux or Windows), Image Location and detailed attributes like architecture and creation date.

- **User Identification:** Retrieve and display the username of the AWS user initiating the actions.

- **Caching:** Optimize performance with cached results to reduce redundant API calls.

- **Customizability:** Specify AWS regions for various operations, enabling flexibility and control over the cloud environment.

- **Rich Output:** Display data in well-organized tables using the rich library, enhancing readability and usability.

## Getting Started

## Directory Structure
```bash
kumo-cli/
├── README.MD
├── __init__.py
├── kumo_cli.egg-info/
├── kumo_instance_manager/
│   ├── __init__.py
│   ├── kumo.py
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_kumo.py
│   └── utils.py
├── requirements.txt
├── setup.py
└── venv/
```

## Prerequisites
1. Install and configure [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
2. Install Python 3.

```bash
sudo apt update && sudo apt upgrade
sudo apt install python3
```
  
3. Install Python Virtual Environment.

```bash
sudo apt install python3-venv
```

## Installation
Step-by-step instructions on how to get the project running locally.

1. Clone the repository

```bash
git clone https://github.com/araxia55/kumo-cli.git
cd kumo-cli
```

2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Install the package in editable mode.
```bash
pip install -e .
```

## Usage
To use the CLI tool, simply run:
```bash
$ kumo-cli  --help

╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                                                                                                                                                                       │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                                                                                                                                                                                │
│ --help                        Show this message and exit.                                                                                                                                                                                                                                                                     │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ list-instance        List all EC2 instances with user who launched them and other details                                                                                                                                                                                                                                     │
│ start-instance       Start an EC2 instance                                                                                                                                                                                                                                                                                    │
│ stop-instance        Stop an EC2 instance                                                                                                                                                                                                                                                                                     │
│ terminate-instance                                                                                                                                                                                                                                                                                                            │
│ launch-instance      Launch a new EC2 instance with additional parameters and default values                                                                                                                                                                                                                                  │
│ list-amis            List all available AMIs, with an optional OS filter                                                                                                                                                                                                                                                      │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

## Command Examples

```bash
# List available EC2 instance

$ kumo-cli list-instance

                                                      EC2 Instance(s)                                                           
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Instance ID         ┃ Name           ┃ Launched By            ┃ State   ┃ Running Time ┃ Public IP   ┃ Private IP    ┃ Region    ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ i-0c8d639446a4fb6c7 │ KumoInstance23 │ administrator-ganbatte │ running │ 0d 3h 4m     │ 34.230.45.6 │ 172.31.95.250 │ us-east-1 │
└─────────────────────┴────────────────┴────────────────────────┴─────────┴──────────────┴─────────────┴───────────────┴───────────┘

# Launch an EC2 instance

$ kumo-cli launch-instance --instance-name kumoInstance

                                 Launched EC2 Instance(s)                                 
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Instance ID         ┃ Name         ┃ Launched By            ┃ Public IP    ┃ Region    ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ i-0115fa7ba4ed9663a │ kumoInstance │ administrator-ganbatte │ 3.82.109.207 │ us-east-1 │
└─────────────────────┴──────────────┴────────────────────────┴──────────────┴───────────┘

# Stop EC2 instances

$ kumo-cli stop-instance i-0115fa7ba4ed9663a

                             Stopped EC2 Instance(s)                             
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Instance ID         ┃ Previous State ┃ Current State ┃ Stopped By             ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━┩
│ i-0115fa7ba4ed9663a │ running        │ stopping      │ administrator-ganbatte │
└─────────────────────┴────────────────┴───────────────┴────────────────────────┘

# List AMI Images 

$ kumo-cli list-amis --os-type windows --help
Initializing Kumo CLI package...

List all available AMIs, with an optional OS, Architecture, Image Region filter, etc.

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --os-type                    TEXT  Filter AMIs by operating system (windows or linux) [default: None]                                                                                                                                                                                    │
│ --owner                      TEXT  Owner of the AMI (self, amazon, or aws-marketplace) [default: self]                                                                                                                                                                                   │
│ --architecture               TEXT  Filter AMIs by architecture (i386|x86_64|arm64|x86_64_mac|arm64_mac) [default: None]                                                                                                                                                                  │
│ --source-image-region        TEXT  Filter AMIs by image region location [default: us-east-1]                                                                                                                                                                                             │
│ --help                             Show this message and exit.                                                                                                                                                                                                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

# Sample output:

$ kumo-cli list-amis --os-type windows --architecture x86_64

┏━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Image ID              ┃ Name                                                                                              ┃ Creation Date            ┃ State     ┃ OS                                 ┃ Architecture ┃ Image Region ┃
┡━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ ami-55555555555555555 │ Windows_Server-2022-English-Full-ECS_Optimized-2025.02.14                                         │ 2025-02-18T16:19:21.000Z │ available │ Windows                            │ x86_64       │ us-east-1    │
│ ami-44444444444444444 │ Windows_Server-2022-English-Core-ECS_Optimized-2025.02.14                                         │ 2025-02-18T16:19:20.000Z │ available │ Windows                            │ x86_64       │ us-east-1    │
│ ami-33333333333333333 │ Windows_Server-2019-English-Full-ECS_Optimized-2025.02.14                                         │ 2025-02-18T16:19:18.000Z │ available │ Windows                            │ x86_64       │ us-east-1    │
│ ami-22222222222222222 │ Windows_Server-2019-English-Core-ECS_Optimized-2025.02.14                                         │ 2025-02-18T16:19:17.000Z │ available │ Windows                            │ x86_64       │ us-east-1    │
│ ami-11111111111111111 │ Windows_Server-2016-English-Full-ECS_Optimized-2025.02.14                                         │ 2025-02-18T16:19:16.000Z │ available │ Windows                            │ x86_64       │ us-east-1    │
└───────────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────┴──────────────────────────┴───────────┴────────────────────────────────────┴──────────────┴──────────────┘
```
## Contributing
## Guidelines for contributing to the project.

1. fork the repository
2. Create a feature branch (git checkout -b feature/your-feature)
3. Commit your changes (git commit -m 'Add some feature')
4. Push to the branch (git push origin feature/your-feature)
5. Open a pull request

Project Link: https://github.com/araxia55/kumo-cli
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
- [License](#license)
- [Contact](#contact)

## About
The **KumoCLI** Project is a versatile command-line interface tool designed to simplify and streamline interactions with Amazon Web Services (AWS) resources. Named after the Japanese word for "cloud," KumoCLI embodies the spirit of agility and efficiency in cloud management. This tool empowers users to manage their AWS infrastructure seamlessly, leveraging the power of Python, AWS SDK (Boto3) and leveraging the **Typer** module for a great CLI experience.

In a whimsical twist, the project's branding includes a logo featuring a brave penguin warrior slashing through clouds, symbolizing the efficiency and power of KumoCLI in mastering the cloud landscape.

With KumoCLI, cloud management becomes a breeze, allowing users to focus on innovation and growth without getting bogged down by operational complexities. Whether you're an AWS novice or a seasoned cloud architect, KumoCLI offers a user-friendly, powerful interface to manage your cloud resources effortlessly.

## Features
- **Instance Management:** Start, stop, and list EC2 instances with detailed information, including instance IDs, states, IP addresses, and more.

- **AMI Management:** List available AMIs, with optional filters for operating system (Linux or Windows) and detailed attributes like architecture and creation date.

- **User Identification:** Retrieve and display the username of the AWS user initiating the actions.

- **Caching:** Optimize performance with cached results to reduce redundant API calls.

- **Customizability:** Specify AWS regions for various operations, enabling flexibility and control over the cloud environment.

- **Rich Output:** Display data in well-organized tables using the rich library, enhancing readability and usability.

## Getting Started

### Prerequisites

```bash
pip install boto3
pip install typer
pip install rich

Installation
Step-by-step instructions on how to get the project running locally.

1. Clone the repository

```bash
git clone https://github.com/your-username/project-name.git
```

2. Navigate to the project directory

```bash
cd project-name
```

3. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage
## Command Examples

```bash
# Start an EC2 instance
python3 kumo.py start-instance i-0abcd1234efgh5678

# Stop an EC2 instance
python3 kumo.py stop-instance i-0abcd1234efgh5678

# List EC2 instances
python3 kumo.py list-instances

                                                    EC2 Instances                                                      
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┓
┃ Instance ID         ┃ Name             ┃ Launched By            ┃ State   ┃ Running Time ┃ Public IP   ┃ Private IP   ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━┩
│ i-0bb4c80b66fb86e9e │ TestInstance     │ ********************** │ stopped │ —            │ —           │ 172.**.**.64 │
│ i-0ded7e3a9433c9231 │ KumoTestInstance │ ********************** │ running │ 0d 1h 27m    │ 54.211.9.47 │ 172.*.**.54  │
└─────────────────────┴──────────────────┴────────────────────────┴─────────┴──────────────┴─────────────┴──────────────┘
```

## Contributing
## Guidelines for contributing to the project.

1. fork the repository
2. Create a feature branch (git checkout -b feature/your-feature)
3. Commit your changes (git commit -m 'Add some feature')
4. Push to the branch (git push origin feature/your-feature)
5. Open a pull request

## License
Include a license for your project (e.g., MIT, GPL). Distributed under the MIT License. See LICENSE for more information.

## Contact
Your Name - your-email@example.com

Project Link: https://github.com/your-username/project-name
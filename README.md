# mfa-cscs-access


The repository contains a simple Python script [cscs-keygen.py] and a shell script [cscs-keygen.sh] which can be used as a command line tool for fetching public and private keys signed by CSCS'S CA after authenticating using MFA. You can then use those keys to ssh to CSCS'login nodes.

For using the python script, these are the steps:

```sh
git clone https://github.com/eth-cscs/sshservice-cli.git
cd sshservice-cli
pip install virtualenv # (if you don't already have virtualenv installed)
virtualenv venv # to create your new environment (called 'venv' here)
source venv/bin/activate # to enter the virtual environment
pip install -r requirements.txt # to install the requirements in the current environment
python cscs-keygen.py
```

For using the shell script, these are the steps:
```bash
git clone git@github.com:eth-cscs/sshservice-cli.git
cd sshservice-cli
bash cscs-keygen.sh
```

============================== **Announcement** =============================


Dear [sshservice] users,

As part of introducing our new resource and management platform, we are updating the tooling used for SSH access to CSCS systems.
This includes a revised centralized platform for account and SSH key management.

**What is changing**
- Updated workflows for generating, registering, and using SSH keys
- Improved support for automation and programmatic access via CLI and APIs
- A revised user interface with additional links to other interfaces

**Transition period**
- To ensure a smooth migration, the current sshservice.cscs.ch (and the corresponding command line tool https://github.com/eth-cscs/sshservice-cli) will **remain available until 2024-04-20**. During this period, both systems will operate in parallel, and we strongly encourage you to transition to the new setup as early as possible.

**Documentation**
- Instructions for the new SSH access setup are available here: https://docs.cscs.ch/access/ssh/. We recommend reviewing the documentation and updating your configuration at your earliest convenience. If you have any questions or encounter issues during the transition, please don’t hesitate to contact our support team.

Best regards,

CSCS IAM Team

# mfa-cscs-access


The repository contains a simple Python script [cscs-keygen.py] and a shell script [cscs-keygen.sh] which can be used as a command line tool for fetching public and private keys signed by CSCS'S CA after authenticating using MFA. You can then use those keys to ssh to CSCS'login nodes.

For using the python script, these are the steps:

```sh
git clone git@github.com:eth-cscs/sshservice-cli.git
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

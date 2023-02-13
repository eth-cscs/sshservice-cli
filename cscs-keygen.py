import getpass
import requests
import os
import sys
import time
import re
import json
from progress.bar import IncrementalBar

#Variables:
api_get_keys = 'https://sshservice.cscs.ch/api/v1/auth/ssh-keys/signed-key'

#Methods:
def get_user_credentials():
    user = input("Username: ")
    pwd = getpass.getpass()
    otp = getpass.getpass("Enter OTP (6-digit code):")
    if not (re.match('^\d{6}$', otp)):
       sys.exit("Error: OTP must be a 6-digit code.")
    return user, pwd, otp


def get_keys(username, password, otp):
    headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
    data = {
        "username": username,
        "password": password,
        "otp": otp
    }
    try:
        resp = requests.post(api_get_keys, data=json.dumps(data), headers=headers, verify=True)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        try:
            d_payload = e.response.json()
        except:
            raise SystemExit(e)
        if "payload" in d_payload and "message" in d_payload["payload"]:
            print("Error: "+d_payload["payload"]["message"])
        raise SystemExit(e)
    else:
        public_key = resp.json()['public']
        if not public_key:
            sys.exit("Error: Unable to fetch public key.")
        private_key = resp.json()['private']
        if not private_key:
            sys.exit("Error: Unable to fetch private key.")
        return public_key, private_key

def save_keys(public,private):
    if not public or not private:
        sys.exit("Error: invalid keys.")
    try:
        with open(os.path.expanduser("~")+'/.ssh/cscs-key-cert.pub', 'w') as file:
            file.write(public)
    except IOError as er:
        sys.exit('Error: writing public key failed.', er)
    try:
        with open(os.path.expanduser("~")+'/.ssh/cscs-key', 'w') as file:
            file.write(private)
    except IOError as er:
        sys.exit('Error: writing private key failed.', er)
    try:
        os.chmod(os.path.expanduser("~")+'/.ssh/cscs-key-cert.pub', 0o644)
    except Exception as ex:
        sys.exit('Error: cannot change permissions of the public key.', ex)
    try:
        os.chmod(os.path.expanduser("~")+'/.ssh/cscs-key', 0o600)
    except Exception as ex:
        sys.exit('Error: cannot change permissions of the private key.', ex)

def set_passphrase():
    user_input = input('Do you want to add a passphrase to your key? [y/n] (Default y) \n')

    yes_choices = ['yes', 'y']
    no_choices = ['no', 'n']

    if user_input.lower() in no_choices:
      passphrase = False
    else:
      passphrase = True
      cmd = 'ssh-keygen -f ~/.ssh/cscs-key -p'
      os.system(cmd)
    return passphrase


def main():
    user, pwd, otp = get_user_credentials()
    bar = IncrementalBar('Retrieving signed SSH keys:', max = 3)
    public, private = get_keys(user, pwd, otp)
    bar.next()
    time.sleep(1)
    bar.next()
    time.sleep(1)
    save_keys(public, private)
    bar.next()
    time.sleep(1)
    bar.finish()
    if (set_passphrase()):
        message = """

Usage:

1. Add the key to the SSH agent, using the passphrase you have set:
ssh-add -t 1d ~/.ssh/cscs-key

2. Connect to the login node using CSCS keys:
ssh -A <CSCS-LOGIN-NODE>

Note - if the key is not added to the SSH agent as mentioned in the step-1 above then use the command:
ssh -i ~/.ssh/cscs-key <CSCS-LOGIN-NODE>

    """
    else:
        message = """

Usage:

1. Add the key to the SSH agent:
ssh-add -t 1d ~/.ssh/cscs-key

2. Connect to the login node using CSCS keys:
ssh -A <CSCS-LOGIN-NODE>

Note - if the key is not added to the SSH agent as mentioned in the step-1 above then use the command:
ssh -i ~/.ssh/cscs-key <CSCS-LOGIN-NODE>

    """

    print(message)

if __name__ == "__main__":
    main()

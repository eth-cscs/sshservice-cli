import getpass
import requests
#only temporary
requests.packages.urllib3.disable_warnings()
import os
import sys
import time
import re
from progress.bar import IncrementalBar

token_endpoint = 'https://auth.cscs.ch/auth/realms/cscs/protocol/openid-connect/token'
client_id = 'sshservice'
client_secret = '12aa48d7-36af-41fa-804f-01c185c5cefc'
api_get_keys = 'https://sshservice.cscs.ch/api/v1/ssh-keys/signed-key'


def get_user_credentials():
    user = input("Username: ")
    pwd = getpass.getpass()
    otp = getpass.getpass("Enter OTP (6-digit code):")
    if not (re.match('^\d{6}$', otp)):
       sys.exit("Error: OTP must be a 6-digit code.")
    return user, pwd, otp

def get_access_token(username, password, otp):
    data = {
        'username': username,
        'password': password,
        'client_id': client_id,
        'grant_type': 'password',
        'client_secret': client_secret,
        'totp': otp
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/json'}
    try:
        resp = requests.post(token_endpoint, data=data, headers=headers)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        try:
            d_payload = e.response.json()
        except:
            raise SystemExit(e)
        if "error_description" in d_payload:
            print("Error: "+d_payload["error_description"])
        raise SystemExit(e)
    else:
        acc_tok =  resp.json()['access_token']
        if not acc_tok:
            sys.exit("Error: Unable to fetch access token.")
        else:
            return acc_tok

def get_keys(access_token):
    headers = {'Authorization': 'Bearer '+access_token, 'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        resp = requests.post(api_get_keys, headers=headers, verify=False)
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

def main():
    user, pwd, otp = get_user_credentials()
    bar = IncrementalBar('Retrieving signed SSH keys:', max = 3)
    public, private = get_keys(get_access_token(user, pwd, otp))
    bar.next()
    time.sleep(1)
    bar.next()
    time.sleep(1)
    save_keys(public, private)
    bar.next()
    time.sleep(1)
    bar.finish()

    message = """
    Usage:
    1. Add the key to the ssh agent:
       $ ssh-add ~/.ssh/cscs-key

    2. Connect to the login node using CSCS keys:
       $ ssh -i ~/.ssh/cscs-key <CSCS-LOGIN-NODE>
    """

    print(message)

if __name__ == "__main__":
    main()

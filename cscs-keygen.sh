#!/bin/bash

function ProgressBar {
# Process data
    let _progress=(${1}*100/${2}*100)/100
    let _done=(${_progress}*4)/10
    let _left=40-$_done
# Build progressbar string lengths
    _fill=$(printf "%${_done}s")
    _empty=$(printf "%${_left}s")

# 1.2 Build progressbar strings and print the ProgressBar line
# 1.2.1 Output example:
# 1.2.1.1 Progress : [########################################] 100%
printf "\rSetting the environment : [${_fill// /#}${_empty// /-}] ${_progress}%%"
}

#Variables
_start=1
#This accounts as the "totalState" variable for the ProgressBar function
_end=100

#Params
MFA_KEYS_URL="https://sshservice.cscs.ch/api/v1/auth/ssh-keys/signed-key"

#Detect OS
OS="$(uname)"
case "${OS}" in
  'Linux')
    OS='Linux'
    ;;
  'FreeBSD')
    OS='FreeBSD'
    ;;
  'WindowsNT')
    OS='Windows'
    ;;
  'Darwin')
    OS='Mac'
    ;;
  *) ;;
esac

#OS validation
if [ "${OS}" != "Mac" ] && [ "${OS}" != "Linux" ]; then
  echo "This script works only on Mac-OS or Linux. Abording."
  exit 1
fi

#Read Inputs
read -p "Username : " USERNAME
read -s -p "Password: " PASSWORD
echo
read -s -p "Enter OTP (6-digit code): " OTP
echo

#Validate inputs
if ! [[ "${USERNAME}" =~ ^[[:lower:]_][[:lower:][:digit:]_-]{2,15}$ ]]; then
    echo "Username is not valid."
    exit 1
fi

if [ -z "${PASSWORD}" ]; then
    echo "Password is empty."
    exit 1
fi

if ! [[ "${OTP}" =~ ^[[:digit:]]{6} ]]; then
    echo "OTP is not valid, OTP must contains only six digits."
    exit 1
fi

ProgressBar 25 "${_end}"
echo "  Authenticating to the SSH key service..."

HEADERS=(-H "Content-Type: application/json" -H "accept: application/json")
KEYS=$(curl -s -S --ssl-reqd \
    "${HEADERS[@]}" \
    -d "{\"username\": \"$USERNAME\", \"password\": \"$PASSWORD\", \"otp\": \"$OTP\"}" \
    "$MFA_KEYS_URL")

if [ $? != 0 ]; then
    exit 1
fi

ProgressBar 50 "${_end}"
echo "  Retrieving the SSH keys..."

DICT_KEY=$(echo ${KEYS} | cut -d \" -f 2)
if [ "${DICT_KEY}" == "payload" ]; then
   MESSAGE=$(echo ${KEYS} | cut -d \" -f 6)
   ! [ -z "${MESSAGE}" ] && echo "${MESSAGE}"
   echo "Error fetching the SSH keys. Aborting."
   exit 1
fi

PUBLIC=$(echo ${KEYS} | cut -d \" -f 4)
PRIVATE=$(echo ${KEYS} | cut -d \" -f 8)

#Check if keys are empty:
if [ -z "${PUBLIC}" ] || [ -z "${PRIVATE}" ]; then
    echo "Error fetching the SSH keys. Aborting."
    exit 1
fi

ProgressBar 75 "${_end}"
echo "  Setting up the SSH keys into your home folder..."

#Check ~/.ssh folder and store the keys
echo ${PUBLIC} | awk '{gsub(/\\n/,"\n")}1' > ~/.ssh/cscs-key-cert.pub || exit 1
echo ${PRIVATE} | awk '{gsub(/\\n/,"\n")}1' > ~/.ssh/cscs-key || exit 1

#Setting permissions:
chmod 644 ~/.ssh/cscs-key-cert.pub || exit 1
chmod 600 ~/.ssh/cscs-key || exit 1

#Format the keys:
if [ "${OS}" = "Mac" ]
then
  sed -i '' -e '$ d' ~/.ssh/cscs-key-cert.pub || exit 1
  sed -i '' -e '$ d' ~/.ssh/cscs-key || exit 1
else [ "${OS}" = "Linux" ]
  sed '$d' ~/.ssh/cscs-key-cert.pub || exit 1
  sed '$d' ~/.ssh/cscs-key || exit 1
fi

ProgressBar 100 "${_end}"
echo "  Completed."

#Usage message:
cat << EOF

Usage:
(Optional but recommended) Set a passphrase on the private key using the below command:
ssh-keygen -f ~/.ssh/cscs-key -p

1. Add the key to the SSH agent:
ssh-add ~/.ssh/cscs-key

2. Connect to the login node using CSCS keys:
ssh -A <CSCS-LOGIN-NODE>

Note - if the key not added to the SSH agent as mentioned in the step-1 above then use the command:
ssh -i ~/.ssh/cscs-key <CSCS-LOGIN-NODE>

EOF

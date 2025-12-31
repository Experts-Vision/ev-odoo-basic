#!/bin/bash
set -e

SERVER_NAME="$1"

# Get the script directory and navigate to parent
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

# Convert Unix path to Windows path for Docker
# /c/Users/... -> C:/Users/...
WIN_PATH=$(echo "${PWD}" | sed 's|^/\([a-z]\)/|\U\1:/|')

docker run --rm -v "${WIN_PATH}:/cloud-ubuntu" \
  -e ANSIBLE_HOST_KEY_CHECKING=False \
  alpine/ansible bash -c "
    echo 'Inside container, listing /cloud-ubuntu:' &&
    ls -la /cloud-ubuntu &&
    cd /cloud-ubuntu/ansible &&
    chmod 600 ./mahmoud-key.pem &&
    ansible-playbook -i inventory.yaml create_deploy.yaml -l $SERVER_NAME
  "
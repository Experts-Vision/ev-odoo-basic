#!/bin/bash
set -e

BACKUP_SERVER_NAME="$1"
cd /mnt/d/mahmoud/ev-odoo-basic/run-profiles/cloud-ubuntu

docker run --rm -v ${PWD}:/cloud-ubuntu \
  -e BACKUP_SERVER_NAME=$BACKUP_SERVER_NAME \
  -e ANSIBLE_HOST_KEY_CHECKING=False \
  alpine/ansible bash -c "
    cd /cloud-ubuntu/ansible &&
    chmod 600 ./mahmoud-key.pem &&
    ansible-playbook -i inventory.yaml backup.yaml -l $BACKUP_SERVER_NAME
  "

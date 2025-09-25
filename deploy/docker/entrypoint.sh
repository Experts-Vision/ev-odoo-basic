#!/bin/bash
echo "Running entrypoint.sh ..."

sudo python3 ./deploy/license-verification/src/main.py
exit_code=$?
if [ $exit_code -ne 0 ]; then
    exit $exit_code
fi

sudo python3 ./deploy/license-verification/src/job.py &

sudo exec odoo "$@"







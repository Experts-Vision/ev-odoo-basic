#!/bin/bash
echo "Running entrypoint.sh ..."

python3 ./deploy/license-verification/src/main.py
exit_code=$?
if [ $exit_code -ne 0 ]; then
    exit $exit_code
fi

python3 ./deploy/license-verification/src/job.py &

exec odoo "$@"







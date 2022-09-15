#!/bin/bash
cd /workspace/tata-python-backend
pm2-runtime "yarn dev"
cd /workspace/tata-python-backend/scripts
pm2-runtime "python3 clutch_plate.py"
wait -n
exit $?
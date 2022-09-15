#!/bin/bash
cd /workspace/tata-python-backend
pm2 start "yarn dev" --name "backend"
cd /workspace/tata-python-backend/scripts
pm2-runtime "python3 clutch_plate.py"
wait -n
exit $?
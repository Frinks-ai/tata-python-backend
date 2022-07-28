#!/bin/bash
cd /tata-python-backend
pm2-runtime "yarn dev"
wait -n
exit $?
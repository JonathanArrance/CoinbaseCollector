#!/bin/bash
python3 /opt/homebot/coinbase.py &

gunicorn -b 0.0.0.0:9030 --reload --access-logfile api_access.log --error-logfile api_error.log --log-level debug --timeout 120 -w 6 api &
/bin/sh -c envsubst < /nginx-default.conf > /etc/nginx/nginx.conf && exec nginx -g 'daemon off;' &

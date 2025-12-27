#!/bin/bash
#this is out of date and use sqlite3

openssl req -newkey rsa:4096  -x509  -sha512  -days 365 -nodes -subj "/C=US/ST=NC/L=AnyTown/O=Home/CN=coinbasecollector.com" -out /etc/api/ssl/apicert_chain.crt -keyout /etc/api/ssl/api_private_key.key

#python3 /opt/crypto/coinbase.py &
#python3 /opt/crypto/candles.py &
#python3 /opt/crypto/macd.py &
python3 /opt/crypto/scheduler.py &

# Start the API server
gunicorn -b 0.0.0.0:9030 --reload --access-logfile api_access.log --error-logfile api_error.log --log-level debug --timeout 120 -w 6 api &
/bin/sh -c envsubst < /nginx-default.conf > /etc/nginx/nginx.conf && exec nginx -g 'daemon off;' &

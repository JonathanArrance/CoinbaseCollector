#!/bin/bash

mkdir -p /opt/crypto/${DB_PATH}
mkdir -p /opt/crypto/ssl

openssl req -newkey rsa:4096  -x509  -sha512  -days 365 -nodes -subj "/C=US/ST=NC/L=AnyTown/O=Home/CN=coinbasecollector.com" -out /opt/crypto/ssl/apicert_chain.crt -keyout /opt/crypto/ssl/api_private_key.key

sqlite3 /opt/crypto${DB_PATH}/crypto.db "CREATE TABLE ValidCoins ( ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT, CoinName TEXT, CoinAbv TEXT)"
sqlite3 /opt/crypto${DB_PATH}/crypto.db "INSERT OR IGNORE INTO ValidCoins (CoinName,CoinAbv) VALUES ('Bitcoin','btc')"
sqlite3 /opt/crypto${DB_PATH}/crypto.db "INSERT OR IGNORE INTO ValidCoins (CoinName,CoinAbv) VALUES ('Ethereum','eth')"
sqlite3 /opt/crypto${DB_PATH}/crypto.db "INSERT OR IGNORE INTO ValidCoins (CoinName,CoinAbv) VALUES ('Dogecoin','doge')"

python3 /opt/crypto/coinbase.py &

gunicorn -b 0.0.0.0:9030 --reload --access-logfile api_access.log --error-logfile api_error.log --log-level debug --timeout 120 -w 6 api &
/bin/sh -c envsubst < /nginx-default.conf > /etc/nginx/nginx.conf && exec nginx -g 'daemon off;' &

#!/bin/bash

mkdir -p ${DB_PATH}
#mkdir -p /opt/crypto/ssl

#openssl req -newkey rsa:4096  -x509  -sha512  -days 365 -nodes -subj "/C=US/ST=NC/L=AnyTown/O=Home/CN=coinbasecollector.com" -out /opt/crypto/ssl/apicert_chain.crt -keyout /opt/crypto/ssl/api_private_key.key
openssl req -newkey rsa:4096  -x509  -sha512  -days 365 -nodes -subj "/C=US/ST=NC/L=AnyTown/O=Home/CN=coinbasecollector.com" -out /etc/api/ssl/apicert_chain.crt -keyout /etc/api/ssl/api_private_key.key

#create the tables
sqlite3 ${DB_PATH}/crypto.db "CREATE TABLE if not exists ValidCoins (ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT, CoinName TEXT UNIQUE, CoinAbv TEXT UNIQUE, CoinTicker TEXT UNIQUE)"
sqlite3 ${DB_PATH}/crypto.db "CREATE TABLE if not exists cryptoHistory (ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT, coin TEXT, timestamp TEXT, price TEXT)"

sqlite3 ${DB_PATH}/crypto.db "INSERT OR IGNORE INTO ValidCoins (CoinName,CoinAbv,CoinTicker) VALUES ('Bitcoin','btc','btc-usd')"
sqlite3 ${DB_PATH}/crypto.db "INSERT OR IGNORE INTO ValidCoins (CoinName,CoinAbv,CoinTicker) VALUES ('Ethereum','eth','eth-usd')"
sqlite3 ${DB_PATH}/crypto.db "INSERT OR IGNORE INTO ValidCoins (CoinName,CoinAbv,CoinTicker) VALUES ('Dogecoin','doge','doge-usd')"
sqlite3 ${DB_PATH}/crypto.db "INSERT OR IGNORE INTO ValidCoins (CoinName,CoinAbv,CoinTicker) VALUES ('Chainlink','link','link-usd')"

python3 /opt/crypto/coinbase.py &

gunicorn -b 0.0.0.0:9030 --reload --access-logfile api_access.log --error-logfile api_error.log --log-level debug --timeout 120 -w 6 api &
/bin/sh -c envsubst < /nginx-default.conf > /etc/nginx/nginx.conf && exec nginx -g 'daemon off;' &

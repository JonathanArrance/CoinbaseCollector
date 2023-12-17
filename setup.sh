#!/bin/bash

#setup on the local machine for test and dev
#source your env variables first

docker network create --driver bridge --subnet 172.18.0.0/16 container_net

mkdir -p $(pwd)/db
mkdir -p $(pwd)/ssl

openssl req -newkey rsa:4096  -x509  -sha512  -days 365 -nodes -subj "/C=US/ST=NC/L=AnyTown/O=Home/CN=coinbasecollector.com" -out ./ssl/apicert_chain.crt -keyout ./ssl/api_private_key.key

sqlite3 /opt/crypto${DB_PATH}/crypto.db "CREATE TABLE if not exists ValidCoins ( ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT, CoinName TEXT, CoinAbv TEXT)"
sqlite3 /opt/crypto${DB_PATH}/crypto.db "CREATE TABLE if not exists cryptoHistory (ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT, coin TEXT, timestamp TEXT, price TEXT)"

sqlite3 .${DB_PATH}/crypto.db "INSERT OR IGNORE INTO ValidCoins (CoinName,CoinAbv) VALUES ('Bitcoin','btc')"
sqlite3 .${DB_PATH}/crypto.db "INSERT OR IGNORE INTO ValidCoins (CoinName,CoinAbv) VALUES ('Ethereum','eth')"
sqlite3 .${DB_PATH}/crypto.db "INSERT OR IGNORE INTO ValidCoins (CoinName,CoinAbv) VALUES ('Dogecoin','doge')"
sqlite3 .${DB_PATH}/crypto.db "INSERT OR IGNORE INTO ValidCoins (CoinName,CoinAbv) VALUES ('Chainlink','link')"

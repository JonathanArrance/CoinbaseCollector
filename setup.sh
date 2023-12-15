#!/bin/bash
docker network create --driver bridge --subnet 172.18.0.0/16 container_net

mkdir -p $(pwd)/db
mkdir -p $(pwd)/ssl

openssl req -newkey rsa:4096  -x509  -sha512  -days 365 -nodes -subj "/C=US/ST=NC/L=AnyTown/O=Home/CN=coinbasecollector.com" -out ./ssl/apicert_chain.crt -keyout ./ssl/api_private_key.key

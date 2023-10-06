#!/bin/bash
docker network create --driver bridge --subnet 172.18.0.0/16 container_net

mkdir -p $(pwd)/db
mkdir -p $(pwd)/ssl

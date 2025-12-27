#!/bin/bash -x
docker run -ti -p 9011:9029 -p 9010:9030 \
--mount type=bind,source="$(pwd)"/ssl,target=/etc/api/ssl \
-e APIVER='beta' \
-e COINBASE_INTERVAL=30 \
-e DB_PATH='/opt/crypto/db' \
-e PGSQL_HOST='192.168.1.66' \
-e PGSQL_PORT=5432 \
-e PGSQL_DB='cryptoanalyzer' \
-e PGSQL_USER='developer' \
-e PGSQL_PASSWORD='bjjisfun!' \
--network container_net \
--name coinbase-collector \
coinbase-collector:latest

#--mount type=bind,source="$(pwd)"/ssl,target=/etc/api/ssl \
#-e NGINX_PORT=443 \

#!/bin/bash -x
docker run -p 443:443 --name web_interface \
-e NGINX_PORT=443 \
--mount type=bind,source="$(pwd)"/ssl,target=/etc/api/ssl \
--mount type=bind,source="$(pwd)"/html,target=/usr/share/nginx/html \
--mount type=bind,source="$(pwd)"/conf/nginx-web.conf,target=/etc/nginx/nginx.conf \
--network container_net \
-d nginx

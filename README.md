# CoinbaseConnector

## Overview

The collector sits between Coinbase and your Grafana+Prometheus deployment. Setting up Prometheus and Grafana are outside of the scope of this document. 

**Grafana** - Used for visualization and sending webhook alerts to the connector.

**Prometheus** - Scrapes the metrics(prices) from the connector.

**Connector** - Pulls the priceing and other metrics for the valid coins defined in the database. Also acts as a buy/sell API that can be queried when price targets are reached. The API endpoints can also be used with other forms of automation.

**Coinbase** - Current crypto brokerage platform.

<img src="./Images/connector.png">

## Setup

**Tools used**

Coinbase API

Docker

Python Promeheus v0.17.1

**Build**

Build the container with the *build_container.sh*

**Environment variables**

```bash
TIMESERVER='pool.ntp.org'
COINBASE_INTERVAL=10
DB_PATH='/db'
COINBASE_KEY=''
```

**Run the container**

```bash
docker run -d -p 9029:9029 -p 9030:9030 \
--mount type=bind,source="$(pwd)"/db,target=/db \
--mount type=bind,source="$(pwd)"/ssl,target=/etc/api/ssl \
-e APIVER='beta' \
-e COINBASE_INTERVAL=30 \
--network container_net \
--name coinbase_collector \
coinbase_collector:latest
```

**Database**

The SQLite DB is stored in the /db location in the container by default. To chnage it you will need to set the DB_PATH env varibale. 

## Prometheus

**Config**

```yaml
global:
  scrape_interval: 5s
  evaluation_interval: 5s
rule_files:
  - /etc/prometheus/prometheus.rules
alerting:
  alertmanagers:
  - scheme: http
    static_configs:
    - targets:
      - "alertmanager.monitoring.svc:9093"

scrape_configs:
  - job_name: 'CoinbaseConnector'
    metrics_path: /metrics
    static_configs:
      - targets: ['192.168.10.88:9029']
```

## REST API

**Simple API connection**

In order to ge to the REST API or add it into your alert webooks, use port 9030 to reach it.

**Endpoints**

In order to get to the endpoint Swagger doc use port 9030.

```bash
https://localhost:9030
```

## Grafana Dashboard
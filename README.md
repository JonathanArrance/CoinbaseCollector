# CoinbaseConnector

## Overview

The collector sits between Coinbase and your Grafana+Prometheus deployment. Setting up Prometheus and Grafana are outside of the scope of this document. 

**Grafana** - Used for visualization and sending webhook alerts to the connector.

**Prometheus** - Scrapes the metrics(prices) from the connector.

**Connector** - Pulls the priceing and other metrics for the valid coins defined in the SQLite DB. Also acts as a buy/sell API that can be fired off when prices targets are reached. The API endpoints can also be used with other forms of automation.

**Coinbase** - Current crypto brokerage platform.

<img src="./Images/connector.png">

## Setup

**Tools used**

**Build**

**Environment variables**

**Run the container**

**Database**


## Prometheus Config

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

## Grafana Dashboard
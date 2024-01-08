import os
import settings
import logging

from prometheus_client import start_http_server
from prometheus_client import Gauge

class prometheus():

    def __init__(self):
        """
        DESC: Initialize
        INPUT:
        OUTPUT: None
        """
        logging.info("Starting Prometheus scrape endpoint.")

    def start_server(self):
        start_http_server(9029)

        self.coin_price = Gauge('coin_price_usd', 'Bitcoin Price in USD',['ticker','name'])
        self.coin_ask = Gauge('coin_ask_usd', 'Bitcoin Ask in USD',['ticker','name'])
        self.coin_bid = Gauge('coin_bid_usd', 'Bitcoin Bid in USD',['ticker','name'])
        self.coin_volume = Gauge('coin_volume_usd', 'Bitcoin Volume',['ticker','name'])
    
    def current_price(self,input_dict):
        print(input_dict)
        try:
            logging.info("Emitting weather station metrics.")
            self.coin_price.labels(input_dict['ticker'],input_dict['name']).set(input_dict['coin_price'])
            self.coin_bid.labels(input_dict['ticker'],input_dict['name']).set(input_dict['coin_bid'])
            self.coin_ask.labels(input_dict['ticker'],input_dict['name']).set(input_dict['coin_ask'])
            self.coin_volume.labels(input_dict['ticker'],input_dict['name']).set(input_dict['coin_volume'])
        except Exception as e:
            logging.error(e)
            logging.error("Could not emit coin metrics.")

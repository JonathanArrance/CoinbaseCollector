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
        start_http_server(9029)

        self.btc_price_gauge = Gauge('bitcoin_price_usd', 'Bitcoin Price in USD')
        self.eth_price_gauge = Gauge('ethereum_price_usd', 'Ethereum Price in USD')

    def bitcoin_price(self,input_dict):

        try:
            self.btc_price_gauge.set(input_dict['price'])
        except Exception as e:
            logging.error(e)

    def etherium_price(self,input_dict):

        try:
            self.eth_price_gauge.set(input_dict['price'])
        except Exception as e:
            logging.error(e)

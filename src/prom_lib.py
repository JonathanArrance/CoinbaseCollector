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

        self.coin_price = Gauge('coin_price_usd', 'Coin Price in USD',['ticker','coin'])
        self.coin_ask = Gauge('coin_ask_usd', 'Coin Ask in USD',['ticker','coin'])
        self.coin_bid = Gauge('coin_bid_usd', 'Coin Bid in USD',['ticker','coin'])
        self.coin_volume = Gauge('coin_volume_usd', 'Coin Volume',['ticker','coin'])
    
    def current_price(self,input_dict):
        try:
            logging.info("Emitting weather station metrics.")
            self.coin_price.labels(input_dict['ticker'],input_dict['coin']).set(input_dict['price'])
            self.coin_bid.labels(input_dict['ticker'],input_dict['coin']).set(input_dict['bid'])
            self.coin_ask.labels(input_dict['ticker'],input_dict['coin']).set(input_dict['ask'])
            self.coin_volume.labels(input_dict['ticker'],input_dict['coin']).set(input_dict['volume'])
        except Exception as e:
            logging.error(e)
            logging.error("Could not emit coin metrics.")

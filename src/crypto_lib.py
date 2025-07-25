import requests
import time
from database import Database
import pandas as pd

db = Database()

class Crypto:

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json'
            }

    def sell_coin_market(self):
        pass

    def buy_coin_market(self):
        pass

    def buy_coin_limit(self):
        pass

    def sell_coin_limit(self):
        pass
    
    def call_url(self,url):
        """
        DESC: Call the desired URL
        """
        try:
            # Make a GET request to the API
            response = requests.get(url)
        except Exception as e:
            print(f"An error occurred: {e}")

        return response

    def get_coin_catalog(self):
        """
        DESC: Get a list of available coins from the source of truth
        INPUT: None
        OUTPUT: list of dict - coin_name
                             - coin_ticker
        """
        currency='USD'
        url = "https://api.exchange.coinbase.com/products/"

        out_coins = []

        response = requests.get(url)
        try:
            if response.status_code == 200:
                coins = response.json()
                for coin in coins:
                    if coin['quote_currency'] == str(currency).upper():
                        out_coins.append(coin)
            else:
                print(f"Error: Unable to fetch data. Status code: {response.status_code}")
        except Exception as e:
            print(f"Could not find an coins traded in {currency}")

        return out_coins
    
    def get_candles(self,input_dict):
        """
        DESC: Get the candles for a coin ticker
        INPUT: coin_ticker - the ticker of the coin to get candles for
               granularity - 60,300,21600,86400 (1 minute, 5 minutes, 6 hours, 1 day)
        OUTPUT: DataFrame - candles with columns: timestamp, low, high, open, close, volume
        """
        url = f"https://api.exchange.coinbase.com/products/{input_dict['coin_ticker']}/candles"
        
        params = {'granularity': input_dict['granularity']}

        response = requests.get(url, params=params)

        try:
            if response.status_code == 200:
                # Parse the response JSON to get the candles
                response = response.json()
            else:
                print(f"Error: Unable to fetch candles. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred while fetching candles: {e}")

        df = pd.DataFrame(response, columns=['timestamp', 'low', 'high', 'open', 'close', 'volume'])
        
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        
        return df.sort_values('timestamp')
    
    def get_coin_price(self,input_dict):
        """
        DESC: Get the coin price, the price endpoint is open and does not need authentication
        INPUT: input_dict - coin_name
                          - coin_ticker
        OUTPUT: out_dict - coin_name
                         - coin_ask
                         - coin_bid
                         - coin_volume
                         - coin_ticker
                         
        this needs to be fixed. need to account for the floats properly and format the output.

        Traceback (most recent call last):
        File "/opt/crypto/coinbase.py", line 31, in <module>
            main()
        File "/opt/crypto/coinbase.py", line 25, in main
            pr.current_price(coin)
        File "/opt/crypto/prom_lib.py", line 31, in current_price
            self.coin_bid.labels(input_dict['ticker'],input_dict['coin']).set(input_dict['bid'])
        File "/usr/local/lib/python3.11/dist-packages/prometheus_client/metrics.py", line 396, in set
            self._value.set(float(value))
                            ^^^^^^^^^^^^
        TypeError: float() argument must be a string or a real number, not 'NoneType'

        
        """
        url = f"https://api.exchange.coinbase.com/products/{input_dict['coin_ticker']}/ticker"
        
        price = bid = ask = volume = None

        try:
            # Make a GET request to the API
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the response JSON to get the price
                data = response.json()
                price = float(data["price"])
                bid = float(data["bid"])
                ask = float(data["ask"])
                volume = float(data["volume"])

                print(f"Current {input_dict['coin_name']} Price: ${price:.2f}")
            else:
                print(f"Error: Unable to fetch data. Status code: {response.status_code}")

        except Exception as e:
            print(f"An error occurred: {e}")
            return({'coin':input_dict['coin_name'],'timestamp':time.time(),'price':0.00,'bid':0.00,'ask':0.00,'volume':0.00,'ticker':input_dict['coin_ticker']})

        return({'coin':input_dict['coin_name'],'timestamp':time.time(),'price':price,'bid':bid,'ask':ask,'volume':volume,'ticker':input_dict['coin_ticker']})

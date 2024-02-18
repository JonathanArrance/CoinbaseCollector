import requests
import time
import settings
from database import Database

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

    def get_portfolio(self):
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
        """
        url = f"https://api.pro.coinbase.com/products/{input_dict['coin_ticker']}/ticker"
        #return self.call_price_url(f"{input_dict['coin_name']}",url)
        price = bid = ask = volume = None

        try:
            # Make a GET request to the API
            response = requests.get(url)
            tick = url.split('/')

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
            #price ="0.00"
            return({'coin':input_dict['coin_name'],'timestamp':time.time(),'price':0.00,'bid':0.00,'ask':0.00,'volume':0.00,'ticker':tick[-2]})

        return({'coin':input_dict['coin_name'],'timestamp':time.time(),'price':price,'bid':bid,'ask':ask,'volume':volume,'ticker':tick[-2]})

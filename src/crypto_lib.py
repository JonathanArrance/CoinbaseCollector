import requests
import time
import settings

class Crypto:

    def __init__(self):
        pass

    def call_url(self,coin,url):

        #valid = ['etherium','bitcoin','chainlink','Doge']

        if coin not in settings.VALID_COINS:
            raise Exception(f'The coin, {coin} is not a valid coin.')
        else:
            coin = coin.capitalize()

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

                print(f"Current {coin} Price: ${price:.2f}")
            else:
                print(f"Error: Unable to fetch data. Status code: {response.status_code}")

        except Exception as e:
            print(f"An error occurred: {e}")
            price ="0.00"

        return({'coin':coin,'timestamp':time.time(),'price':price,'bid':bid,'ask':ask,'volume':volume,'ticker':tick[-2]})

    def get_eth_price(self):
        url = "https://api.pro.coinbase.com/products/eth-usd/ticker"
        return self.call_url("etherium",url)

    def get_btc_price(self):
        url = "https://api.pro.coinbase.com/products/btc-usd/ticker"
        return self.call_url("bitcoin",url)

    def get_doge_price(self):
        url = "https://api.pro.coinbase.com/products/doge-usd/ticker"
        return self.call_url("dogecoin",url)
    
    def get_link_price(self):
        url = "https://api.pro.coinbase.com/products/link-usd/ticker"
        return self.call_url("dogecoin",url)

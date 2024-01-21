from crypto_lib import Crypto
from prom_lib import prometheus as prom
from database import Database
import time
import settings

def main():

    pr = prom()
    data = Database()
    cr = Crypto()

    pr.start_server()

    while True:
        btc = cr.get_btc_price()
        pr.current_price(btc)
        print('\n')
        eth = cr.get_eth_price()
        pr.current_price(eth)
        print('\n')
        doge = cr.get_doge_price()
        pr.current_price(doge)

        data.write_to_history(btc)
        data.write_to_history(eth)
        data.write_to_history(doge)
        time.sleep(settings.COINBASE_INTERVAL)

if __name__ == '__main__':
    main()

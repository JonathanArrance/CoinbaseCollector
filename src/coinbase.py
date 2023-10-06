from crypto_lib import Crypto
from prom_lib import prometheus as prom
from database import Database
import time
import settings

def main():

    pr = prom()
    data = Database()
    cr = Crypto()

    while True:
        btc = cr.get_btc_price()
        print('\n')
        eth = cr.get_eth_price()

        #emit the prom database
        pr.bitcoin_price(btc)
        pr.etherium_price(eth)
        data.write_to_db(btc)
        data.write_to_db(eth)
        time.sleep(settings.COINBASE_INTERVAL)

if __name__ == '__main__':
    main()

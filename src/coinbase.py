from crypto_lib import Crypto
from prom_lib import prometheus as prom
from database import Database
import time
import settings

def main():

    pr = prom()
    db = Database()
    cr = Crypto()

    pr.start_server()

    while True:
        valid_coins = db.get_coins()
        for valcoin in valid_coins:
            coin = cr.get_coin_price({"coin_name":valcoin[2],"coin_ticker":valcoin[3]})
            pr.current_price(coin)
            print('\n')
            db.write_to_history(coin)
            time.sleep(settings.COINBASE_INTERVAL)

if __name__ == '__main__':
    main()

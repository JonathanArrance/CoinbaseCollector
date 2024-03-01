from crypto_lib import Crypto
from prom_lib import prometheus as prom
from database import Database
from multiprocessing import Process
import time
import settings

pr = prom()
db = Database()
cr = Crypto()
pr.start_server()

def worker(valcoin):
    coin = cr.get_coin_price(valcoin)
    pr.current_price(coin)
    print('\n')
    db.write_to_history(coin)

def main():

    while True:
        valid_coins = db.get_coins()
        processes = []
        for valcoin in valid_coins:
            p = Process(target=worker, args=(valcoin,))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()
        
        time.sleep(settings.COINBASE_INTERVAL)

if __name__ == '__main__':
    main()

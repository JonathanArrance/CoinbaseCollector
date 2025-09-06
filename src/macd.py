from crypto_lib import Crypto
from database import Database
import time
import logging

def main():

    db = Database()
    cr = Crypto()

    while True:
        valid_coins = db.get_coins()
        for valcoin in valid_coins:
            #granularity = ['60','300','900','3600']
            granularity = ['60']
            
            #remove old entries over a year old.
            #db.delete_old_pg_entries(valcoin['coin_ticker'])
            for gran in granularity: 
                logging.info(f"Calculating MACD for {valcoin['coin_ticker']} with granularity {gran}")
                md = cr.coin_macd(cs)
                logging.info(md)
                db.insert_macd({'macd_df':md,
                                'coin_ticker':valcoin['coin_ticker'],
                                'coin_name':valcoin['coin_name'],
                                'granularity':gran
                                })
            time.sleep(43200)

if __name__ == '__main__':
    main()
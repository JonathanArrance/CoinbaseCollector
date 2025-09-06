from crypto_lib import Crypto
from database import Database
import time
import logging
import settings

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
                logging.info(f"Getting candles for {valcoin['coin_ticker']} with granularity {gran}")
                cs = cr.get_candles({'coin_ticker':valcoin['coin_ticker'],'granularity':gran})
                db.insert_candles({'candle_df':cs,
                                'coin_ticker':valcoin['coin_ticker'],
                                'coin_name':valcoin['coin_name'],
                                'granularity':gran
                                })

        time.sleep(settings.CANDLE_INTERVAL)

if __name__ == '__main__':
    main()
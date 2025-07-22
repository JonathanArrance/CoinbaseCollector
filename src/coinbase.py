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

    try:
        while True:
            valid_coins = db.get_coins()
            for valcoin in valid_coins:
                coin = cr.get_coin_price(valcoin)
                pr.current_price(coin)
                print('\n')
                db.write_to_history(coin)
            
                granularity = ['60','300','900','3600']
                for gran in granularity:
                    cs = cr.get_candles({'coin_ticker':valcoin['coin_ticker'],'granularity':gran})
                    db.insert_candles({'candle_df':cs,
                                    'coin_ticker':valcoin['coin_ticker'],
                                    'coin_name':valcoin['coin_name'],
                                    'granularity':gran
                                    })
                    time.sleep(1)
                
                time.sleep(settings.COINBASE_INTERVAL)
    except Exception as e:
        print(e)
        db.close_pg_connection()

if __name__ == '__main__':
    main()



"""
ERROR:root:float() argument must be a string or a real number, not 'NoneType'
ERROR:root:Could not emit coin metrics.

"""
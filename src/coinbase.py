from crypto_lib import Crypto
from prom_lib import prometheus as prom
from database import Database
import time
import settings



def _gen_interval():
    """
    DESC: Generate the interval for the candelstick data
    """
    pass

def candelstick_60(ticker):
    """
    """
    
    pass

def candelstick_300(ticker):
    """
    """
    pass

def candelstick_900(ticker):
    """
    """
    pass

def candelstick_3600(ticker):
    """
    """
    pass

def main():

    db = Database()
    pr = prom()
    cr = Crypto()

    pr.start_server()

    #try:
    while True:
        valid_coins = db.get_coins()
        for valcoin in valid_coins:
            coin = cr.get_coin_price(valcoin)
            pr.current_price(coin)
            print('\n')
            db.write_to_history(coin)
        
            granularity = ['60','300','900','3600']
            db.delete_old_pg_entries(valcoin['coin_ticker'])
            for gran in granularity: 
                print(f"Getting candles for {valcoin['coin_ticker']} with granularity {gran}")
                cs = cr.get_candles({'coin_ticker':valcoin['coin_ticker'],'granularity':gran})
                db.insert_candles({'candle_df':cs,
                                'coin_ticker':valcoin['coin_ticker'],
                                'coin_name':valcoin['coin_name'],
                                'granularity':gran
                                })
                md = cr.coin_macd(cs)
                db.insert_macd({'macd_df':md,
                                'coin_ticker':valcoin['coin_ticker'],
                                'coin_name':valcoin['coin_name'],
                                'granularity':gran
                                })
                time.sleep(1)

            time.sleep(settings.COINBASE_INTERVAL)
    #except Exception as e:
    #    print(e)
    #    db.close_pg_connection()

if __name__ == '__main__':
    main()



"""
ERROR:root:float() argument must be a string or a real number, not 'NoneType'
ERROR:root:Could not emit coin metrics.

"""
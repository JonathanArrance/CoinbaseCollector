from crypto_lib import Crypto
from prom_lib import prometheus as prom
from database import Database
import logging
import threading
import schedule
import time
import settings

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

def macd_job():

    while True:
        #open up the DB connection for writing
        db.open_pg_connection()
        try:
            logging.info("Starting MACD job cycle.")
            print("Starting MACD Job Cycle")
            valid_coins = db.get_coins()
            for valcoin in valid_coins:
                #granularity = ['60','300','900','3600']
                granularity = ['60']
                
                #remove old entries over a year old.
                #db.delete_old_pg_entries(valcoin['coin_ticker'])
                for gran in granularity: 
                    logging.info(f"Calculating MACD for {valcoin['coin_ticker']} with granularity {gran}")
                    print(f"Calculating MACD for {valcoin['coin_ticker']} with granularity {gran}")
                    cs = cr.get_candles({'coin_ticker':valcoin['coin_ticker'],'granularity':gran})
                    md = cr.coin_macd(cs)
                    logging.info(md)
                    db.insert_macd({'macd_df':md,
                                    'coin_ticker':valcoin['coin_ticker'],
                                    'coin_name':valcoin['coin_name'],
                                    'granularity':gran
                                    })
        except Exception as e:
            logging.error(f"Error in macd_job: {e}")
            print(f"Error in macd_job: {e}")
        db.close_pg_connection()

def candle_job():
    
    while True:
        db.open_pg_connection()
        try:
            logging.info("Starting candle job cycle.")
            valid_coins = db.get_coins()
            for valcoin in valid_coins:
                #granularity = ['60','300','900','3600']
                granularity = ['60']
                
                #remove old entries over a year old.
                #db.delete_old_pg_entries(valcoin['coin_ticker'])
                for gran in granularity: 
                    logging.info(f"Getting candles for {valcoin['coin_ticker']} with granularity {gran}")
                    print(f"Getting candles for {valcoin['coin_ticker']} with granularity {gran}")
                    cs = cr.get_candles({'coin_ticker':valcoin['coin_ticker'],
                                        'granularity':gran
                                        })

                    db.insert_candles({'candle_df':cs,
                                    'coin_ticker':valcoin['coin_ticker'],
                                    'coin_name':valcoin['coin_name'],
                                    'granularity':gran
                                    })
        except Exception as e:
            logging.error(f"Error in candle_job: {e}")
            print(f"Error in candle_job: {e}")
        
        db.close_pg_connection()

def coinbase_job():
    
    while True:
        db.open_pg_connection()        
        try:
            logging.info("Starting coinbase job cycle.")
            valid_coins = db.get_coins()
            for valcoin in valid_coins:
                logging.info(f"Getting price for {valcoin}")
                coin = cr.get_coin_price(valcoin)
                pr.current_price(coin)
                print('\n')
                db.write_to_history(coin)
                time.sleep(settings.COINBASE_INTERVAL)
        except Exception as e:
            logging.error(f"Error in coinbase_job: {e}")
            print(f"Error in coinbase_job: {e}")
        db.close_pg_connection()

if __name__ == '__main__':

    db = Database()
    cr = Crypto()
    pr = prom()
    
    pr.start_server()

    #schedule.every(settings.COINBASE_INTERVAL).seconds.do(run_threaded,coinbase_job)
    schedule.every(settings.COINBASE_INTERVAL).seconds.do(coinbase_job)
    
    schedule.every(settings.CANDLE_INTERVAL).seconds.do(run_threaded,candle_job)
    #schedule.every(settings.CANDLE_INTERVAL).seconds.do(candle_job)
    
    schedule.every(settings.MACD_INTERVAL).seconds.do(run_threaded,macd_job)
    #schedule.every(settings.MACD_INTERVAL).seconds.do(macd_job)

    while True:
        #db.open_pg_connection()
        schedule.run_pending()
        time.sleep(1)
        #db.close_pg_connection()
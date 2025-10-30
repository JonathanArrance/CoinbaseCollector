import sqlite3
import psycopg2
import logging
import settings
import time
from datetime import datetime

class Database:

    def __init__(self):
        pass

    def open_pg_connection(self):
        try:
            self.pgconn = psycopg2.connect(**settings.PG_CONFIG)
            logging.info("Connected to the PostgreSQL DB.")
        except Exception as e:
            logging.error(f"Could not create the cryptoHistory table: {e}.")
            raise e

        #establish a pgsql cursor
        self.pgcur = self.pgconn.cursor()

    def close_pg_connection(self):
        logging.info("Closing the PostgreSQL DB connection.")
        self.pgconn.close()
    
    def delete_old_pg_entries(self,ticker):
        """
        DESC: Delete entries in the PostgreSQL database that are older than a year.
        """
        one_year_ago = int(time.time()) - (365 * 24 * 60 * 60)  # Calculate the timestamp for one year ago

        try:
            self.pgcur.execute(
                "DELETE FROM coinbase_ohlc WHERE epoctimestamp <= %s and symbol = %s", (one_year_ago,ticker)
            )
            self.pgconn.commit()
            logging.info("Successfully deleted candlestick entries older than a year.")
        except Exception as e:
            logging.error(f"Could not delete old candlestick entries: {e}.")
            self.pgconn.rollback()
        
        try:
            self.pgcur.execute(
                "DELETE FROM coinbase_macd WHERE epoctimestamp <= %s and symbol = %s", (one_year_ago,ticker)
            )
            self.pgconn.commit()
            logging.info("Successfully deleted MACD entries older than a year.")
        except Exception as e:
            logging.error(f"Could not delete old MACD entries: {e}.")
            self.pgconn.rollback()
        
        #I need to add the new tables

    def insert_macd(self,input_dict):
        """
        DESC: Insert the MACD into the cryptoHistory table
        INPUT: macd_df - DataFrame with the MACD
               coin_ticker 
        OUTPUT: True if successful, False if not
        """
        df = input_dict['macd_df']
        ticker = input_dict['coin_ticker']
        coin_name = input_dict['coin_name']
        granularity = str(input_dict['granularity'])

        print(f"Inserting MACD for {ticker} with granularity {granularity} into the PGsql DB.")
        for _, row in df.iterrows():
            try:
                self.pgcur.execute(
                    """INSERT INTO coinbase_macd (epoctimestamp, timestamp, symbol, macd, signal, histogram, coinname, granularity)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (epoctimestamp, symbol, granularity) DO NOTHING""", 
                    (row['epoctimestamp'],
                     row['timestamp'], 
                     ticker, 
                     row['MACD'], 
                     row['signal'], 
                     row['Histogram'], 
                     coin_name, 
                     granularity)
                )
                self.pgconn.commit()
            except Exception as e:
                print(e)
                logging.error(f"Could not insert MACD into the DB: {e}.")
                self.pgconn.rollback()

        return True
    
    def insert_candles(self,input_dict):
        """
        DESC: Insert the candles into the cryptoHistory table
        INPUT: candle_df - DataFrame with the candles
               coin_ticker 
        OUTPUT: True if successful, False if not
        """
        df = input_dict['candle_df']
        ticker = input_dict['coin_ticker']
        coin_name = input_dict['coin_name']
        granularity = str(input_dict['granularity'])

        print(f"Inserting candles for {ticker} with granularity {granularity} into the PGsql DB.")
        for _, row in df.iterrows():
            #int(datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S%z").timestamp())
            try:
                self.pgcur.execute(
                    """INSERT INTO coinbase_ohlc (epoctimestamp, timestamp, symbol, open, high, low, close, volume, coinname, granularity)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (epoctimestamp, symbol, granularity) DO NOTHING""", 
                    (row['epoctimestamp'],
                     row['timestamp'], 
                     ticker, 
                     row['open'], 
                     row['high'], 
                     row['low'], 
                     row['close'], 
                     row['volume'], 
                     coin_name, 
                     granularity)
                )
                self.pgconn.commit()
            except Exception as e:
                print(e)
                logging.error(f"Could not insert candles into the DB: {e}.")
                self.pgconn.rollback()

        #cur.close()
        #self.pgconn.close()
        return True
    
    def write_to_history(self,input_dict):

        try:
            sql = """
                INSERT INTO cryptoHistory (coin, timestamp, price)
                VALUES (%s, %s, %s)
            """
            self.pgcur.execute(sql, (
                input_dict['coin'],
                int(input_dict['timestamp']),
                input_dict['price']
            ))
            self.pgconn.commit()

        except Exception as e:
            self.pgconn.rollback()   # rollback only on error
            print(e)
            logging.error(f'Could not write to the DB: {e}.')
            return False

        return True

    def add_coin(self,input_dict):
        """
        DESC: Add a valid coin to query
        INPUT: input_dict - coinname
                          - coinabv
                          - cointicker
        NOTe: {'CoinName': 'Bitcoin', 'CoinAbv':'btc','CoinTicker':'btc-usd'}
        """
        out = {'CoinName': None, 'CoinAbv': None, 'CoinTicker': None}

        coinname = str(input_dict['coinname']).capitalize()
        abv = str(input_dict['coinabv']).lower()
        ticker = str(input_dict['cointicker']).lower()

        try:
            sql = """
                INSERT INTO validCoins (CoinName, CoinAbv, CoinTicker)
                VALUES (%s, %s, %s)
                ON CONFLICT (CoinAbv) DO UPDATE
                SET CoinName = EXCLUDED.CoinName,
                    CoinTicker = EXCLUDED.CoinTicker
            """
            self.pgcur.execute(sql, (coinname, abv, ticker))
            self.pgconn.commit()

            out = {'CoinName': coinname, 'CoinAbv': abv, 'CoinTicker': ticker}

        except Exception as e:
            self.pgconn.rollback()
            print(e)
            logging.error(f'Could not write to the DB: {e}.')

        return out


    def get_valid_coins(self):
        """
        DESC: Get the valid coins
        """
        coins = self.get_coins()
        valid = []
        for coin in coins:
            out = {'coin_name':str(coin['coinname']).lower() ,'coin_ticker':coin['coinname']}
            valid.append(out)
        
        return valid

    def get_coins(self):
        """
        DESC: List all of the valid coins
        INPUT: None
        OUTPUT: out_list of tuples
        NOTe: 
        """
        out = []
        rows = []

        try:
            self.pgcur.execute("SELECT * FROM validcoins")
            rows = self.pgcur.fetchall()
        except Exception as e:
            print(e)
            logging.error(f'Could not list the ValidCoins: {e}.')

        for row in rows:
            out.append({
                'id': row[0],
                'coin_name': row[1],
                'coin_abv': row[2],
                'coin_ticker': row[3]
            })

        return out

    def get_coin(self,coinname=None,coinid=None):
        """
        DESC: Get the coin specifics and price history
        INPUT: coinname
        OUTPUT: out_dict - name
                         - bid
                         - ask
                         - volume
        """
        coinname = coinname.capitalize()
        out = {}

        try:
            sql = "SELECT ID, CoinName, CoinAbv, CoinTicker FROM validCoins WHERE CoinName = %s"
            self.pgcur.execute(sql, (coinname,))
            row = self.pgcur.fetchone()
            
            if row:
                out = {
                    'index': row[0],
                    'coin_name': row[1],
                    'coin_abv': row[2],
                    'coin_ticker': row[3]
                }
            else:
                logging.warning(f"No entry found in ValidCoins for coin: {coinname}")
                out = None

        except Exception as e:
            print(e)
            logging.error(f"Could not find {coinname} in ValidCoins: {e}.")
            out = None

        return out


    def delete_coin(self,coinname=None,coinid=None):
        """
        DESC: Delete a valid coin
        INPUT: coin_id - Integer id
        NOTe:
        """
        #make sure the coin name is capitalized.
        coinname = coinname.capitalize()

        try:
            self.pgcur.execute(f"DELETE FROM validCoins WHERE CoinName='{coinname}' AND ID='{coinid}'")
            self.pgconn.commit()
        except Exception as e:
            print(e)
            logging.error(f'Could not delete the id: {e}.')
            self.pgconn.rollback()
            return {'coinname':coinname,'success':False}
        else:
            return {'coinname':coinname,'success':True}


    def add_portfolio(self,input_dict):
        """
        DESC:  a portfolio value and and the coins
        INPUT: input_dict - portfolio_name - name of the portfolio
        OUTPUT: out_dict - Name
                         - Success true/false
        """
        pname = str(input_dict['portfolio_name']).capitalize()
        out = {'portfolio_name': pname, 'success': False}

        try:
            sql = """
                INSERT INTO portfolios (PortfolioName)
                VALUES (%s)
                ON CONFLICT (PortfolioName) DO UPDATE
                SET PortfolioName = EXCLUDED.PortfolioName
            """
            self.pgcur.execute(sql, (pname,))
            self.pgconn.commit()

            out = {'portfolio_name': pname, 'success': True}

        except Exception as e:
            self.pgconn.rollback()
            print(e)
            logging.error(f'Could not write to the DB: {e}.')

        return out

    def get_portfolios(self):
        """
        DESC: List the available portfolios.
        Works
        """
        out = []
        try:
            sql = "SELECT ID, portfolioName FROM Portfolios"
            self.pgcur.execute(sql)
            rows = self.pgcur.fetchall()

            for row in rows:
                out.append({'id': row[0], 'portfolio_name': row[1]})

        except Exception as e:
            self.pgconn.rollback()
            print(e)
            logging.error(f"Could not list the Portfolios: {e}.")

        return out

    def delete_portfolio(self,name):
        """
        DESC: Delete a portfolio
        INPUT: name - name of the portfolio
        OUTPUT: out_dict - Name
                         - Success true/false
        """
        portfolioname = str(name).capitalize()
        out = {'portfolio_name': portfolioname, 'success': False}

        try:
            # Start a transaction block
            # 1. Delete portfolio coins
            self.pgcur.execute(
                "DELETE FROM portfolioCoins WHERE PortfolioName = %s",
                (portfolioname,)
            )

            # 2. Delete portfolio itself
            self.pgcur.execute(
                "DELETE FROM portfolios WHERE PortfolioName = %s",
                (portfolioname,)
            )

            # Commit both deletes as a single transaction
            self.pgconn.commit()

            out['success'] = True

        except Exception as e:
            self.pgconn.rollback()
            print(e)
            logging.error(f"Could not delete portfolio {portfolioname}: {e}")

        return out

    def add_portfolio_coin(self,input_dict):
        """
        DESC: Add a new coin to the portfolio.
        INPUT: input_dict - coinName
                          - portfolioName
        OUTPUT: out_dict - coinName
        NOTES: The portfolio must exsist in order to add coins to it.
        """
        portfolioname = str(input_dict['portfolioName']).capitalize()
        coinname = str(input_dict['coinName']).capitalize()
        out = {'coin_name': coinname, 'success': False}

        # Check if portfolio exists
        portfolio = self.get_portfolio(portfolioname)
        if not portfolio or not portfolio.get('success', False):
            logging.error(f"Could not find the portfolio: {portfolioname}.")
            return out

        try:
            sql = """
                INSERT INTO portfolioCoins (PortfolioName, CoinName)
                VALUES (%s, %s)
                ON CONFLICT (PortfolioName, CoinName)
                DO UPDATE SET CoinName = EXCLUDED.CoinName
            """
            self.pgcur.execute(sql, (portfolioname, coinname))
            self.pgconn.commit()
            out = {'coin_name': coinname, 'success': True}

        except Exception as e:
            self.pgconn.rollback()
            print(e)
            logging.error(f"Could not write to the DB: {e}.")

        return out

    def delete_portfolio_coin(self,input_dict):
        """
        DESC: Delete a coin from a portfolio
        INPUT: input_dict - coinName
                          - portfolioName
        OUTPUT: out_dict - Name
                         - Success true/false
        note: The portfolio must exsist in order to delete a coin
        """
        portfolioname = str(input_dict['portfolio_name']).capitalize()
        coinname = str(input_dict['coin_name']).capitalize()
        out = {'coin_name': coinname, 'success': False}

        # Check if portfolio exists
        portfolio = self.get_portfolio(portfolioname)
        if not portfolio or not portfolio.get('success', False):
            logging.error(f"Could not find the portfolio: {portfolioname}.")
            return out

        # Clear out the portfolio coins
        try:
            sql = "DELETE FROM portfolioCoins WHERE CoinName = %s AND PortfolioName = %s"
            self.pgcur.execute(sql, (coinname, portfolioname))
            self.pgconn.commit()
            out = {'coin_name': coinname, 'success': True}
        except Exception as e:
            print(e)
            logging.error(f"Could not delete coin from Portfolio: {e}.")
            self.pgconn.rollback()

        return out

    def get_portfolio(self,name):
        """
        DESC: Get a portfolio value and and the coins
        """
        portfolioname = str(name).capitalize()
        out = {'success': False, 'portfolio_name': None}

        try:
            sql = "SELECT ID, PortfolioName FROM portfolios WHERE PortfolioName = %s"
            self.pgcur.execute(sql, (portfolioname,))
            row = self.pgcur.fetchone()

            if row:
                out = {'success': True, 'portfolio_name': portfolioname}
            else:
                logging.warning(f"Portfolio {portfolioname} not found.")

        except Exception as e:
            self.pgconn.rollback()
            print(e)
            logging.error(f"Could not find {portfolioname} in Portfolios: {e}.")

        return out

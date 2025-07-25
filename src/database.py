import sqlite3
import psycopg2
import logging
import settings
import time

class Database:

    def __init__(self):
        try:
            self.connection = sqlite3.connect(settings.DB_PATH + "/crypto.db",check_same_thread=False)
            logging.info("Connected to the DB.")
        except Exception as e:
            logging.error(f"Could not connect to the DB: {e}.")
            raise e

        #check if the table is created. If not create it
        self.cursor = self.connection.cursor()
        #self.cursor.execute("CREATE TABLE if not exists cryptoHistory (ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT, coin TEXT, timestamp TEXT, price TEXT)")

        try:
            self.pgconn = psycopg2.connect(**settings.PG_CONFIG)
            logging.info("Connected to the PostgreSQL DB.")
        except Exception as e:
            logging.error(f"Could not create the cryptoHistory table: {e}.")
            raise e

        #establish a pgsql cursor
        self.pgcur = self.pgconn.cursor()

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

        for _, row in df.iterrows():
            try:
                self.pgcur.execute(
                    """INSERT INTO coinbase_ohlc (timestamp, symbol, open, high, low, close, volume, coinname, granularity)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (timestamp) DO NOTHING""", 
                    (row['timestamp'], ticker, row['open'], row['high'], row['low'], row['close'], row['volume'], coin_name, granularity)
                )
                self.pgconn.commit()
            except Exception as e:
                print(e)
                logging.error(f"Could not insert candles into the DB: {e}.")
                self.pgconn.rollback()

        #cur.close()
        #self.pgconn.close()
        return True

    def close_pg_connection(self):
        self.pgconn.close()
    
    def write_to_history(self,input_dict):

        try:
            #sql = "INSERT INTO cryptoHistory (coin,timestamp,price) VALUES (?,?,?)",({input_dict['coin']},{input_dict['timestamp']},{input_dict['price']})
            self.cursor.execute("INSERT INTO cryptoHistory (coin,timestamp,price) VALUES (?,?,?)",(input_dict['coin'],input_dict['timestamp'],input_dict['price']))
            self.connection.commit()
        except Exception as e:
            print(e)
            logging.error(f'Could not write to the DB: {e}.')
        else:
            self.connection.rollback()
        
        return True

    def add_coin(self,input_dict):
        """
        DESC: Add a valid coin to query
        INPUT: input_dict - coinname
                          - coinabv
                          - cointicker
        NOTe: {'CoinName': 'Bitcoin', 'CoinAbv':'btc','CoinTicker':'btc-usd'}
        """
        out = {'CoinName': None,'CoinAbv':None,'CoinTicker':None}
        coinname = str(input_dict['coinname']).capitalize()
        abv = str(input_dict['coinabv']).lower()
        ticker = str(input_dict['cointicker']).lower()

        try:
            self.cursor.execute("INSERT OR REPLACE INTO ValidCoins (CoinName,CoinAbv,CoinTicker) VALUES (?,?,?)",(coinname,abv,ticker))
            self.connection.commit()
            out = {'CoinName': coinname,'CoinAbv':abv,'CoinTicker':ticker}
        except Exception as e:
            print(e)
            logging.error(f'Could not write to the DB: {e}.')
        else:
            self.connection.rollback()
        
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
        try:
            self.cursor.execute("SELECT * FROM ValidCoins")
            rows = self.cursor.fetchall()
        except Exception as e:
            print(e)
            logging.error(f'Could not list the ValidCoins: {e}.')
        
        out = []
        for row in rows:
            out.append({'id':row[0],'coin_name':row[1],'coin_abv':row[2],'coin_ticker':row[3]})

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
        #make sure the coin name is capitalized.
        coinname = coinname.capitalize()

        try:
            self.cursor.execute(f"SELECT * FROM ValidCoins WHERE CoinName='{coinname}'")
            row = self.cursor.fetchone()
        except Exception as e:
            print(e)
            logging.error(f"Could not find {coinname} the ValidCoins: {e}.")
    
        out = {'index':row[0],'coin_name':row[1],'coin_abv':row[2],'coin_ticker':row[3]}

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
            self.cursor.execute(f"DELETE FROM ValidCoins WHERE CoinName='{coinname}' AND ID='{coinid}'")
            self.connection.commit()
        except Exception as e:
            print(e)
            logging.error(f'Could not delete the id: {e}.')
            self.connection.rollback()
            return {'coinname':coinname,'success':False}
        else:
            return {'coinname':coinname,'success':True}
    
    def trim_db(self,keep):
        """
        DESC: Keep only the entries greater than or equal to the keep variable
        EX: keep = 120minutes 60sec x 120min = 7200sec 
        Only entries less than or equal to 7200sec will be kept
        """
        keep_cutoff = int(time.time()) - int(keep) * 60
        
        try:
            self.cursor.execute("DELETE FROM cryptoHistory WHERE timestamp <= ?",(keep_cutoff,))
            self.connection.commit()
        except Exception as e:
            print(e)
            logging.error(f'Could not trim the timestamps: {e}.')
        else:
            self.connection.rollback()
        
        return True

    #Portfolio transactions

    def add_portfolio(self,input_dict):
        """
        DESC:  a portfolio value and and the coins
        INPUT: input_dict - portfolio_name - name of the portfolio
        OUTPUT: out_dict - Name
                         - Success true/false
        """
        pname = str(input_dict['portfolio_name']).capitalize()
        print(type(pname))
        out = {'portfolio_name': pname,'success': False}

        try:
            self.cursor.execute("INSERT OR REPLACE INTO Portfolios (PortfolioName) VALUES (?)",(pname,))
            self.connection.commit()
            out = {'portfolio_name': input_dict['portfolio_name'],'success':True}
        except Exception as e:
            print(e)
            logging.error(f'Could not write to the DB: {e}.')
        else:
            self.connection.rollback()

        return out

    def get_portfolios(self):
        """
        DESC: List the available portfolios.
        Works
        """
        out = []
        try:
            self.cursor.execute(f"SELECT * FROM Portfolios")
            rows = self.cursor.fetchall()
        except Exception as e:
            print(e)
            logging.error(f"Could not list the Portfolios: {e}.")
        
        for row in rows:
            out.append({'id':row[0],'portfolio_name':row[1]})

        return out

    def delete_portfolio(self,name):
        """
        DESC: Delete a portfolio
        INPUT: name - name of the portfolio
        OUTPUT: out_dict - Name
                         - Success true/false
        """
        portfolioname = str(name).capitalize()

        #clear out the portfolio coins
        try:
            self.cursor.execute(f"DELETE FROM PortfolioCoins WHERE PortfolioName='{portfolioname}'")
            self.connection.commit()
        except Exception as e:
            print(e)
            logging.error(f'Could not delete coin from Portfolio: {e}.')
            self.connection.rollback()
            return {'portfolio_name': portfolioname,'success': False}
        
        try:
            self.cursor.execute(f"DELETE FROM Portfolios WHERE PortfolioName='{portfolioname}'")
            self.connection.commit()
        except Exception as e:
            print(e)
            logging.error(f'Could not delete the Portfolio: {e}.')
            self.connection.rollback()
            return {'portfolio_name': portfolioname,'success': False}
        else:
            return {'portfolio_name': portfolioname,'success': True}

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
        out = {'coin_name': coinname,'success': False}

        if(self.get_portfolio(portfolioname)['Success'] != False):
            logging.error(f'Could not find the portfolio: {portfolioname}.')
            return out

        try:
            self.cursor.execute("INSERT OR REPLACE INTO PortfolioCoins (PortfolioName,CoinName) VALUES (?,?)",(portfolioname,coinname))
            self.connection.commit()
            out = {'coin_name': coinname,'success':True}
        except Exception as e:
            print(e)
            logging.error(f'Could not write to the DB: {e}.')
        else:
            self.connection.rollback()
        
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
        out = {'coin_name': coinname,'success': False}

        if(self.get_portfolio(portfolioname)['success'] != False):
            logging.error(f'Could not find the portfolio: {portfolioname}.')
            return out

        #clear out the portfolio coins
        try:
            self.cursor.execute(f"DELETE FROM PortfolioCoins WHERE CoinName='{coinname}' AND PortfolioName='{portfolioname}'")
            self.connection.commit()
            out = {'coin_name': portfolioname,'success': True}
        except Exception as e:
            print(e)
            logging.error(f'Could not delete coin from Portfolio: {e}.')
            self.connection.rollback()
        
        return out

    def get_portfolio(self,name):
        """
        DESC: Get a portfolio value and and the coins
        """
        portfolioname = str(name).capitalize()
        out = {'success':False,'portfolio_name':None}

        try:
            self.cursor.execute(f"SELECT * FROM Portfolios WHERE PortfolioName='{portfolioname}'")
            row = self.cursor.fetchall()
            print(row)
            out = {'success':True,'portfolio_name':portfolioname}
        except Exception as e:
            print(e)
            logging.error(f"Could not find {portfolioname} in Portfolios: {e}.")
        
        return out

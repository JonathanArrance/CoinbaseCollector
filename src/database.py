import sqlite3
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
            out.append({'index':row[0],'coin_name':row[1],'coin_abv':row[2],'coin_ticker':row[3]})

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
    
        return {'index':row[0],'coin_name':row[1],'coin_abv':row[2],'coin_ticker':row[3]}

    def delete_coin(self,coinname=None,coinid=None):
        """
        DESC: Delete a valid coin
        INPUT: coin_id - Integer id
        NOTe:
        """
        #make sure the coin name is capitalized.
        coinname = coinname.capitalize()

        try:
            self.cursor.execute(f"DELETE FROM ValidCoins WHERE CoinName='{coinname}'")
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
        INPUT: input_dict - portfolioname - name of the portfolio
        OUTPUT: out_dict - Name
                         - Success true/false
        """
        pname = str(input_dict['portfolioname']).capitalize()
        print(pname)
        out = {'PortfolioName': pname,'Success': False}

        #try:
        x = f"INSERT OR REPLACE INTO Portfolios (PortfolioName) VALUES ({pname})"
        print(x)
        self.cursor.execute(x)
        self.connection.commit()
        out = {'PortfolioName': pname,'Success':True}
        #except Exception as e:
        #    print(e)
        #    logging.error(f'Could not write to the DB: {e}.')
        #else:
        #    self.connection.rollback()
        
        return out

    def get_portfolios(self):
        """
        DESC: List the available portfolios.
        """
        try:
            self.cursor.execute(f"SELECT * FROM Portfolios")
            rows = self.cursor.fetchall()
        except Exception as e:
            print(e)
            logging.error(f"Could not list the Portfolios: {e}.")
        
        return rows

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
            return {'PortfolioName': portfolioname,'Success': False}
        
        try:
            self.cursor.execute(f"DELETE FROM Portfolios WHERE PortfolioName='{portfolioname}'")
            self.connection.commit()
        except Exception as e:
            print(e)
            logging.error(f'Could not delete the Portfolio: {e}.')
            self.connection.rollback()
            return {'PortfolioName': portfolioname,'Success': False}
        else:
            return {'PortfolioName': portfolioname,'Success': True}

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
        out = {'coinName': coinname,'success': False}

        if(self.get_portfolio(portfolioname)['Success'] != False):
            logging.error(f'Could not find the portfolio: {portfolioname}.')
            return out

        try:
            self.cursor.execute("INSERT OR REPLACE INTO PortfolioCoins (PortfolioName,CoinName) VALUES (?,?)",(portfolioname,coinname))
            self.connection.commit()
            out = {'coinName': coinname,'success':True}
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
        portfolioname = str(input_dict['portfolioName']).capitalize()
        coinname = str(input_dict['coinName']).capitalize()
        out = {'coinName': coinname,'success': False}

        if(self.get_portfolio(portfolioname)['Success'] != False):
            logging.error(f'Could not find the portfolio: {portfolioname}.')
            return out

        #clear out the portfolio coins
        try:
            self.cursor.execute(f"DELETE FROM PortfolioCoins WHERE CoinName='{coinname}' AND PortfolioName='{portfolioname}'")
            self.connection.commit()
            out = {'coinName': portfolioname,'success': True}
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
        out = {'success':False,'portfolio':None}

        try:
            self.cursor.execute(f"SELECT * FROM Portfolios WHERE PortfolioName='{portfolioname}'")
            row = self.cursor.fetchall()
            print(row)
            out = {'success':True,'portfolio':portfolioname}
        except Exception as e:
            print(e)
            logging.error(f"Could not find {portfolioname} in Portfolios: {e}.")
        
        return out

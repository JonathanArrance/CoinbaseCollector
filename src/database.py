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
            self.cursor.execute("INSERT INTO ValidCoins (CoinName,CoinAbv,CoinTicker) VALUES (?,?,?)",(coinname,abv,ticker))
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
            valid.append(str(coin[1]).lower())
        
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
            out.append({'index':row[0],'coinname':row[1],'coinabv':row[2],'cointicker':row[3]})

        return out
    
    def get_coin(self,coinname):
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

        return {'index':row[0],'coinname':row[1],'coinabv':row[2],'cointicker':row[3]}

    def delete_coin(self,coinname):
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



        

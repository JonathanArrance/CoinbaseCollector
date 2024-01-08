import sqlite3
import logging
import settings
import time

class Database:

    def __init__(self):
        try:
            self.connection = sqlite3.connect(settings.DB_PATH + "/crypto.db")
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
        INPUT: input_dict - CoinName
                          - CoinAbv
        NOTe: {'CoinName': 'Bitcoin', 'CoinAbv':'btc'}
        """
        try:
            self.cursor.execute("INSERT INTO ValidCoins (CoinName,CoinAbv) VALUES (?,?)",(input_dict['CoinName'],input_dict['CoinAbv']))
            self.connection.commit()
        except Exception as e:
            print(e)
            logging.error(f'Could not write to the DB: {e}.')
        else:
            self.connection.rollback()
        
        return True

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
        
        return rows

    def delete_coin(self,coin_id):
        """
        DESC: Delete a valid coin
        INPUT: coin_id - Integer id
        NOTe:
        """
        try:
            self.cursor.execute("DELETE FROM ValidCoins WHERE ID=?",(coin_id,))
            self.connection.commit()
        except Exception as e:
            print(e)
            logging.error(f'Could not delete the id: {e}.')
        else:
            self.connection.rollback()
        
        return True
    
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



        

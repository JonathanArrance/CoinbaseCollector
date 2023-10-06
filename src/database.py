import sqlite3
import logging
import settings

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
        self.cursor.execute("CREATE TABLE if not exists cryptoHistory (coin TEXT, timestamp TEXT, price TEXT)")

    def write_to_db(self,input_dict):

        try:
            #sql = "INSERT INTO cryptoHistory (coin,timestamp,price) VALUES (?,?,?)",({input_dict['coin']},{input_dict['timestamp']},{input_dict['price']})
            self.cursor.execute("INSERT INTO cryptoHistory (coin,timestamp,price) VALUES (?,?,?)",(input_dict['coin'],input_dict['timestamp'],input_dict['price']))
            self.connection.commit()
        except Exception as e:
            print(e)
            logging.error(f'Could not write to the DB: {e}.')
        else:
            self.connection.rollback()

    def trim_db(self,hours):
        #remove entries that are x hours old
        pass

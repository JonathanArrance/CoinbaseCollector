import os

#Coinbase
COINBASE_KEY = os.getenv('COINBASE_KEY',None)
COINBASE_INTERVAL = os.getenv('COINBASE_INTERVAL',2)
COINBASE_INTERVAL = int(COINBASE_INTERVAL)

TIMESERVER = os.getenv('TIMESERVER','pool.ntp.org')

APIVER = os.getenv('VALID_COINS','beta')
DB_PATH = os.getenv('DB_PATH','/db')

#What time of day to trim out the old entries 
TRIMOUT = os.getenv('TRIM',"23:30")
#how many minutes of data to keep when trimming
KEEP = os.getenv('KEEP',120)

#pgsql
PGSQL_HOST = os.getenv('PGSQL_HOST','localhost')
PGSQL_PORT = os.getenv('PGSQL_PORT',5432)
PGSQL_USER = os.getenv('PGSQL_USER','postgres')
PGSQL_PASSWORD = os.getenv('PGSQL_PASSWORD','postgres')
PGSQL_DB = os.getenv('PGSQL_DB','coinbase')

PG_CONFIG = {
    "dbname": PGSQL_DB,
    "user": PGSQL_USER,
    "password": PGSQL_PASSWORD,
    "host": PGSQL_HOST,
    "port": PGSQL_PORT
}
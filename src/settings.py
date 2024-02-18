import os

#Coinbase
COINBASE_KEY = os.getenv('COINBASE_KEY',None)
COINBASE_INTERVAL = os.getenv('COINBASE_INTERVAL',10)
COINBASE_INTERVAL = int(COINBASE_INTERVAL)

TIMESERVER = os.getenv('TIMESERVER','pool.ntp.org')

APIVER = os.getenv('VALID_COINS','beta')
DB_PATH = os.getenv('DB_PATH','/db')

#What time of day to trim out the old entries 
TRIMOUT = os.getenv('TRIM',"23:30")
#how many minutes of data to keep when trimming
KEEP = os.getenv('KEEP',120)
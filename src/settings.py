import os

TIMESERVER = os.getenv('COINBASE_INTERVAL','pool.ntp.org')

COINBASE_INTERVAL = os.getenv('COINBASE_INTERVAL',10)
COINBASE_INTERVAL = int(COINBASE_INTERVAL)

VALID_COINS = os.getenv('VALID_COINS',['etherium','bitcoin','chainlink','doge'])

APIVER = os.getenv('VALID_COINS','beta')

DB_PATH = os.getenv('DB_PATH','/db')

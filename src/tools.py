import time
import json
import settings
import logging
import requests
import ntptime

logging.basic(level=logging.basic)

def gettime():
    ntptime.host = settings.TIMESERVER
    ntptime.setttiem()
    print(f'Connected on {settings.TIMESERVER}')
    local = time.localtime()
    print(local)

def callurl(url):
    try:
        response = requests.get(url)
        logging.info(response)
    except Exception as e:
        log.error("something is wrong with the url call")
        log.error(e)

    data = json.loads(response)
    print(data)
    if not data:
        data = None

    return data

#!/bin/python
import settings
import logging
from crypto_lib import Crypto
#import random
#import hashlib
#import os

#API Stuff
from flask import Flask, abort, jsonify, request
from flask_restx import Api, Resource, reqparse
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

apiver = settings.APIVER

#Set flask to output "pretty print"
application = Flask(__name__)
application.secret_key = "arrance"
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
application.config['DEBUG'] = True
application.wsgi_app = ProxyFix(application.wsgi_app)

restxapi = Api(application,version=settings.APIVER, title='Action API',
    description='An API used to interact with Coinbase from Grafana.',)

#Enable logging
logging.basicConfig(level=logging.DEBUG)

parser = reqparse.RequestParser()

#create the namespaces
ns1 = restxapi.namespace('crypto/'+apiver, description='Crypto API endpoints')

cr = Crypto()

@ns1.route('/listcoins')
class CryptoPrice(Resource):
    #@auth.login_required
    def get(self,coin):
        pass

@ns1.route('/getcoin/<coin>')
class CryptoPrice(Resource):
    #@auth.login_required
    def get(self,coin):
        pass

@ns1.route('/sell/<coin>')
class CryptoPrice(Resource):
    #@auth.login_required
    def post(self,coin):
        pass

@ns1.route('/buy/<coin>')
class CryptoPrice(Resource):
    #@auth.login_required
    def post(self,coin):
        pass

@ns1.route('/addcoin/<coin>')
class CryptoPrice(Resource):
    #@auth.login_required
    def post(self,coin):
        pass

@ns1.route('/price/<coin>')
class CryptoPrice(Resource):
    #@auth.login_required
    def get(self,coin):
        price = '0.00'
        if coin.lower() not in settings.VALID_COINS:
            abort(404)
        elif coin.lower() == 'etherium':
            price = cr.get_eth_price()
        elif coin.lower() == 'bitcoin':
            price = cr.get_btc_price()
        elif coin.lower() == 'doge':
            price = cr.get_doge_price()
        else:
            abort(400)

        try:
            return jsonify(price['price'])
        except Exception as e:
            logging.error(e)
            abort(400)

if __name__ == '__main__':

    #application.run(host='0.0.0.0',port=9000, debug=True,ssl_context='adhoc)
    application.run(host='0.0.0.0',port=9030, debug=True)

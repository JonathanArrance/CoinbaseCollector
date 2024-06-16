#!/bin/python
import settings
import logging
import time
from crypto_lib import Crypto
from database import Database


#API Stuff
from flask import Flask, abort, jsonify, request
from flask_restx import Api, Resource, reqparse
from werkzeug.middleware.proxy_fix import ProxyFix
#from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

#Set flask to output "pretty print"
application = Flask(__name__)
application.secret_key = "arrance"
application.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
application.config['DEBUG'] = True
application.wsgi_app = ProxyFix(application.wsgi_app)

restxapi = Api(application,version=settings.APIVER, title='Crypto Action API',
    description='An API used to interact with Coinbase from Grafana and Prometheus.',)

#Enable logging
logging.basicConfig(level=logging.DEBUG)

#parser = reqparse.RequestParser()
#addport = reqparse.RequestParser()

#create the namespaces
ns1 = restxapi.namespace('coins/', description='Crypto coin API endpoints')
ns2 = restxapi.namespace('orders/', description='Crypto orders API endpoints')
ns3 = restxapi.namespace('portfolio/', description='Crypto portfolios')

cr = Crypto()
db = Database()

@ns1.route('/listcoins')
class ListCoins(Resource):
    #@auth.login_required
    def get(self):
        return jsonify(db.get_coins())
        
@ns1.route('/getcoin/<coin>')
class GetCoin(Resource):
    #@auth.login_required
    def get(self,coin):
        #Get the Coin info, current coin price, and history froom the db.
        return jsonify(db.get_coin(coin))

@ns1.route('/addcoin')
class AddCoin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('coinname', type=str, required=True, location='form',help='The full coin name.')
    parser.add_argument('coinabv', type=str,required=True, location='form',help='The coin abreviation. Ex Bitcoin, abriviation is btc.')
    parser.add_argument('cointicker', type=str, required=True, location='form',help='Coin ticker in Coinbase. Ex btc-usd')
    @restxapi.doc(parser=parser)
    
    #@auth.login_required
    def post(self):
        #args = parser.parse_args()
        args = AddCoin.parser.parse_args()
        try:
            return jsonify(db.add_coin(args))
        except Exception as e:
            logging.error(e)
            abort(400)

@ns1.route('/removecoin/<coin>')
class DeleteCoin(Resource):
    #@auth.login_required
    def delete(self,coin):
        #Get the Coin info, current coin price, and history froom the db.
        return jsonify(db.delete_coin(coin))

@ns1.route('/currentprice')
class CryptoPrice(Resource):
    #@auth.login_required
    def get(self):
        
        outs = db.get_coins()

        prices = []
        for out in outs:

            try:
                p = cr.get_coin_price(out)
                prices.append(p)
            except Exception as e:
                logging.error(e)
                abort(400)

        return jsonify(prices)

@ns3.route('/list')
class ListPortfolio(Resource):
    #@auth.login_required
    def get(self):
        return jsonify(db.get_portfolios())

@ns3.route('/get/<portfolio>')
class GetPortfolio(Resource):
    #@auth.login_required
    def get(self,portfolio):
        return jsonify(db.get_portfolio(portfolio))

@ns3.route('/addportfolio')
class AddPortfolio(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('portfolioname', type=str, required=True, location='form',help='New Portfolio name.')
    @restxapi.doc(parser=parser)
    
    #@auth.login_required
    def post(self):
        args = AddPortfolio.parser.parse_args()
        try:
            return jsonify(db.add_portfolio(args))
        except Exception as e:
            logging.error(e)
            abort(400)

@ns3.route('/removeportfolio')
class Portfolio(Resource):
    #@auth.login_required
    def delete(self):
        return "Not implemented"

@ns3.route('/<portfolio>/addcoin')
class Portfolio(Resource):
    #@auth.login_required
    def post(self):
        return "Not implemented"

@ns3.route('/<portfolio>/removecoin')
class Portfolio(Resource):
    #@auth.login_required
    def delete(self):
        return "Not implemented"


###########

@ns2.route('/marketsell/<coin>')
class SellCoin(Resource):
    #@auth.login_required
    def post(self,coin):
        return "Not implemented"

@ns2.route('/marketbuy/<coin>')
class BuyCoin(Resource):
    #@auth.login_required
    def post(self,coin):
        return "Not implemented"

@ns2.route('/limitsell/<coin>')
class LimitSellCoin(Resource):
    #@auth.login_required
    def post(self,coin):
        return "Not implemented"

@ns2.route('/limitbuy/<coin>')
class LimitBuyCoin(Resource):
    #@auth.login_required
    def post(self,coin):
        return "Not implemented"


if __name__ == '__main__':

    #application.run(host='0.0.0.0',port=9000, debug=True,ssl_context='adhoc)
    application.run(host='0.0.0.0',port=9030, debug=True)

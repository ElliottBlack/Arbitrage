from bs4 import BeautifulSoup
import requests
import json
import time
import datetime
from datetime import datetime
from binance.client import Client

from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

currencyPairs = ['ETH/BTC', 'LTC/BTC']

#bitbank stuff
bitbankURL = 'https://public.bitbank.cc'
bitbankPairs = ['eth_btc','ltc_btc']
bitbankPrices = [0,0]


#binance stuff
binanceURL = 'https://api.binance.com/api/v3/ticker/24hr'
binancePairs = ['ETHBTC','LTCBTC']
binancePrices = [0,0]


#binance API stuff
api_key = 'BUsTA1giVkpy30PDWbPbPCiw7Y3xdIdxiGGqjMPOj4NmOqAXrFbnd7uZXvCVmutD'
api_secret = 'wdeXGHantmL3vCeJO2CsnkpMcVaoDdr0oRUEkhI0QDmjl4XXFfKSkTSRDSMkL3tI'
client = Client(api_key, api_secret)

#arb stuff
arbRes = [0,0]

def bitbank():
		#get bitbankData
	i = 0
	for pair in bitbankPairs:
		response = requests.get(bitbankURL + '/' + pair + '/ticker')
		data = response.json()
		bitbankPrices[i] = float(data['data']['last'])
		i = i + 1

#get binace data
def binance():
	i = 0
	for pair in binancePairs:
		trades = client.get_recent_trades(symbol=pair,limit=1)
		binancePrices[i] = float(trades[0]['price'])
		i = i + 1

#arbitrage calculation
def arbCal():        
        for i in range(len(bitbankPrices)):
                x = (((binancePrices[i] - bitbankPrices[i]))/binancePrices[i]) 
                arbRes[i] = x*100

                

@app.route("/")
@app.route("/home")
def home():
	bitbank()
	binance()
	arbCal()
	return render_template('home.html', currencyPairs = currencyPairs, bitbankPrices = bitbankPrices, binancePrices = binancePrices, arbPer = arbRes)



if __name__ == '__main__':

	socketio.run(app, debug=True)

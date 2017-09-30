import urllib
import logging

import json

from flask import render_template

class Exchange:
    pass

def show_markets():
    print 'showing markets'
    exchange_names = ["BitfinexUSD",
                      "BitstampUSD",
                      "KrakenUSD",
                      "OKCoinCNY"]
    exchanges = get_exchanges(exchange_names)
    return render_template('exchanges.html',
                            exchanges=exchanges)

def get_exchanges(exchange_names):
    exchanges = []
    for iexchange in exchange_names:
        exchange = get_exchange(iexchange)
        exchanges.append(exchange)
    return exchanges

def get_exchange(exchange_name):
    res = urllib.urlopen('https://api.bitfinex.com/v1/book/btcusd')
    jsonstr = res.read().decode('utf8')
    try:
        raw_exchange = json.loads(jsonstr)
        exchange = raw_exchange.get('asks')
        if exchange:
            rexchange = Exchange()
            rexchange.name = exchange_name
            rexchange.cc = "BTC"
            rexchange.time = exchange[0].get('timestamp')
            rexchange.price = exchange[0].get('price')
            rexchange.currency = "USD"
            return rexchange
    except Exception:
        logging.error("%s - Can't parse json: %s" % (exchange_name, jsonstr))
        return None


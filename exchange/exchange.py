from flask import Flask, Response, session, render_template, request, url_for, redirect, abort

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
    return {"name":"XXX",
            "cc": "BTC",
            "time":"Now",
            "price":"2.00",
            "currency":"USD"}
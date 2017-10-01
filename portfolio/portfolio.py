from flask import render_template

class Portfolio:
    pass

def show_portfolio(userId):
    print 'showing portfolio for ' + userId
    portfolio = get_portfolio(userId)
    return render_template('portfolio.html',
                           portfolio=portfolio)

def get_portfolio(userId):
    portfolio = Portfolio()
    portfolio.name = userId
    portfolio.cc = "BTC"
    portfolio.balance = 101.0
    return portfolio
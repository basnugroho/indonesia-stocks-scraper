import pandas_datareader.data as web
import datetime
from flask import Flask
from flask import jsonify
import json
import pandas as pd

class FlaskStock:
    def __init__(self):
        self.file_path = "/Users/nugroho/basnugroho717@gmail.com drive/sahamin/rti/"

    def get_current_prices(self, stock_code):
        ticker = stock_code.upper() + ".JK"
        # start_date = datetime.datetime.today()
        end_date = datetime.datetime.today()
        try:
            prices = web.DataReader(ticker, 'yahoo', end_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
            dates = [datetime.datetime.fromtimestamp(date.tolist() / 1000000000).strftime('%Y-%m-%d') for date in
                     prices.index.values]
            histoPrices = {
                "dates": str(dates),
                "opens": str([round(price, 2) for price in prices["Open"].values]),
                "highs": str([round(price, 2) for price in prices["High"].values]),
                "lows": str([round(price, 2) for price in prices["Low"].values]),
                "closes": str([round(price, 2) for price in prices["Close"].values]),
                "adj_closes": str([round(price, 2) for price in prices["Adj Close"].values]),
                "volumes": str([round(price, 2) for price in prices["Volume"].values])
            }
            return histoPrices
        except:
            return str(f"cant't get the price {ticker}")

    def get_yesterday_close_price(self, stock_code):
        ticker = stock_code.upper() + ".JK"
        # start_date = datetime.datetime.today()
        end_date = datetime.datetime.today() - datetime.timedelta(1)
        try:
            prices = web.DataReader(ticker, 'yahoo', end_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
            dates = [datetime.datetime.fromtimestamp(date.tolist()/1000000000).strftime('%Y-%m-%d') for date in prices.index.values]
            histoPrices = {
                "dates": str(dates),
                "opens": str([round(price, 2) for price in prices["Open"].values]),
                "highs": str([round(price, 2) for price in prices["High"].values]),
                "lows": str([round(price, 2) for price in prices["Low"].values]),
                "closes": str([round(price, 2) for price in prices["Close"].values]),
                "adj_closes": str([round(price, 2) for price in prices["Adj Close"].values]),
                "volumes": str([round(price, 2) for price in prices["Volume"].values])
            }
            return histoPrices
        except:
            return str(f"cant't get the price {ticker}")

    def get_1W_close_prices(self, stock_code):
        ticker = stock_code.upper() + ".JK"
        start_date = datetime.datetime.today()
        end_date = datetime.datetime.today() - datetime.timedelta(5)
        try:
            prices = web.DataReader(ticker, 'yahoo', end_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d"))
            dates = [datetime.datetime.fromtimestamp(date.tolist()/1000000000).strftime('%Y-%m-%d') for date in prices.index.values]
            histoPrices = {
                "dates": str(dates),
                "opens": str([round(price, 2) for price in prices["Open"].values]),
                "highs": str([round(price, 2) for price in prices["High"].values]),
                "lows": str([round(price, 2) for price in prices["Low"].values]),
                "closes": str([round(price, 2) for price in prices["Close"].values]),
                "adj_closes": str([round(price, 2) for price in prices["Adj Close"].values]),
                "volumes": str([round(price, 2) for price in prices["Volume"].values])
            }
            return histoPrices
        except:
            return str(f"cant't get the price {ticker}")

    def get_1M_close_prices(self, stock_code):
        ticker = stock_code.upper() + ".JK"
        start_date = datetime.datetime.today()
        end_date = datetime.datetime.today() - datetime.timedelta(20)
        try:
            prices = web.DataReader(ticker, 'yahoo', end_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d"))
            dates = [datetime.datetime.fromtimestamp(date.tolist()/1000000000).strftime('%Y-%m-%d') for date in prices.index.values]
            histoPrices = {
                "dates": str(dates),
                "opens": str([round(price, 5) for price in prices["Open"].values]),
                "highs": str([round(price, 2) for price in prices["High"].values]),
                "lows": str([round(price, 2) for price in prices["Low"].values]),
                "closes": str([round(price, 2) for price in prices["Close"].values]),
                "adj_closes": str([round(price, 2) for price in prices["Adj Close"].values]),
                "volumes": str([round(price, 2) for price in prices["Volume"].values])
            }
            return histoPrices
        except:
            return str(f"cant't get the price {ticker}")

    def get_3M_close_prices(self, stock_code):
        ticker = stock_code.upper() + ".JK"
        start_date = datetime.datetime.today()
        end_date = datetime.datetime.today() - datetime.timedelta(20*3)
        try:
            prices = web.DataReader(ticker, 'yahoo', end_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d"))
            dates = [datetime.datetime.fromtimestamp(date.tolist()/1000000000).strftime('%Y-%m-%d') for date in prices.index.values]
            histoPrices = {
                "dates": str(dates),
                "opens": str([round(price, 5) for price in prices["Open"].values]),
                "highs": str([round(price, 2) for price in prices["High"].values]),
                "lows": str([round(price, 2) for price in prices["Low"].values]),
                "closes": str([round(price, 2) for price in prices["Close"].values]),
                "adj_closes": str([round(price, 2) for price in prices["Adj Close"].values]),
                "volumes": str([round(price, 2) for price in prices["Volume"].values])
            }
            return histoPrices
        except:
            return str(f"cant't get the price {ticker}")

    def get_6M_close_prices(self, stock_code):
        ticker = stock_code.upper() + ".JK"
        start_date = datetime.datetime.today()
        end_date = datetime.datetime.today() - datetime.timedelta(20*6)
        try:
            prices = web.DataReader(ticker, 'yahoo', end_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d"))
            dates = [datetime.datetime.fromtimestamp(date.tolist()/1000000000).strftime('%Y-%m-%d') for date in prices.index.values]
            histoPrices = {
                "dates": str(dates),
                "opens": str([round(price, 5) for price in prices["Open"].values]),
                "highs": str([round(price, 2) for price in prices["High"].values]),
                "lows": str([round(price, 2) for price in prices["Low"].values]),
                "closes": str([round(price, 2) for price in prices["Close"].values]),
                "adj_closes": str([round(price, 2) for price in prices["Adj Close"].values]),
                "volumes": str([round(price, 2) for price in prices["Volume"].values])
            }
            return histoPrices
        except:
            return str(f"cant't get the price {ticker}")

    def get_1Y_close_prices(self, stock_code):
        ticker = stock_code.upper() + ".JK"
        start_date = datetime.datetime.today()
        end_date = datetime.datetime.today() - datetime.timedelta(250)
        try:
            prices = web.DataReader(ticker, 'yahoo', end_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d"))
            dates = [datetime.datetime.fromtimestamp(date.tolist()/1000000000).strftime('%Y-%m-%d') for date in prices.index.values]
            histoPrices = {
                "dates": str(dates),
                "opens": str([round(price, 5) for price in prices["Open"].values]),
                "highs": str([round(price, 2) for price in prices["High"].values]),
                "lows": str([round(price, 2) for price in prices["Low"].values]),
                "closes": str([round(price, 2) for price in prices["Close"].values]),
                "adj_closes": str([round(price, 2) for price in prices["Adj Close"].values]),
                "volumes": str([round(price, 2) for price in prices["Volume"].values])
            }
            return histoPrices
        except:
            return str(f"cant't get the price {ticker}")

    def get_5Y_close_prices(self, stock_code):
        ticker = stock_code.upper() + ".JK"
        start_date = datetime.datetime.today()
        end_date = datetime.datetime.today() - datetime.timedelta(250*5)
        try:
            prices = web.DataReader(ticker, 'yahoo', end_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d"))
            dates = [datetime.datetime.fromtimestamp(date.tolist()/1000000000).strftime('%Y-%m-%d') for date in prices.index.values]
            histoPrices = {
                "dates": str(dates),
                "opens": str([round(price, 5) for price in prices["Open"].values]),
                "highs": str([round(price, 2) for price in prices["High"].values]),
                "lows": str([round(price, 2) for price in prices["Low"].values]),
                "closes": str([round(price, 2) for price in prices["Close"].values]),
                "adj_closes": str([round(price, 2) for price in prices["Adj Close"].values]),
                "volumes": str([round(price, 2) for price in prices["Volume"].values])
            }
            return histoPrices
        except:
            return str(f"cant't get the price {ticker}")

    def get_all_close_prices(self, stock_code):
        ticker = stock_code.upper() + ".JK"
        start_date = datetime.datetime.today()
        end_date = datetime.datetime.today() - datetime.timedelta(5000)
        try:
            prices = web.DataReader(ticker, 'yahoo', end_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d"))
            dates = [datetime.datetime.fromtimestamp(date.tolist()/1000000000).strftime('%Y-%m-%d') for date in prices.index.values]
            histoPrices = {
                "dates": str(dates),
                "opens": str([round(price, 5) for price in prices["Open"].values]),
                "highs": str([round(price, 2) for price in prices["High"].values]),
                "lows": str([round(price, 2) for price in prices["Low"].values]),
                "closes": str([round(price, 2) for price in prices["Close"].values]),
                "adj_closes": str([round(price, 2) for price in prices["Adj Close"].values]),
                "volumes": str([round(price, 2) for price in prices["Volume"].values])
            }
            return histoPrices
        except:
            return str(f"cant't get the price {ticker}")

fetcher = FlaskStock()
print(fetcher.get_1W_close_prices("UNVR"))

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'welcome to price fetcher API'

@app.route('/<stock_code>/')
def get_current_prices(stock_code):
    price = FlaskStock()
    data = price.get_current_prices(stock_code)
    message = {
        'status': 200,
        'message': 'OK',
        stock_code.upper(): data
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

@app.route('/<stock_code>/yest')
def get_yesterday_price(stock_code):
    price = FlaskStock()
    data = price.get_yesterday_close_price(stock_code)
    message = {
        'status': 200,
        'message': 'OK',
        stock_code.upper(): data
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

@app.route('/<stock_code>/1w')
def get_1w_close_prices(stock_code):
    price = FlaskStock()
    data = price.get_1W_close_prices(stock_code)
    message = {
        'status': 200,
        'message': 'OK',
        stock_code.upper(): data
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

@app.route('/<stock_code>/1m')
def get_1m_close_prices(stock_code):
    price = FlaskStock()
    data = price.get_1M_close_prices(stock_code)
    message = {
        'status': 200,
        'message': 'OK',
        stock_code.upper(): data
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

@app.route('/<stock_code>/3m')
def get_3m_close_prices(stock_code):
    price = FlaskStock()
    data = price.get_3M_close_prices(stock_code)
    message = {
        'status': 200,
        'message': 'OK',
        stock_code.upper(): data
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

@app.route('/<stock_code>/6m')
def get_6m_close_prices(stock_code):
    price = FlaskStock()
    data = price.get_6M_close_prices(stock_code)
    message = {
        'status': 200,
        'message': 'OK',
        stock_code.upper(): data
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

@app.route('/<stock_code>/1y')
def get_1y_close_prices(stock_code):
    price = FlaskStock()
    data = price.get_1Y_close_prices(stock_code)
    message = {
        'status': 200,
        'message': 'OK',
        stock_code.upper(): data
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

@app.route('/<stock_code>/5y')
def get_5Y_close_prices(stock_code):
    price = FlaskStock()
    data = price.get_5Y_close_prices(stock_code)
    message = {
        'status': 200,
        'message': 'OK',
        stock_code.upper(): data
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

@app.route('/<stock_code>/all')
def get_all_close_prices(stock_code):
    price = FlaskStock()
    data = price.get_all_close_prices(stock_code)
    message = {
        'status': 200,
        'message': 'OK',
        stock_code.upper(): data
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp

# stocks = pd.read_excel('/Users/nugroho/basnugroho717@gmail.com drive/sahamin/rti/daftar_saham.xlsx')
# stocks = pd.DataFrame(stocks)
#
# i = 0
# for stock in stocks["Kode"]:
#     print(fetcher.get_yesterday_close_price(stock))
#     i+=1
#     if i > 3:
#         break

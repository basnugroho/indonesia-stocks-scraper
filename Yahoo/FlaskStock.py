import pandas_datareader.data as web
import datetime
from flask import Flask
from flask import jsonify
import re
import json

app = Flask(__name__)

class FlaskStock:

    weekDays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

    def __init__(self):
        self.file_path = "/Users/nugroho/basnugroho717@gmail.com drive/sahamin/rti/"

    def get_current_prices(self, stock_code):
        ticker = stock_code.upper() + ".JK"
        shift_days = 0
        if datetime.datetime.today().weekday() == 5:
            shift_days = 1
        if datetime.datetime.today().weekday() == 6:
            shift_days = 1
        start_date = datetime.datetime.today() - datetime.timedelta(shift_days)
        try:
            prices = web.DataReader(ticker, 'yahoo', start_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d"))
            dates = [datetime.datetime.fromtimestamp(date.tolist()/1000000000).strftime('%Y-%m-%d') for date in prices.index.values]
            histoPrices = {
                "dates": str(dates),
                "opens": [round(price, 5) for price in prices["Open"].values],
                "highs": [round(price, 2) for price in prices["High"].values],
                "lows": [round(price, 2) for price in prices["Low"].values],
                "closes": [round(price, 2) for price in prices["Close"].values],
                "adj_closes": [round(price, 2) for price in prices["Adj Close"].values],
                "volumes": [round(price, 2) for price in prices["Volume"].values]
            }
            return histoPrices
        except:
            return str(f"cant't get the price {ticker}")


    def get_prices_history(self, stock_code, time):
        ticker = stock_code.upper() + ".JK"

        shift_days = 0
        if datetime.datetime.today().weekday() == 5:
            shift_days = 1
        if datetime.datetime.today().weekday() == 6:
            shift_days = 1

        start_date = datetime.datetime.today() - datetime.timedelta(shift_days)
        match = re.match(r"([0-9]+)([a-z]+)", time, re.I)
        if match:
            items = match.groups()
        if items[1]=="d":
            end_date = start_date - datetime.timedelta(int(items[0]))
        elif items[1]=="w":
            end_date = start_date - datetime.timedelta(int(items[0]) * 7)
        elif items[1]=="m":
            end_date = start_date - datetime.timedelta(int(items[0]) * 30)
        elif items[1] == "y":
            end_date = start_date - datetime.timedelta(int(items[0]) * 365)
        else:
            end_date = start_date - datetime.timedelta(25000)

        try:
            prices = web.DataReader(ticker, 'yahoo', end_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d"))
            dates = [datetime.datetime.fromtimestamp(date.tolist()/1000000000).strftime('%Y-%m-%d') for date in prices.index.values]
            histoPrices = {
                # "today": self.weekDays[datetime.datetime.today().weekday()],
                # "start_date": str(dates[0]),
                # "end_date": str(dates[-1]),
                "dates": str(dates),
                "opens": [round(price, 5) for price in prices["Open"].values],
                "highs": [round(price, 2) for price in prices["High"].values],
                "lows": [round(price, 2) for price in prices["Low"].values],
                "closes": [round(price, 2) for price in prices["Close"].values],
                "adj_closes": [round(price, 2) for price in prices["Adj Close"].values],
                "volumes": [round(price, 2) for price in prices["Volume"].values]
            }
            return histoPrices
        except:
            return str(f"cant't get the price {ticker}")

    def get_all_prices(self, stock_code):
        ticker = stock_code.upper() + ".JK"
        start_date = datetime.datetime.today()
        end_date = datetime.datetime.today() - datetime.timedelta(250*20)
        try:
            prices = web.DataReader(ticker, 'yahoo', end_date.strftime("%Y-%m-%d"), start_date.strftime("%Y-%m-%d"))
            dates = [datetime.datetime.fromtimestamp(date.tolist()/1000000000).strftime('%Y-%m-%d') for date in prices.index.values]
            histoPrices = {
                "start_date": str(dates[0]),
                "end_date": str(dates[-1]),
                "dates": str(dates),
                "opens": [round(price, 5) for price in prices["Open"].values],
                "highs": [round(price, 2) for price in prices["High"].values],
                "lows": [round(price, 2) for price in prices["Low"].values],
                "closes": [round(price, 2) for price in prices["Close"].values],
                "adj_closes": [round(price, 2) for price in prices["Adj Close"].values],
                "volumes": [round(price, 2) for price in prices["Volume"].values]
            }
            return histoPrices
        except:
            return str(f"cant't get the price {ticker}")

@app.route('/')
def welcome():
    return 'welcome to price fetcher API'

@app.route('/<stock_code>/')
def get_current_prices(stock_code):
    price = FlaskStock()
    data = price.get_current_prices(stock_code)
    return json.dumps(data)

@app.route('/<stock_code>/<time>')
def get_prices_history(stock_code, time):
    price = FlaskStock()
    data = price.get_prices_history(stock_code, time)
    return json.dumps(data)

@app.route('/<stock_code>/all')
def get_all_prices(stock_code):
    price = FlaskStock()
    data = price.get_all_prices(stock_code)
    return json.dumps(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

# run it
# export FLASK_APP=FlaskStock.py
# export FLASK_ENV=development
# python -m flask run
# flask run --host=0.0.0.0

import pandas_datareader.data as web
import datetime
import pandas as pd

class Price_Fetcher:
    def __init__(self):
        self.file_path = "/Users/nugroho/Google Drive/sahamin/rti"

    def get_yesterday_close_price(self, symbol):
        ticker = symbol.upper()+".JK"
        yesterday = datetime.datetime.today() - datetime.timedelta(1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        try:
            prices = web.DataReader(ticker, 'yahoo', yesterday_str, yesterday_str)
            return prices["Adj Close"].values[0]
        except:
            return 0
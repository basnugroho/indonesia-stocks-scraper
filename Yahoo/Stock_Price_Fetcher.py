import pandas_datareader.data as web
import datetime
import pandas as pd

class Price_Fetcher:
    def __init__(self):
        self.file_path = "/Users/nugroho/basnugroho717@gmail.com drive/sahamin/rti/"

    def get_yesterday_close_price(self, symbol):
        ticker = symbol.upper()+".JK"
        yesterday = datetime.datetime.today() - datetime.timedelta(1)
        yesterday_str = yesterday.strftime("%Y-%m-%d")
        try:
            prices = web.DataReader(ticker, 'yahoo', yesterday_str, yesterday_str)
            return prices["Adj Close"].values[0]
        except:
            return 0

# fetcher = Stock_Price_Fetcher()
#
# stocks = pd.read_excel('/Users/nugroho/basnugroho717@gmail.com drive/sahamin/rti/daftar_saham.xlsx')
# stocks = pd.DataFrame(stocks)
#
# i = 0
# for stock in stocks["Kode"]:
#     print(fetcher.get_yesterday_close_price(stock))
#     i+=1
#     if i > 3:
#         break

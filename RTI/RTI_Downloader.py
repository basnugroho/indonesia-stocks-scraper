from selenium import webdriver
from time import  sleep
import os
import pandas as pd
from Scrapers.RTI.RTI_Reader import RTI_Reader
from bs4 import BeautifulSoup
import requests
import re
import zipfile

class Downloader:
    def __init__(self,
                 ending_period = "31-Mar-2019",
                 force_download = False,
                 download_path = '/Users/nugroho/basnugroho717@gmail.com drive/sahamin/rti',
                 target_url = 'https://analytics2.rti.co.id/?m_id=1&sub_m=s2&sub_sub_m=3',
                 driver = webdriver.Chrome('/Users/nugroho/basnugroho717@gmail.com drive/sahamin/chromedriver')):
        self.download_path = download_path
        self.target_url = target_url
        self.driver = driver
        self.stock_code = ""
        self.period = ""
        self.fin_part = ""
        self.file_exist = False
        self.empty_stocks = []
        self.download_attempt = 1
        self.values = ""
        self.force_download = force_download
        self.ending_period = ending_period

    def load_stock(self, stock_code, period="annual", fin_part="income_statement"):
        self.stock_code = stock_code.upper()
        self.fin_part = fin_part.lower()
        self.period = period.lower()

        if self.force_download:
            print(f"[Force Download Mode] downloading {self.stock_code}.html")
            self.submit_stock(stock_code=self.stock_code, fin_part=self.fin_part, period=self.period)
            self.download_page_source()

        # check the file
        if self.is_file_exist(stock_code=stock_code, period=period, fin_part=fin_part)==True:
            print(f"{self.stock_code}.html in {self.ending_period} {self.fin_part} ({self.period}) already exist!")

            while self.is_values_empty(index=0): # last index in file empty? check and re-download
                print(f"{self.stock_code}.html in {self.ending_period} {self.fin_part} ({self.period}) is empty!")
                self.re_download_page_source(self.download_attempt)
                self.download_attempt += 1
                if self.download_attempt > 3:
                    self.empty_stocks.append(stock_code)
                    print(f"{stock_code} download attempt more than 3, move on to the next stock")
                    self.download_attempt = 1
                    break
            if self.is_values_empty(index=0) == False: # file checked has values
                print(f"{self.stock_code}.html in {self.ending_period} {self.fin_part} ({self.period}) has values!")
                self.download_attempt = 1
                # continue to the next stock
        else: # file not exist yet then download
            print(f"{self.stock_code}.html in {self.ending_period} {self.fin_part} ({self.period}) not exist!")
            self.submit_stock(stock_code=self.stock_code, fin_part=self.fin_part, period=self.period)
            self.download_page_source()
            # for check value
            self.load_stock(self.stock_code, period=self.period, fin_part=self.fin_part)

    def submit_stock(self, stock_code, fin_part, period):
        self.stock_code = stock_code.upper()
        self.fin_part = fin_part.lower()
        self.period = period.lower()

        self.open_target_url()
        code_form = self.driver.find_element_by_xpath('//input[@name="codefld2"]')  # input code saham
        sleep(1)  # butuh di pause kadang ngetik gak lengkap keburu di submit
        code_form.send_keys(self.stock_code)  # isi code saham
        self.driver.find_element_by_xpath('//input[@id="go"]').click()  # klik button Go
        if self.fin_part == "balance_sheet":
            self.driver.find_element_by_xpath('//a[@id="fm1"]').click()  # klik balance sheet
        elif self.fin_part == "cash_flow":
            self.driver.find_element_by_xpath('//a[@id="fm3"]').click()  # klik cash flow
        else:
            self.driver.find_element_by_xpath('//a[@id="fm2"]').click()  # klik income statement
        sleep(1)
        if (self.period == "annual"):
            self.driver.find_element_by_xpath('//a[@id="fin_prd1"]').click()  # klik annual
        else:
            self.driver.find_element_by_xpath('//a[@id="fin_prd3"]').click()  # klik quarter

    def open_target_url(self):
        self.driver.get(self.target_url)

    def close_browser(self):
        self.driver.close()
        print("browser closed")

    def download_page_source(self):
        try:
            # print("preparing download place. . .")
            if self.period.lower() == "annual":
                if self.fin_part == "balance_sheet":
                    file = open(self.download_path +'/balance_sheet/'+self.ending_period+'/annual/' + self.stock_code + '.html',
                                'w', encoding='utf-8')
                elif self.fin_part == "cash_flow":
                    file = open(self.download_path +'/cash_flow/'+self.ending_period+'/annual/' + self.stock_code + '.html',
                                'w', encoding='utf-8')
                else:
                    file = open(self.download_path +'/income_statement/'+self.ending_period+'/annual/' + self.stock_code + '.html',
                                'w', encoding='utf-8')
            else:
                if self.fin_part == "balance_sheet":
                    file = open(self.download_path +'/balance_sheet/'+self.ending_period+'/quarter/' + self.stock_code + '.html',
                                'w', encoding='utf-8')
                elif self.fin_part == "cash_flow":
                    file = open(self.download_path +'/cash_flow/'+self.ending_period+'/quarter/' + self.stock_code + '.html',
                                'w', encoding='utf-8')
                else:
                    file = open(self.download_path +'/income_statement/'+self.ending_period+'/quarter/' + self.stock_code + '.html',
                                'w', encoding='utf-8')

            # print(f"downloading {self.stock_code} page source from {self.driver.current_url}")
            file.write(self.driver.page_source)
            file.close()
        except NameError:
            print(f"{self.stock_code}.html write file error: {NameError}")

    def re_download_page_source(self, attemp):
        print(f"re-download {self.stock_code} in {self.fin_part} ({self.period}) attempts {(attemp)}")
        self.submit_stock()
        if attemp <= 3:
            sleep(attemp)
        else:
            sleep(3)
        self.download_page_source()

    def is_values_empty(self, index):
        reader = RTI_Reader()
        if self.fin_part == "income_statement":
            try:
                value = reader.extract_income_statement(self.stock_code, self.period)
                self.values = value
                if (value["total_sales"][index]==None) and value["net_income"][index]==None:
                    print(value)
                    return True
                else:
                    return False
            except NameError:
                print("error:" +NameError)
        elif self.fin_part == "balance_sheet":
            try:
                value = reader.extract_balance_sheet(self.stock_code, self.period)
                if (value["current_assets"]["cash_and_cash_equivalents"][index]==None and
                    value["total_assets"][index]==None and value["total_liabilities"]==None):
                    print(value)
                    return True
                else:
                    return False
            except NameError:
                print("error:" +NameError)
        elif self.fin_part == "cash_flow":
            try:
                value = reader.extract_cash_flow(self.stock_code, self.period)
                if (value["cash_flow_from_operating_activities"][index]==None and
                value["cash_flow_from_investing_activities"][index]==None and
                value["cash_flow_from_financing_activities"][index]==None):
                    print(value)
                    return True
                else:
                    return False
            except NameError:
                print("error:" +NameError)
        else:
            return False

    def is_file_exist(self, stock_code, period, fin_part):
        self.stock_code = stock_code
        self.period = period
        self.fin_part = fin_part

        if self.period.lower() == "annual":
            if self.fin_part == "balance_sheet":
                file_exist = os.path.isfile(
                    self.download_path +'/balance_sheet/'+self.ending_period+'/annual/' + self.stock_code + '.html')
            elif self.fin_part == "cash_flow":
                file_exist = os.path.isfile(
                    self.download_path +'/cash_flow/'+self.ending_period+'/annual/' + self.stock_code + '.html')
            else:
                file_exist = os.path.isfile(
                    self.download_path +'/income_statement/'+self.ending_period+'/annual/' + self.stock_code + '.html')
        else:
            if self.fin_part == "balance_sheet":
                file_exist = os.path.isfile(
                    self.download_path +'/balance_sheet/'+self.ending_period+'/quarter/' + self.stock_code + '.html')
            elif self.fin_part == "cash_flow":
                file_exist = os.path.isfile(
                    self.download_path +'/cash_flow/'+self.ending_period+'/quarter/' + self.stock_code + '.html')
            else:
                file_exist = os.path.isfile(
                    self.download_path +'/income_statement/'+self.ending_period+'/quarter/' + self.stock_code + '.html')

        self.file_exist = file_exist
        if file_exist:
            return True
        else:
            return False

if __name__ == '__main__':
    dl = Downloader()
    dl.open_target_url()

    stocks = pd.read_excel(dl.download_path + '/daftar_saham.xlsx')
    stocks = pd.DataFrame(stocks)
    for stock in stocks["Kode"]:
        dl.load_stock(stock_code=stock, period="annual", fin_part="income_statement")
        # dl.load_stock(stock_code=stock,period="annual",fin_part="balance_sheet")
        # dl.load_stock(stock_code=stock, period="annual", fin_part="cash_flow")
        #
        # dl.load_stock(stock_code=stock, period="quarter", fin_part="income_statement")
        # dl.load_stock(stock_code=stock,period="quarter",fin_part="balance_sheet")
        # dl.load_stock(stock_code=stock, period="quarter", fin_part="cash_flow")
    #dl.close_browser()
    dl.empty_stocks

    # single download test
    # dl = Downloader()
    # dl.open_target_url()
    # dl.load_stock(stock_code="CKRA", period="annual", fin_part="income_statement")
    # reader = RTI_Reader(all=False, read_online=False)
    # # print(reader.extract_income_statement(stock_code=dl.stock_code, period=dl.period))
    # if dl.is_values_empty(0):
    #     print(f"{dl.stock_code} is empty")
    # else:
    #     print(dl.values)
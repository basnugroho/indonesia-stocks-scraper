from bs4 import BeautifulSoup
import json
import requests
import pandas as pd
import datetime
from Yahoo import Stock_Price_Fetcher

class RTI_Reader:
    def __init__(self,
                 all=True,
                 read_online=False,
                 ending_period = "31-Mar-2019",
                 file_path="/Users/nugroho/Google Drive/sahamin/rti",
                 target_url = 'https://analytics2.rti.co.id/?m_id=1&sub_m=s2&sub_sub_m=3'):

        self.file_path = file_path
        self.read_online  = read_online
        self.target_url = target_url
        # self.driver = driver
        self.fin_part = ""
        self.period = ""
        self.stock_code = ""
        self.all = all
        self.ending_period = ending_period
        self.write_json_fails = []

    def ipo_str_to_date(self, datestr):
        year = datestr.rsplit(' ', 1)[-1]
        str_month = datestr.rsplit(' ', 1)[-2].rsplit(' ', 1)[-1]
        day = datestr.rsplit(' ', 1)[-2].rsplit(' ', 1)[-2]

        if str_month == "Jan":
            str_month = "01"
        elif str_month == "Feb":
            str_month = "02"
        elif str_month == "Mar":
            str_month = "03"
        elif str_month == "Apr":
            str_month = "04"
        elif str_month == "Mei":
            str_month = "05"
        elif str_month == "Jun":
            str_month = "06"
        elif str_month == "Jul":
            str_month = "07"
        elif str_month == "Ags":
            str_month = "08"
        elif str_month == "Sep":
            str_month = "09"
        elif str_month == "Okt":
            str_month = "10"
        elif str_month == "Nov":
            str_month = "11"
        else:
            str_month = "12"

        str_date = year + " " + str_month + " " + day

        return datetime.datetime.strptime(str_date, '%Y %m %d').strftime('%Y-%m-%d')

    def extract_general_info(self, stock_code):
        stocks = pd.read_excel(self.file_path + '/daftar_saham.xlsx')
        stocks = pd.DataFrame(stocks)

        self.fin_part = "income_statement"
        self.period = "annual"
        self.stock_code = stock_code
        date_str = stocks.loc[stocks['Kode'] == stock_code]['Tanggal Pencatatan'].to_string(index=False)
        fetcher = Stock_Price_Fetcher.Price_Fetcher()


        soup = BeautifulSoup(self.read_file(), 'lxml')
        general = {
            "stock_code": stock_code,
            "name": stocks.loc[stocks['Kode'] == stock_code]['Nama'].to_string(index=False).lstrip(),
            "price": float(fetcher.get_yesterday_close_price(self.stock_code)),
            "currency": self.get_currency(soup),
            "listed_date": self.ipo_str_to_date(date_str),
            "share": int(stocks.loc[stocks['Kode'] == stock_code]['Saham'].to_string(index=False)),
            "papan_pencatatan": stocks.loc[stocks['Kode'] == stock_code]['Papan Pencatatan'].to_string(index=False).lstrip(),
        }
        return general

    def extract_income_statement(self, stock_code, period):
        self.fin_part = "income_statement"
        self.period = period
        self.stock_code = stock_code

        soup = BeautifulSoup(self.read_file(), 'lxml')
        if self.read_online:
            soup = BeautifulSoup(self.read_file(), 'html.parser')

        income_statement = {
            "stock_code": stock_code,
            "years": list(map(self.get_year,self.get_ending_periods(soup))),
            "quarters": list(map(self.get_quarter,self.get_ending_periods(soup))),
            "total_sales": self.get_values_number(soup, "r2c"),
            "cost_of_good_sold": self.get_values_number(soup, "r3c"),
            "gross_profit": self.get_values_number(soup, "r4c"),
            "operating_expenses": {
                "sales_and_marketing_expenses": self.get_values_number(soup, "r5c"),
                "administrative_expenses": self.get_values_number(soup, "r6c"),
                "other_operating_expenses": self.get_values_number(soup, "r7c"),
            },
            "total_operating_expenses": self.get_values_number(soup, "r8c"),
            "operating_income": self.get_values_number(soup, "r9c"),
            "other_income_and_expenses": {
                "interest_income": self.get_values_number(soup, "r10c"),
                "interest_expense": self.get_values_number(soup, "r11c"),
                "foreign_exchange_gain_loss": self.get_values_number(soup, "r12c"),
                "gain_loss_on_sale_of_assets": self.get_values_number(soup, "r13c"),
                "other_items": self.get_values_number(soup, "r14c"),
            },
            "total_other_income_and_expenses": self.get_values_number(soup, "r15c"),
            "income_before_tax": self.get_values_number(soup, "r16c"),
            "income_tax_expenses": self.get_values_number(soup, "r17c"),
            "income_from_normal_operations": self.get_values_number(soup, "r18c"),
            "extraordinary_items": self.get_values_number(soup, "r19c"),
            "minority_int_in_net_earnings": self.get_values_number(soup, "r20c"),
            "net_income": self.get_values_number(soup, "r21c"),
            "net_income_attributable_to": {
                "equity_holders_of_the_company": self.get_values_number(soup, "r22c"),
                "non_controlling_interest": self.get_values_number(soup, "r23c"),
                "total_net_income_attributable_to": self.get_values_number(soup, "r23c"),
            },
            "earning_per_share": self.get_values_number(soup, "r25c"),
            "diluted_earnings_per_share": self.get_values_number(soup, "r26c"),
            "comprehensive_income": {
                "net_income": self.get_values_number(soup, "r27c"),
                "other_comprehensive_income": self.get_values_number(soup, "r28c"),
            },
            "total_comprehensive_income": self.get_values_number(soup, "r29c"),
            "comprehensive_income_attributable_to": {
                "equity_holders_of_the_company": self.get_values_number(soup, "r30c"),
                "non_controlling_interest": self.get_values_number(soup, "r31c"),
                "total_comprehensive_income_attributable_to": self.get_values_number(soup, "r32c"),
            }
        }

        return income_statement

    def extract_balance_sheet(self, stock_code, period):
        self.fin_part = "balance_sheet"
        self.period = period
        self.stock_code = stock_code

        soup = BeautifulSoup(self.read_file(), 'lxml')

        balance_sheet = {
            "stock_code": self.stock_code,
            "years": list(map(self.get_year,self.get_ending_periods(soup))),
            "quarters": list(map(self.get_quarter,self.get_ending_periods(soup))),
            "current_assets": {
                "cash_and_cash_equivalents": self.get_values_number(soup, "r2c"),
                "net_receivables": self.get_values_number(soup, "r3c"),
                "inventory": self.get_values_number(soup, "r4c"),
                "prepaid_expenses": self.get_values_number(soup, "r5c"),
                "other_current_assets": self.get_values_number(soup, "r6c"),
            },
            "total_current_assets": self.get_values_number(soup, "r7c"),
            "deferred_tax_assets": self.get_values_number(soup, "r8c"),
            "longterm_assets": {
                "property_plant_equipment": self.get_values_number(soup, "r9c"),
                "goodwill": self.get_values_number(soup, "r10c"),
                "intangible_assets": self.get_values_number(soup, "r11c"),
                "other_assets": self.get_values_number(soup, "r12c")
            },
            "total_longterm_assets": self.get_values_number(soup, "r13c"),
            "total_assets": self.get_values_number(soup, "r14c"),
            "current_liabilities": {
                "account_payables": self.get_values_number(soup, "r15c"),
                "short_term_debt": self.get_values_number(soup, "r16c"),
                "other_current_liabilities": self.get_values_number(soup, "r17c")
            },
            "total_current_liabilities": self.get_values_number(soup, "r18c"),
            "deferred_tax_liabilities": self.get_values_number(soup, "r19c"),
            "longterm_liabilities": self.get_values_number(soup, "r20c"),
            "total_liabilities": self.get_values_number(soup, "r21c"),
            "minority_interest": self.get_values_number(soup, "r22c"),
            "stockholders_equity": {
                "common_stock": self.get_values_number(soup, "r23c"),
                "paid_in_capital": self.get_values_number(soup, "r24c"),
                "retained_earnings_(deficit)": self.get_values_number(soup, "r25c"),
                "other_stockholders_equity": self.get_values_number(soup, "r26c"),
                "non_controlling_interest_(effective_2011)": self.get_values_number(soup, "r27c"),
            },
            "total_stockholders_equity": self.get_values_number(soup, "r28c"),
            "total_liabilities_and_stockholders_equity": self.get_values_number(soup, "r29c")
        }
        return balance_sheet

    def extract_cash_flow(self, stock_code, period):
        self.fin_part = "cash_flow"
        self.period = period
        self.stock_code = stock_code

        soup = BeautifulSoup(self.read_file(), 'lxml')
        cash_flow = {
            "stock_code": stock_code,
            "years": list(map(self.get_year,self.get_ending_periods(soup))),
            "quarters": list(map(self.get_quarter,self.get_ending_periods(soup))),
            "operating_activities": {
                "cash_from_customers": self.get_values_number(soup,"r2c"),
                "payments_for_operating_activities": self.get_values_number(soup,"r3c"),
                "other_operating_activities": self.get_values_number(soup,"r4c")
            },
            "cash_flow_from_operating_activities": self.get_values_number(soup,"r5c"),
            "investing_activities": {
                "capital_expenditures": self.get_values_number(soup,"r6c"),
                "other_investing_activities": self.get_values_number(soup,"r7c")
            },
            "cash_flow_from_investing_activities": self.get_values_number(soup,"r8c"),
            "financing_activities": {
                "additional_paid_in_capital": self.get_values_number(soup,"r9c"),
                "financing_activities_(related_party)": self.get_values_number(soup,"r10c"),
                "dividends_paid": self.get_values_number(soup,"r11c"),
                "other_financing_activities": self.get_values_number(soup,"r12c")
            },
            "cash_flow_from_financing_activities": self.get_values_number(soup,"r13c"),
            "net_increase_decrease_in_cash_flow": self.get_values_number(soup,"r14c"),
            "cash_at_the_beginning_of_the_period": self.get_values_number(soup,"r15c"),
            "effect_of_exchange_rate_changes": self.get_values_number(soup,"r16c"),
            "cash_at_the_end_of_the_period": self.get_values_number(soup,"r17c")
        }
        return cash_flow

    def extract_ratios(self, stock_code):
        self.fin_part = "income_statement"
        self.period = "annual"
        self.stock_code = stock_code

        soup = BeautifulSoup(self.read_file(), 'lxml')
        ratios = {
            "stock_code": stock_code,
            "years": list(map(self.get_year,self.get_ending_periods(soup))),
            "quarters": list(map(self.get_quarter,self.get_ending_periods(soup))),
            "eps": self.get_values_number(soup, "r25c"),
            "per": [],
            "dps": [],
            "div_yield": [],
            "npm": [],
            "roe": [],
            "pbv": []
        }

        return ratios

    def read_file(self):
        if self.read_online:
            response = requests.get(self.target_url)
            data = response.text.read()
            data.close()
            return data
        else:
            file = open(self.file_path + "/" + self.fin_part + "/" + self.ending_period + "/" + self.period + "/" + self.stock_code + ".html")
            data = file.read()
            file.close()
            return data

    def remove_number_format(self, item):
        if item!="":
            if self.is_number(item):
                return float(item)
            if item != "-":
                item = item.replace(' M', '')
                return float(item.replace(',', ''))
            else:
                return None

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    def get_year(self, item):
        if item != "":
            return int(item.rsplit('-', 1)[-1])
        else:
            return None

    def get_quarter(self, item):
        if item!="":
            if item.rsplit('-', 1)[-2].rsplit('-', 1)[-1] == "Mar":
                return 1
            elif item.rsplit('-', 1)[-2].rsplit('-', 1)[-1] == "Jun":
                return 2
            elif item.rsplit('-', 1)[-2].rsplit('-', 1)[-1] == "Sep":
                return 3
            elif item.rsplit('-', 1)[-2].rsplit('-', 1)[-1] == "Dec":
                return 4
            else:
                return 4

    def get_currency(self, soup):
        curr = soup.find(attrs={'id': 'prd'}).text
        if curr == "\xa0 (in Rp)":
            return "IDR"
        else:
            return "USD"

    def get_ending_periods(self, soup):
        ending_periods = []

        if self.all:
            if self.period == "annual": end_num = 7;
            else: end_num = 6;

            for i in range(1, end_num):
                ending_periods.append(soup.find(attrs={'id': 'r1c' + str(i)}).text)
        else:
            ending_periods.append(soup.find(attrs={'id': 'r1c' + str(1)}).text)
        return ending_periods

    def get_values_number(self, soup, attribute_id):
        items = []

        if self.period == "annual": end_num = 7;
        else: end_num = 6;

        if self.all == True:
            for i in range(1, end_num):
                items.append(soup.find(attrs={'id': attribute_id + str(i)}).text)
            items = map(self.remove_number_format, items)
        else:
            items.append(soup.find(attrs={'id': attribute_id + str(1)}).text)
            items = map(self.remove_number_format, items)
        return list(items)

    def write_json(self, stock_code):
        self.stock_code = stock_code
        # soup = BeautifulSoup(self.read_file(), 'lxml')
        if self.all==False:
            try:
                with open(self.file_path + "/json/" +self.ending_period+'-last/'+self.stock_code +'_general_'+self.ending_period+'.json',
                          'w') as outfile:
                    json.dump(self.extract_general_info(stock_code=self.stock_code), outfile, indent=4)
                    outfile.close()
                with open(self.file_path + "/json/" +self.ending_period+'-last/'+self.stock_code +'_income_statements_quarter_'+self.ending_period+'.json',
                          'w') as outfile:
                    json.dump(self.extract_income_statement(stock_code=self.stock_code, period="quarter"), outfile, indent=4)
                    outfile.close()
                with open(self.file_path + "/json/" +self.ending_period+'-last/'+self.stock_code +'_income_statements_annual_'+self.ending_period+'.json',
                          'w') as outfile:
                    json.dump(self.extract_income_statement(stock_code=self.stock_code, period="annual"), outfile, indent=4)
                    outfile.close()
                with open(self.file_path + "/json/" +self.ending_period+'-last/'+self.stock_code +'_balance_sheets_quarter_'+self.ending_period+'.json',
                          'w') as outfile:
                    json.dump(self.extract_balance_sheet(stock_code=self.stock_code, period="quarter"), outfile, indent=4)
                    outfile.close()
                with open(self.file_path + "/json/" +self.ending_period+'-last/'+self.stock_code +'_balance_sheets_annual_'+self.ending_period+'.json',
                          'w') as outfile:
                    json.dump(self.extract_balance_sheet(stock_code=self.stock_code, period="annual"), outfile, indent=4)
                    outfile.close()
                with open(self.file_path + "/json/" +self.ending_period+'-last/'+self.stock_code +'_cash_flows_quarter_'+self.ending_period+'.json',
                          'w') as outfile:
                    json.dump(self.extract_cash_flow(stock_code=self.stock_code, period="quarter"), outfile, indent=4)
                    outfile.close()
                with open(self.file_path + "/json/" +self.ending_period+'-last/'+self.stock_code +'_cash_flows_annual_'+self.ending_period+'.json',
                          'w') as outfile:
                    json.dump(self.extract_cash_flow(stock_code=self.stock_code, period="annual"), outfile, indent=4)
                    outfile.close()
                with open(self.file_path + "/json/" +self.ending_period+'-last/'+self.stock_code +'_ratios_'+self.ending_period+'.json',
                          'w') as outfile:
                    json.dump(self.extract_ratios(stock_code=self.stock_code), outfile, indent=4)
                    outfile.close()
            except (FileNotFoundError, IOError):
                print(f"Wrong file or file path for {self.stock_code} error: {FileNotFoundError}")
                self.write_json_fails.append(self.stock_code)
        else:
            try:
                with open(self.file_path + "/json/" + self.ending_period + '-all/' + self.stock_code + '_general_' + self.ending_period + '.json',
                          'w') as outfile:
                    json.dump(self.extract_general_info(stock_code=self.stock_code), outfile, indent=4)
                    outfile.close()
                with open(self.file_path + "/json/" + self.ending_period + '-all/' + self.stock_code + '_income_statements_quarter_' + self.ending_period + '.json',
                          'w') as outfile:
                    json.dump(self.extract_income_statement(stock_code=self.stock_code, period="quarter"), outfile,
                              indent=4)
                    outfile.close()
                with open(self.file_path + "/json/" + self.ending_period + '-all/' + self.stock_code + '_income_statements_annual_' + self.ending_period + '.json',
                          'w') as outfile:
                    json.dump(self.extract_income_statement(stock_code=self.stock_code, period="annual"), outfile, indent=4)
                    outfile.close()
                with open(self.file_path + "/json/" + self.ending_period + '-all/' + self.stock_code + '_balance_sheets_quarter_' + self.ending_period + '.json',
                          'w') as outfile:
                    json.dump(self.extract_balance_sheet(stock_code=self.stock_code, period="quarter"), outfile, indent=4)
                    outfile.close()
                with open(self.file_path + "/json/" + self.ending_period + '-all/' + self.stock_code + '_balance_sheets_annual_' + self.ending_period + '.json',
                          'w') as outfile:
                    json.dump(self.extract_balance_sheet(stock_code=self.stock_code, period="annual"), outfile, indent=4)
                    outfile.close()
                with open(self.file_path + "/json/" + self.ending_period + '-all/' + self.stock_code + '_cash_flows_quarter_'+ self.ending_period + '.json',
                          'w') as outfile:
                    json.dump(self.extract_cash_flow(stock_code=self.stock_code, period="quarter"), outfile, indent=4)
                    outfile.close()
                with open(self.file_path + "/json/" + self.ending_period + '-all/' + self.stock_code + '_cash_flows_annual_' +self.ending_period + '.json',
                          'w') as outfile:
                    json.dump(self.extract_cash_flow(stock_code=self.stock_code, period="annual"), outfile, indent=4)
                    outfile.close()
                # with open(self.file_path + "/json/" + self.ending_period + '-all/' + self.stock_code + '_ratios_annual' +self.ending_period + '.json',
                #           'w') as outfile:
                #     json.dump(self.extract_ratios(stock_code=self.stock_code), outfile, indent=4)
                #     outfile.close()
            except (FileNotFoundError, IOError):
                print(f"Wrong file or file path for {self.stock_code} error: {FileNotFoundError}")
                self.write_json_fails.append(self.stock_code)
    def open_target_url(self):
        self.driver.get(self.target_url)

if __name__ == '__main__':
    reader = RTI_Reader(all=True,read_online=False)
    stocks = pd.read_excel(reader.file_path + '/daftar_saham.xlsx')
    stocks = pd.DataFrame(stocks)
    go = False
    for stock in stocks["Kode"]:
        print(reader.extract_general_info(stock_code=stock))
        print("")
        # print(reader.extract_income_statement(stock_code=stock, period="annual"))
        # print("")
        # print(reader.extract_balance_sheet(stock_code=stock, period="annual"))
        # print("")
        # print(reader.extract_cash_flow(stock_code=stock, period="annual"))
        # print("")
        # print(reader.extract_ratios(stock_code=stock))

        reader.write_json(stock)
    print("write json done")

    stock_list = []
    for stock in stocks["Kode"]:
        stock_list.append(stock)
    print(stock_list)

    # write stock list json
    # try:
    #     with open(
    #             reader.file_path + "/json/stock_list.json",
    #             'w') as outfile:
    #         json.dump(stock_list, outfile)
    #         outfile.close()
    #         print(f"write stock list json succeed")
    # except (FileNotFoundError, IOError):
    #     print(f"Wrong file or file path error: {FileNotFoundError}")


    # for selected stocks only
    reader = RTI_Reader(all=True, read_online=False)
    stocks = ["AALI"]

    for stock in stocks:
        print(reader.extract_general_info(stock_code=stock))
        print("")
        # print(reader.extract_income_statement(stock_code=stock, period="annual"))
        # print("")
        # print(reader.extract_balance_sheet(stock_code=stock, period="annual"))
        # print("")
        # print(reader.extract_cash_flow(stock_code=stock, period="annual"))
        # print("")
        # print(reader.extract_ratios(stock_code=stock))

        reader.write_json(stock)
    print("write json done")


    # reader = RTI_Reader(all=False,read_online=False)
    # stocks = pd.read_excel(reader.file_path + '/daftar_saham.xlsx')
    # stocks = pd.DataFrame(stocks)
    # go = False
    # for stock in stocks["Kode"]:
    #     print(reader.extract_general_info(stock_code=stock))
    #     print("")
    #     # print(reader.extract_income_statement(stock_code=stock, period="annual"))
    #     # print("")
    #     # print(reader.extract_balance_sheet(stock_code=stock, period="annual"))
    #     # print("")
    #     # print(reader.extract_cash_flow(stock_code=stock, period="annual"))
    #     # print("")
    #     # print(reader.extract_ratios(stock_code=stock))
    #
    #     reader.write_json(stock)
    # print("write json done")
    #
    #
    # reader.write_json_fails
    #
    # fails = ['ARTO', 'ASBI', 'ASDM', 'ASGR', 'ASII', 'ASJT', 'ASMI', 'ASRI', 'ASRM', 'ASSA', 'ATIC', 'ATPK', 'AUTO', 'BABP', 'BBYB', 'BELL', 'BORN', 'BTEL', 'BULL', 'CANI', 'CASA', 'CASS', 'CKRA', 'CLPI', 'CNKO', 'CNTX', 'CPRI', 'DFAM', 'DGIK', 'DPUM', 'DUCK', 'ELTY', 'ENRG', 'ETWA', 'FIRE', 'FOOD', 'GEMS', 'GLOB', 'GOLL', 'GREN', 'GSMF', 'HEXA', 'HRME', 'IKBI', 'INDX', 'ITMA', 'JAST', 'KBRI', 'KONI', 'KRAH', 'MAMI', 'MAPI', 'MRAT', 'MTFN', 'MTPS', 'MTRA', 'MYOH', 'NIPS', 'NUSA', 'POLI', 'POLY', 'POSA', 'PRIM', 'PSDN', 'RELI', 'RIGS', 'RIMO', 'SAFE', 'SDRA', 'SIAP', 'SMRU', 'SQMI', 'SSMS', 'SUGI', 'SULI', 'TAMU', 'TDPM', 'TELE', 'TMPI', 'TMPO', 'TPIA', 'TRAM', 'TRIO', 'TRST', 'URBN']
    # for stock in fails:
    #     print(reader.extract_general_info(stock_code=stock))
    #     print("")
    #     print(reader.extract_income_statement(stock_code=stock, period="annual"))
    #     print("")
    #     print(reader.extract_balance_sheet(stock_code=stock, period="annual"))
    #     print("")
    #     print(reader.extract_cash_flow(stock_code=stock, period="annual"))
    #     print("")
    #     print(reader.extract_ratios(stock_code=stock))
    #     reader.write_json()


    # print
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(reader.extract_general_info(stock_code="ABMM"))
    # print("")
    # pp.pprint(reader.extract_income_statement(stock_code="ABMM", period="annual"))
    # print("")
    # pp.pprint(reader.extract_balance_sheet(stock_code="ABMM", period="annual"))
    # print("")
    # pp.pprint(reader.extract_cash_flow(stock_code="ABMM", period="annual"))
    # pp.pprint(reader.extract_ratios(stock_code="ABMM"))
    #

    #
    # stocks = pd.read_excel("/Users/nugroho/basnugroho717@gmail.com drive/sahamin/rti/" + '/daftar_saham.xlsx')
    # stocks = pd.DataFrame(stocks)
    # stocks.loc[stocks['Kode'] == 'AALI']
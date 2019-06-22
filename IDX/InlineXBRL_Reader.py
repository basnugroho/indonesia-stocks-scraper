from bs4 import BeautifulSoup
import re
import os
import json
import pprint


class Scraper:
    def __init__(self, year, quarter, code):
        self.year = year
        self.quarter = quarter
        self.download_path = "/Users/nugroho/basnugroho717@gmail.com drive/sahamin/financial_statements/"
        self.path = self.download_path + str(year) + '/Q' + str(quarter) + '/' + code + '/inlineXBRL/'

        # run on create object
        self.inline_xbrl_files = []
        self.set_xbrl_list_files()

    def set_xbrl_list_files(self):
        for file in os.listdir(self.path):
            if file.endswith(".html"):
                # print(os.path.join("Scrapers/2018/Q3/AALI/inlineXBRL/", file))
                self.inline_xbrl_files.append(file)
                self.inline_xbrl_files.sort()

    def read_file(self,file):
        file = open(self.path+file)
        data = file.read()
        file.close()
        return data

    def get_general_info(self):
        soup = BeautifulSoup(self.read_file(file=self.inline_xbrl_files[0]), 'lxml')
        columns = self.get_general_info_en_columns()
        values = self.get_general_info_values()
        data = dict(zip(columns, values))
        return data

    def get_balance_sheet(self):
        soup = BeautifulSoup(scraper.read_file(file=scraper.inline_xbrl_files[1]), 'lxml')
        trows = soup.findAll('tr', {'style': ''})

        columns = []
        values = []
        for row in trows:
            cols = row.findAll('td', {'class': 'rowHeaderEN01'})
            for col in cols:
                columns.append(col.contents[0].replace(' ', '_').lower())
            vals = row.findAll('ix:nonfraction', {'contextref': 'CurrentYearInstant'})
            if len(vals) > 0:
                numb_str = re.sub('  +', '', vals[0].contents[0].replace('\n', ''))
                try:
                    values.append(float(numb_str.replace(',', '')))
                except Exception as e:
                    print(e)
            else:
                values.append('')

        return dict(zip(columns, values[2:]))

    def get_income_statement(self):
        soup = BeautifulSoup(scraper.read_file(file=scraper.inline_xbrl_files[2]), 'lxml')
        trows = soup.findAll('tr', {'style': ''})

        columns = []
        values = []

        pass

        # for row in trows:
        #     cols = row.findAll('td', {'class': 'rowHeaderEN01'})
        #     for col in cols:
        #         columns.append(col.contents[0].replace(' ', '_').lower())
        #
        #     vals = row.findAll('ix:nonfraction', {'contextref': 'CurrentYearDuration'})
        #     minus_sign = row.findAll('td', {'class': 'valueCell'})
        #     if len(vals) > 0:
        #         numb_str = re.sub('  +', '', vals[0].contents[0].replace('\n', ''))
        #         try:
        #             values.append(float(numb_str.replace(',', '')))
        #         except Exception as e:
        #             print(e)
        #     else:
        #         values.append('')

        # # negatify
        # shifted_values = values[2:]
        # minus_signs = self.find_minus_signs()
        # for i in range(0, len(minus_signs)):
        #     if minus_signs[i]:
        #         shifted_values[i] = -1 * shifted_values[i]
        #
        # return dict(zip(columns, shifted_values))

    def find_minus_signs(self):
        min_signs = []
        signs = []
        soup = BeautifulSoup(scraper.read_file(file=scraper.inline_xbrl_files[2]), 'lxml')
        trows = soup.findAll('tr', {'style': ''})
        for row in trows:
            minus_sign = row.findAll('td', {'class': 'valueCell'})
            min_signs.append(minus_sign)

        for i in range(1, len(min_signs)):
            if len(min_signs[i]) > 0:
                if str(min_signs[i][0]).find('(') is not -1:
                    signs.append(True)
                else:
                    signs.append(False)
        return signs

    def get_cash_flow(self):
        pass

    def get_all(self, type='json'):
        # data = self.get_general_info().copy()
        # data.update({'income_statement': self.get_income_statement()})
        data = {'general_info': self.get_general_info(),
                'balance_sheet': self.get_balance_sheet(),
                'income_statement': self.get_income_statement(),
                'cash_flow': self.get_cash_flow()
                }
        # if(type=='json'):
        #     return json.dumps(data)
        # else:
        #     return json.dumps(data)
        return data

    def write_json(self):
        with open(self.path+'data.json', 'w') as outfile:
            json.dump(self.get_all(), outfile, indent=4)
            outfile.close()

    def get_general_info_en_columns(self, file_number=0):
        soup = BeautifulSoup(self.read_file(file=self.inline_xbrl_files[file_number]), 'lxml')
        columns = soup.findAll(attrs={'class': 'rowHeaderEN01'})
        return [col.text.replace(' ', '_').lower() for col in columns]

    def get_general_info_values(self, file_number=0):
        soup = BeautifulSoup(self.read_file(file=self.inline_xbrl_files[file_number]), 'lxml')
        columns = soup.findAll(attrs={'class': 'valueCell'})
        return [re.sub('  +', '', col.text.replace('\n', '')) for col in columns]

    def get_visible_balance_sheet_columns(self):
        soup = BeautifulSoup(self.read_file(file=self.inline_xbrl_files[1]), 'lxml')
        trows = soup.findAll('tr', {'style': ''})
        visible_columns = []
        for row in trows:
            cols = row.findAll('td', {'class': 'rowHeaderEN01'})
            for col in cols:
                visible_columns.append(col.contents[0])
        data = [column.replace(' ', '_').lower() for column in visible_columns]
        return data

if __name__ == '__main__':
    scraper = Scraper(year=2017, quarter=1, code='UNVR')
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(scraper.get_general_info())

    scraper.write_json()
    # pp.pprint(scraper.get_general_info_en_columns())
    # print(len(scraper.get_general_info_en_columns()))
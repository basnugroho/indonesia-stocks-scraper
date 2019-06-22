from selenium import webdriver
from time import  sleep
import os
from bs4 import BeautifulSoup
import re
import requests
import zipfile

class Downloader:
    def __init__(self, download_path='/Users/nugroho/basnugroho717@gmail.com drive/sahamin/financial_statements',
                 target_url='https://www.idx.co.id/perusahaan-tercatat/laporan-keuangan-dan-tahunan/'):
        self.download_path = download_path
        self.driver = webdriver.Chrome('/Users/nugroho/basnugroho717@gmail.com drive/sahamin/chromedriver')
        self.target_url = target_url
        self.empty_inlineXBRL_list = []
        self.submitted_inlineXBRL_list = []

    def reset_inlineXBRL_list(self):
        self.empty_inlineXBRL_list = []

    def reset_submitted_inlineXBRL_list(self):
        self.submitted_inlineXBRL_list = []

    def load_search(self, year, quarter, stocks = []):
        quarter_tw = self.int_quarter_to_tw(quarter)
        if (len(stocks) < 1):
            self.driver.find_element_by_xpath('//div[@class="option-box"]/select[@id="yearList"]/option[@value="%s"]' %(year)).click()
            self.driver.find_element_by_xpath('//div[@class="option-box"]/select[@id="periodList"]/option[@value="%s"]' %(quarter_tw)).click()
            self.driver.find_element_by_id('searchButton').click()
        else:
            pass
        sleep(2)

    def open_target_url(self):
        # open target url
        self.driver.get(self.target_url)
        sleep(2)

    def download_inlineXBRL(self, year, quarter):
        print("Downloading to "+self.download_path+" folder . . .")

        # preparation
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        container = soup.find_all("div", {"class": "container"})
        financial_reps = container[3].find_all("div", {"class": "financial-report-container"})

        # scrape page source
        for finrep in financial_reps:
            stock_code = finrep.find("dd", {"class": "financial-report-description ng-binding"}).text
            download_path = self.download_path + '/' + str(year) + '/Q' + str(quarter) + '/' + stock_code

            # cek folder (kode saham)
            if not os.path.exists(download_path):
                os.makedirs(download_path)
                print(stock_code+": "+download_path, ' folder created')
            else:
                print(stock_code+": "+download_path, ' folder already exist')

            # download inlineXBRL.zip
            fins = finrep.find_all("div", {"class": "financial-report-download ng-scope"})
            xbrl_exist = False
            for fin in fins:
                if fin.a.text == 'inlineXBRL.zip':
                    self.submitted_inlineXBRL_list.append(stock_code)
                    xbrl_exist = True
                    xblr_url = fin.a['href']
                    local_xblr_name = xblr_url.split("/")[len(xblr_url.split("/")) - 1]

                    # cek lg sampai level file, kalo file gakada lanjut cari link download
                    exists = os.path.isfile(download_path+'/'+local_xblr_name)
                    local_file_path = os.path.join(download_path, local_xblr_name)
                    if exists:
                        print(stock_code+": "+local_xblr_name+" file already exist")
                        # extract zip
                        self.unzip(stock_code, local_file_path, download_path+"/inlineXBRL")
                    else:
                        req = requests.get(xblr_url, stream=True)
                        sleep(2)
                        try:
                            with open(local_file_path, 'wb') as fl:
                                for chunk in req.iter_content(chunk_size=1024):
                                    if chunk:
                                        fl.write(chunk)
                            print(stock_code+": "+local_xblr_name+" downloaded")
                        except Exception as e:
                            print(e)
                            print('Could not download ' +stock_code+ '_inlineXBLR.zip')
                            print('xblr_url: ', xblr_url)
            if (xbrl_exist==False):
                self.empty_inlineXBRL_list.append(stock_code)
                print(stock_code+": xbrl file not found")
        print("download done\n")

    def unzip(self, stock_code, file_path, extract_path, delete=False):
        zip_ref = zipfile.ZipFile(file_path, 'r')
        zip_ref.extractall(extract_path)
        print(stock_code+": inlineXBRL.zip extracted")
        zip_ref.close()

    def get_total_pages(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        pagination = soup.find_all("ul", {"class": "pagination ng-scope"})
        if (pagination == []):
            return 1
        else:
            pages = pagination[0].find_all("li", {"class": "ng-scope"})
            a = []
            for page in pages:
                a.append(page.find("a", {"class": "ng-binding"}))
            return int(re.findall('\d+', str(a[-2]))[0])

    def close_browser(self):
        self.driver.close()

    def int_quarter_to_tw(self, quarter):
        if (quarter==1):
            return 'tw1'
        elif (quarter==2):
            return 'tw2'
        elif(quarter==3):
            return 'tw3'
        else:
            return 'audit'

    def save_page_source(self):
        try:
            file = open('Scrapers/page_source.html', 'w', encoding='utf-8')
            file.write(self.html)
            file.close()
        except:
            print('save file error')

    def move_to_next_page(self):
        paginats = self.driver.find_elements_by_xpath('//li[@class="ng-scope"]/a')
        for page in paginats:
            if (page.text == '›'):
                try:
                    page.click()
                    #print(f"page {page.text} clicked!")
                    active_page = self.driver.find_element_by_xpath('//li[@class="ng-scope active"]/a')
                    print(f"moved to page: {active_page.text}")
                    #print(". . .")
                    sleep(1)
                except Exception as e:
                    print(e)
                    print(f"could not move to next page")

    def move_to_page(self, page_number):
        paginats = self.driver.find_elements_by_xpath('//li[@class="ng-scope"]/a')
        for page in paginats:
            if (page.text == str(page_number)):
                try:
                    page.click()
                    #print(f"page {page.text} clicked!")
                    active_page = self.driver.find_element_by_xpath('//li[@class="ng-scope active"]/a')
                    print(f"moved to page: {active_page.text}")
                    sleep(1)
                except Exception as e:
                    print(e)
                    print(f"could not move to page: {active_page.text}")

    def get_total_submitted(self):
        return len(self.submitted_inlineXBRL_list) + len(self.empty_inlineXBRL_list)

    def print_active_page(self):
        active_page = self.driver.find_element_by_xpath('//li[@class="ng-scope active"]/a')
        print(f"current active page: {active_page.text}")

if __name__ == '__main__':
    dl = Downloader()
    dl.open_target_url()
    year=2017
    quarter=2
    star_page=1 # sementara 1 only

    # download xbrl files
    dl.reset_inlineXBRL_list()
    dl.reset_submitted_inlineXBRL_list()
    dl.load_search(year=year, quarter=quarter)
    dl.move_to_page(star_page)
    total_pages = dl.get_total_pages()
    print(f"total pages: {total_pages}")
    if (total_pages>1):
        for page in range(star_page-1,total_pages):
            #print(f"{dl.print_active_page()}")
            dl.download_inlineXBRL(year=year, quarter=quarter)
            dl.move_to_next_page()
    else:
        dl.download_inlineXBRL(year=year, quarter=quarter)

    # extract downloaded xbrl files
    dl.reset_inlineXBRL_list()
    dl.reset_submitted_inlineXBRL_list()
    dl.load_search(year=year, quarter=quarter)
    dl.move_to_page(star_page)
    total_pages = dl.get_total_pages()
    print(f"total pages: {total_pages}")
    if (total_pages>1):
        for page in range(star_page-1,total_pages):
            #print(f"{dl.print_active_page()}")
            dl.download_inlineXBRL(year=year, quarter=quarter)
            dl.move_to_next_page()
    else:
        dl.download_inlineXBRL(year=year, quarter=quarter)

    # check
    print("empty inlineXBRL stocks:")
    print(dl.empty_inlineXBRL_list)
    print("total empty inlineXBRL: "+str(len(dl.empty_inlineXBRL_list)))
    print("total submitted inlineXBRL: " + str(len(dl.submitted_inlineXBRL_list)))
    print("total all submitted stocks: "+str(dl.get_total_submitted()))
    #print(dl.submitted_inlineXBRL_list)
    #dl.close_browser()
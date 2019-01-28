# coding=utf-8
import tushare as tu
import pandas as pd
from finance_common_utils.common_utils import datetime_utils as dateutils
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from finance_common_utils.common_utils import datetime_utils
from selenium import webdriver
import time
from finance_news_report_analysis.utils import spider_common_utils as utils
from selenium.webdriver.chrome.options import Options


#设置TOKEN
tu.set_token('b2d9cda1ccac47a845fc2dd31e41a39185bfa43d5b6fa110fddf21e2')
#设置PRO-API
pro = tu.pro_api()

NEWS_PLATFORM = {'eastmoney': 'EM'}
NEWS_URL={'eastmoney':'http://data.eastmoney.com/rzrq/total/all.10.html'}

def init_stock_money_margin():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(NEWS_URL['eastmoney'])
    print('TIME:--->' + datetime_utils.datetimeutils().get_current_datetime())
    time.sleep(15)
    print('TIME:--->' + datetime_utils.datetimeutils().get_current_datetime())
    infordata = []
    contents = driver.find_element_by_id("rzrqjyzlTable").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
    for vo in contents:
        voo = vo.find_elements_by_tag_name('td')
        for vooo in voo:
            text = utils.replace_spicial_symbol(vooo.text)
            print(text)
        print("------------------------------")



if __name__ == '__main__':
    init_stock_money_margin()
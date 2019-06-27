# coding=utf-8
import pandas as pd
from finance_common_utils.common_utils import datetime_utils as dateutils
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from finance_common_utils.common_utils import datetime_utils
from selenium import webdriver
import time
from finance_news_report_analysis.utils import spider_common_utils as utils
from selenium.webdriver.chrome.options import Options
from finance_common_utils.common_utils import Logger as loggers
from finance_stock_dao_model.stock_money_margin_trade_data_dto import stock_money_margin_trade_data_dto as dto
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager

NEWS_PLATFORM = {'eastmoney': 'EM'}
NEWS_URL={'eastmoney':'http://data.eastmoney.com/rzrq/total/all.10.html'}

logger = loggers.Logger(logname='log.txt', loglevel=1, logger="init_stock_money_margin").getlog()

def init_stock_money_margin():
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 指定无界面形式运行
    chrome_options.add_argument('no-sandbox')  # 禁止沙盒
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(NEWS_URL['eastmoney'])
    logger.info('TIME:--->' + datetime_utils.datetimeutils().get_current_datetime())
    time.sleep(5)
    logger.info('TIME:--->' + datetime_utils.datetimeutils().get_current_datetime())
    infordata = []
    contents = driver.find_element_by_id("rzrqjyzlTable").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
    current_data=[]
    for vo in contents:
        voo = vo.find_elements_by_tag_name('td')
        for vooo in voo:
            text = utils.replace_spicial_symbol(vooo.text)
            current_data.append(text)
    data = arr_size(current_data,13)
    for con in data:
        index = 0
        trade_date =None
        hushen_300_index =None
        up_down_point =None
        rz_drye = None
        rz_drye_zltszb = None
        rz_sr_mre = None
        rz_sr_che = None
        rz_sr_jmr = None
        rq_drye = None
        rq_dryl = None
        rq_sr_mcl = None
        rq_sr_chl = None
        rq_sr_jmc = None

        for conn in con:
            if index ==0:
               trade_date =conn
            elif index ==1:
               hushen_300_index = conn
            elif index ==2:
                up_down_point = conn
            elif index ==3:
                rz_drye = replace_special_character(conn)
            elif index ==4:
                rz_drye_zltszb = replace_special_character(conn)
            elif index ==5:
                rz_sr_mre = replace_special_character(conn)
            elif index ==6:
                rz_sr_che = replace_special_character(conn)
            elif index ==7:
                rz_sr_jmr = replace_special_character(conn)
            elif index ==8:
                rq_drye = replace_special_character(conn)
            elif index ==9:
                rq_dryl = replace_special_character(conn)
            elif index ==10:
                rq_sr_mcl = replace_special_character(conn)
            elif index ==11:
                rq_sr_chl = replace_special_character(conn)
            elif index ==12:
                rq_sr_jmc = replace_special_character(conn)
                vodto = dto(trade_date=trade_date,hushen_300_index=hushen_300_index,up_down_point=up_down_point,
                            rz_drye=rz_drye,rz_drye_zltszb=rz_drye_zltszb,rz_sr_mre=rz_sr_mre,
                            rz_sr_che=rz_sr_che,rz_sr_jmr=rz_sr_jmr,rq_drye=rq_drye,
                            rq_dryl=rq_dryl,rq_sr_mcl=rq_sr_mcl,rq_sr_chl=rq_sr_chl,rq_sr_jmc=rq_sr_jmc)
                dbmanager.sql_manager().single_common_save_basedata(vodto)
            index = index + 1

def replace_special_character(input_data):
    if input_data.find('亿') != -1:
        input_data = input_data.replace('亿', '').replace(' ', '')
        input_data = round(float(input_data) * 100000000)
    elif input_data.find('万') != -1:
        input_data = input_data.replace('万', '').replace(' ', '')
        input_data = round(float(input_data) * 10000)
    elif input_data.find('%') != -1:
        input_data = input_data.replace('%', '').replace(' ', '')
    return input_data


def arr_size(arr,size):
    s=[]
    for i in range(0,int(len(arr))+1,size):
        c=arr[i:i+size]
        s.append(c)
    return s

if __name__ == '__main__':
    init_stock_money_margin()
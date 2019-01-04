# coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import utils.spider_common_utils as utils
from finance_common_utils.common_utils.datetime_model import datetime_utils
import finance_common_utils.mysql_dbutils.sqlalchemy_dbutils as dbmanager
from finance_stock_dao_model.stock_news_data_dto import stock_news_data_dto as dto
from finance_news_report_research import notice_research_constant as constant
import sys
import uuid

NEWS_PLATFORM = {'wallstreetcn': 'WALLSTREETCN','yuncaijing':'YUNCAIJING'}
NEWS_URL={'wallstreetcn':'https://wallstreetcn.com/live/a-stock',
          'yuncaijing':'https://www.yuncaijing.com/insider/main.html'}



def daily_wallstreetcn_spider():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(NEWS_URL['wallstreetcn'])
    contents = driver.find_elements_by_class_name("live-item")
    for vo in contents:
        text = vo.find_element_by_class_name("live-item_html").text
        infor = utils.replace_special_character(text)
        index_date = vo.find_element_by_class_name("live-item_created").text
        href = vo.find_element_by_tag_name("a").get_attribute("href")
        save_current_news('wallstreetcn',index_date,href,infor)


def daily_yuncaijing_spider():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(NEWS_URL['yuncaijing'])
    contents = driver.find_element_by_class_name("news-ul").find_elements_by_tag_name("li")
    for vo in contents:
        index_date = vo.find_element_by_class_name("time").text
        href = vo.find_element_by_class_name("nc-arc-wrap").find_element_by_tag_name("a").get_attribute("href")
        text =vo.find_element_by_class_name("nc-arc-wrap").find_element_by_class_name("des").text
        infor = utils.replace_special_character(text)
        save_current_news('yuncaijing',index_date,href,infor)


def save_current_news(platform,index_date,href,infor):
    vodto = dto(index_date=index_date, href=href, context=infor,
                create_time=datetime_utils.datetimeutils().get_current_datetime(),
                news_platform=NEWS_PLATFORM[platform])
    dbmanager.sql_manager().single_common_save_basedata(vodto)


if __name__=='__main__':
    daily_yuncaijing_spider()

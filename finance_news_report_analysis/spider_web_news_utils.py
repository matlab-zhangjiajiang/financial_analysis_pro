# coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from finance_news_report_analysis.utils import spider_common_utils as utils
from finance_common_utils.common_utils import datetime_utils
import finance_common_utils.mysql_dbutils.sqlalchemy_dbutils as dbmanager
from finance_stock_dao_model.stock_news_data_dto import stock_news_data_dto as dto

NEWS_PLATFORM = {'wallstreetcn': 'WSC','yuncaijing':'YCJ','tonghuasun':'THS','eastmoney':'EM','sina':'SA'}
NEWS_URL={'wallstreetcn':'https://wallstreetcn.com/live/a-stock',
          'yuncaijing':'https://www.yuncaijing.com/insider/main.html',
          'tonghuasun':'http://news.10jqka.com.cn/realtimenews.html',
          'eastmoney':'http://kuaixun.eastmoney.com',
          'sina':'http://finance.sina.com.cn/7x24/'}



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
    driver.quit()


def daily_yuncaijing_spider():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    try:
        driver.get(NEWS_URL['yuncaijing'])
        contents = driver.find_element_by_class_name("news-ul").find_elements_by_tag_name("li")
        for vo in contents:
           index_date = vo.find_element_by_class_name("time").text
           href = vo.find_element_by_class_name("nc-arc-wrap").find_element_by_tag_name("a").get_attribute("href")
           text =vo.find_element_by_class_name("nc-arc-wrap").find_element_by_class_name("des").text
           infor = utils.replace_special_character(text)
           save_current_news('yuncaijing',index_date,href,infor)
    except Exception as error:
        print('spider error',error)
    finally:
        driver.quit()


def daily_tonghuasun_spider():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(NEWS_URL['tonghuasun'])
    content = driver.find_element_by_css_selector("[class='newsText all']")
    contents = content.find_elements_by_tag_name("li")
    for vo in contents:
         if vo.get_attribute('class')!='beforeNewTime':
            index_date = vo.find_element_by_class_name("newsTimer").text
            href = vo.find_element_by_class_name("newsDetail").find_element_by_tag_name("a").get_attribute("href")
            text = vo.find_element_by_class_name("newsDetail").find_element_by_tag_name("a").text
            infor = utils.replace_special_character(text)
            save_current_news('tonghuasun',index_date,href,infor)
    driver.quit()


def daily_eastmoney_spider():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    try:
       driver.get(NEWS_URL['eastmoney'])
       content = driver.find_element_by_id("livenews-list")
       contents = content.find_elements_by_class_name("livenews-media")
       for vo in contents:
           index_date = vo.find_element_by_class_name("time").text
           flag = True
           try:
              href = vo.find_element_by_tag_name("a")
           except Exception as error:
              flag = False
           if flag:
              href = vo.find_element_by_tag_name("a").get_attribute("href")
              text = vo.find_element_by_tag_name("a").text
              infor = utils.replace_special_character(text)
              save_current_news('eastmoney', index_date, href, infor)
    except Exception as error:
        print('spider error',error)
    finally:
        driver.quit()


def daily_sina_spider():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    try:
       driver.get(NEWS_URL['sina'])
       content = driver.find_element_by_id("liveList01")
       contents = content.find_elements_by_css_selector("[class='bd_i bd_i_og  clearfix']")
       for vo in contents:
           index_date = vo.find_element_by_class_name("bd_i_time_c").text
           text = vo.find_element_by_class_name("bd_i_txt_c").text
           infor = utils.replace_special_character(text)
           href = NEWS_URL['sina']+datetime_utils.datetimeutils().get_current_time_new()+'/'+index_date
           save_current_news('sina', index_date, href, infor)
    except Exception as error:
        print('spider error',error)
    finally:
        driver.quit()


def save_current_news(platform,index_date,href,infor):
    vodto = dto(index_date=index_date, href=href, context=infor,
                create_time=datetime_utils.datetimeutils().get_current_datetime(),
                news_platform=NEWS_PLATFORM[platform])
    dbmanager.sql_manager().single_common_save_basedata(vodto)


if __name__=='__main__':
    daily_sina_spider()

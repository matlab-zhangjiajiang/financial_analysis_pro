# coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from finance_common_utils.common_utils import datetime_utils
from finance_news_report_analysis.utils import spider_common_utils as utils
from datetime import datetime
from finance_stock_dao_model.exchange_stock_notice_infor_dto import exchange_stock_notice_infor_dto as dto
from finance_common_utils.common_utils import Logger as loggers


NEWS_PLATFORM = {'sse.com': 'SSE','szse.com':'SZSE'}
NEWS_URL={'sse.com':'http://www.sse.com.cn/disclosure/listedinfo/announcement/',
          'szse.com':'http://www.szse.cn/disclosure/listed/notice/index.html',
          'main.szse':'http://www.szse.cn'}

logger = loggers.Logger(logname='log.txt', loglevel=1, logger="exchange_stock_notice_manager").getlog()

class exchange_stock_notice_manager(object):

    #上交所公告
    def get_announcement_notice_sse(self):
        logger.info('----main----')
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(NEWS_URL['sse.com'])
        logger.info('TIME:--->'+datetime_utils.datetimeutils().get_current_datetime())
        time.sleep(5)
        logger.info('TIME:--->'+datetime_utils.datetimeutils().get_current_datetime())
        infordata = []
        contents = driver.find_element_by_class_name("modal_pdf_list").find_elements_by_tag_name("dd")
        for vo in contents:
            info_code = utils.replace_special_character(vo.get_attribute("data-seecode"))
            info_time = utils.replace_special_character(vo.get_attribute("data-time"))
            info_url = vo.find_element_by_tag_name("a").get_attribute("href")
            info_title = vo.find_element_by_tag_name("a").get_attribute("title")
            vo = dto(stock_code=info_code, info_url=info_url, info_title=info_title, key_time=info_time)
            infordata.append(vo)
        return infordata

    #深交所公告
    def get_announcement_notice_szse(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(NEWS_URL['szse.com'])
        logger.info('TIME:--->' + datetime_utils.datetimeutils().get_current_datetime())
        time.sleep(5)
        logger.info('TIME:--->' + datetime_utils.datetimeutils().get_current_datetime())
        infordata = []
        contents = driver.find_element_by_class_name("disclosure-tbody").find_elements_by_tag_name("tr")
        for vo in contents:
            info_code = vo.find_element_by_css_selector("[class='pull-left title-code']").text
            infor_company = vo.find_element_by_class_name("ellipsis").get_attribute("title")
            obj = vo.find_element_by_class_name("text-title-box").find_element_by_tag_name("a")
            info_url = obj.get_attribute("href")
            info_title = infor_company+":"+utils.replace_special_character(obj.text)
            info_time = vo.find_element_by_class_name("text-time").text
            vo = dto(stock_code=info_code, info_url=info_url, info_title=info_title, key_time=info_time)
            infordata.append(vo)
        return infordata


    def get_announcement_all_notice(self):
        ssedata = self.get_announcement_notice_sse()
        szsedata = self.get_announcement_notice_szse()
        data = ssedata+szsedata
        return data

if __name__ == '__main__':
    print(exchange_stock_notice_manager().get_announcement_all_notice())
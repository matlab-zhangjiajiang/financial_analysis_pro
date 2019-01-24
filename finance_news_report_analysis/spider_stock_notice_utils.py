# coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from finance_common_utils.common_utils import datetime_utils
import utils.spider_common_utils as utils
from datetime import datetime
from finance_stock_dao_model.exchange_stock_notice_infor_dto import exchange_stock_notice_infor_dto as dto

NEWS_PLATFORM = {'sse.com': 'SSE'}
NEWS_URL={'sse.com':'http://www.sse.com.cn/disclosure/listedinfo/announcement/'}


class exchange_stock_notice_manager(object):

    #上交所公告
    def get_announcement_notice_sse(self):
        print('----main----')
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(NEWS_URL['sse.com'])
        print('TIME:--->'+datetime_utils.datetimeutils().get_current_datetime())
        time.sleep(30)
        print('TIME:--->'+datetime_utils.datetimeutils().get_current_datetime())
        infordata = []
        contents = driver.find_element_by_class_name("modal_pdf_list").find_elements_by_tag_name("dd")
        for vo in contents:
            info_code = utils.replace_special_character(vo.get_attribute("data-seecode"))
            info_time = utils.replace_special_character(vo.get_attribute("data-time"))
            info_url = vo.find_element_by_tag_name("a").get_attribute("href")
            info_title = vo.find_element_by_tag_name("a").get_attribute("title")
            print(info_time+":"+info_code+"--->"+info_url+"--->"+info_title)
            vo = dto(stock_code=info_code, info_url=info_url, info_title=info_title, key_time=info_time)
            infordata.append(vo)
        return infordata

if __name__ == '__main__':
    print(exchange_stock_notice_manager().get_announcement_notice_sse())
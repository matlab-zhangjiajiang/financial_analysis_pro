#utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from finance_stock_common_spider.eastmoney_datacenter_spider import spider_data_web_address as address
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from finance_common_utils.common_utils import datetime_utils

class top_ten_circulate_holder(object):

    #ggdate 公告时间
    def get_top_ten_circulate_holder(self,stockcode,ggdate):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 指定无界面形式运行
        chrome_options.add_argument('no-sandbox')  # 禁止沙盒
        driver = webdriver.Chrome(options=chrome_options)
        #获取对应的地址
        driver.get(address.spider_web_address().DATA_URL['TOP_TEN_CIRCULATE_HOLDER']+stockcode)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'TTCS_Table_Div')))
        #当前年份公告列表
        element = driver.find_element_by_class_name('tab')
        datavalus = element.find_elements_by_tag_name('li')
        dd_data_list =[]
        for data in datavalus:
            dd_data_list.append(data.text)
        if ggdate in dd_data_list:
           current_element = driver.find_element_by_id('TTCS_Table_Div')
           current_table = current_element.find_element_by_css_selector("table[style='display:table']")
           li_list = current_table.find_elements_by_tag_name("tr")
           li_list = li_list[2:len(li_list)-1]
           for li_value in li_list:
               current_data = li_value.find_elements_by_tag_name('td')
               i=0
               holder_name =''
               for holder_data in current_data:
                   

                   i=i+1

               print('--------------------->')



    def spider_cron_top_ten_circulate_holder(self):
        self.get_top_ten_circulate_holder('SH601390','2019-03-31')


if __name__ == '__main__':
    top_ten_circulate_holder().spider_cron_top_ten_circulate_holder()

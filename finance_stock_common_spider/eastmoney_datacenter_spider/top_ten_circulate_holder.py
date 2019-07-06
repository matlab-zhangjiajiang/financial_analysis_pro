#utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from finance_stock_common_spider.eastmoney_datacenter_spider import spider_data_web_address as address
from finance_stock_tushare_utils.stock_basic_data import stock_area_tools as areatools
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from finance_common_utils.common_utils import datetime_utils
import tushare as tu

class top_ten_circulate_holder(object):

    def __init__(self):
        # 设置TOKEN
        tu.set_token('b2d9cda1ccac47a845fc2dd31e41a39185bfa43d5b6fa110fddf21e2')
        tu.pro_api()

    #ggdate 公告时间
    def get_top_ten_circulate_holder(self,stockcode,ggdate):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 指定无界面形式运行
        chrome_options.add_argument('no-sandbox')  # 禁止沙盒
        driver = webdriver.Chrome(options=chrome_options)
        #获取对应的地址
        url = address.spider_web_address().DATA_URL['TOP_TEN_CIRCULATE_HOLDER']+stockcode
        print(url)
        driver.get(url)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'content')))
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
               holder_nature=''
               stock_type=''
               hold_amount=0
               zzltg_cg_ratio=0
               zj_state=''
               bd_ratio=0
               for holder_data in current_data:
                   if i==0:
                       holder_name =holder_data.text
                   elif i==1:
                       holder_nature = holder_data.text
                   elif i==2:
                       stock_type = holder_data.text
                   elif i==3:
                       hold_amount = holder_data.text.replace(',','')
                   elif i==4:
                       zzltg_cg_ratio = holder_data.text.replace('%','')
                   elif i==5:
                       zj_state = holder_data.text.replace('不变','0').replace(',','')
                   elif i==6:
                       bd_ratio = holder_data.text.replace('%','').replace('--','0')
                   i=i+1
               print(holder_name+'--'+holder_nature+'--'+stock_type+'--'+hold_amount+'--'+zzltg_cg_ratio+'--'+zj_state+'--'+bd_ratio)
               print('--------------------->')
        driver.close()



    def spider_cron_top_ten_circulate_holder(self):
        basicdata = tu.get_stock_basics()
        for stokdata in list(basicdata.index):
            areacode = areatools.stock_area_tools().get_stock_area_code(stokdata)
            mainkey = areacode+stokdata
            print(mainkey)
            self.get_top_ten_circulate_holder(mainkey,'2019-03-31')


if __name__ == '__main__':
    top_ten_circulate_holder().spider_cron_top_ten_circulate_holder()

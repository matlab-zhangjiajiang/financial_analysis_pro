#utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from finance_stock_common_spider.eastmoney_datacenter_spider import spider_data_web_address as address
from finance_stock_tushare_utils.stock_basic_data import stock_area_tools as areatools
from finance_stock_dao_model.stock_circulat_holds_data_20190630_dto import stock_circulat_holds_data_20190630_dto as dto
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from finance_common_utils.common_utils import Logger as loggers
from finance_common_utils.common_utils import datetime_utils
import pandas as pd
import tushare as tu


logger = loggers.Logger(logname='log.txt', loglevel=1, logger="main_job").getlog()

class top_ten_circulate_holder(object):

    def __init__(self):
        # 设置TOKEN
        tu.set_token('b2d9cda1ccac47a845fc2dd31e41a39185bfa43d5b6fa110fddf21e2')
        tu.pro_api()

    #ggdate 公告时间
    def get_top_ten_circulate_holder(self,mainkey,ggdate,stockcode):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 指定无界面形式运行
        chrome_options.add_argument('no-sandbox')  # 禁止沙盒
        driver = webdriver.Chrome(options=chrome_options)
        try:
            # 获取对应的地址
            url = address.spider_web_address().DATA_URL['TOP_TEN_CIRCULATE_HOLDER'] + mainkey
            print(url)
            driver.get(url)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'section')))
            # 当前年份公告列表
            element = driver.find_element_by_class_name('tab')
            datavalus = element.find_elements_by_tag_name('li')
            dd_data_list = []
            gg_date_list = []
            for data in datavalus:
                gg_date_list.append(data.text)
                dd_data_list.append(int(data.text.replace('-', '')[0:6]))
            max_report_date = max(dd_data_list)
            max_gg_date = max(gg_date_list)
            if max_report_date > ggdate:
                current_element = driver.find_element_by_id('templateDiv')
                current_element = current_element.find_element_by_id('TTS_Table_Div')
                current_table = current_element.find_element_by_css_selector("table[style='display:table']")
                li_list = current_table.find_elements_by_tag_name("tr")
                li_list = li_list[2:len(li_list) - 1]
                for li_value in li_list:
                    current_data = li_value.find_elements_by_tag_name('td')
                    i = 0
                    holder_name = ''
                    stock_type = ''
                    hold_amount = 0
                    zzltg_cg_ratio = 0
                    zj_state = ''
                    bd_ratio = 0
                    for holder_data in current_data:
                        if i == 0:
                            holder_name = holder_data.text
                        elif i == 1:
                            stock_type = holder_data.text
                        elif i == 2:
                            hold_amount = holder_data.text.replace(',', '')
                        elif i == 3:
                            zzltg_cg_ratio = holder_data.text.replace('%', '')
                        elif i == 4:
                            zj_state = holder_data.replace(',', '')
                        elif i == 5:
                            bd_ratio = holder_data.text.replace('%', '').replace('--', '0')
                        i = i + 1
                    id = stockcode + max_gg_date.replace('-', '') + holder_name.replace('-', '')
                    print(
                        holder_name + '--' + stock_type + '--' + hold_amount + '--' + zzltg_cg_ratio + '--' + zj_state + '--' + bd_ratio)
                    crdto = dto(id=id, ts_code=stockcode, ann_date=max_gg_date, end_date=max_gg_date,
                                holder_name=holder_name,
                                hold_amount=hold_amount, holder_nature='', stock_type=stock_type,
                                zzltg_cg_ratio=zzltg_cg_ratio,
                                zj_state=zj_state, bd_ratio=bd_ratio)
                    dbmanager.sql_manager().single_common_save_basedata(crdto)
        except Exception as e:
            logger.info('执行出错!', e)
        finally:
            driver.close()
        driver.close()


    def get_stock_holders_basic_data(self,tablename):
        conengine = dbmanager.sql_manager().init_engine()
        sql ="select  ts_code  from finance_system_stock_circulat_holds_data_"+tablename+" group by ts_code"
        data = pd.read_sql_query(sql,conengine)
        return list(data['ts_code'])


    def spider_cron_top_ten_circulate_holder(self,tablename,dyggdate):
        existdata = self.get_stock_holders_basic_data(tablename)
        basicdata = tu.get_stock_basics()
        for stokdata in list(basicdata.index):
            if stokdata not in existdata:
               areacode = areatools.stock_area_tools().get_stock_area_code(stokdata)
               mainkey = areacode+stokdata
               print(mainkey)
               try:
                  self.get_top_ten_circulate_holder(mainkey,dyggdate,stokdata)
               except Exception as e:
                  logger.info('执行出错!',e)
                  continue

if __name__ == '__main__':
    top_ten_circulate_holder().spider_cron_top_ten_circulate_holder('20190630',201903)

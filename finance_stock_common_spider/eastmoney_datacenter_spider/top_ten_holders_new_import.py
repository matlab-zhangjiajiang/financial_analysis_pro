#utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from finance_stock_common_spider.eastmoney_datacenter_spider import spider_data_web_address as address
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from finance_stock_common_spider.eastmoney_datacenter_spider import spider_data_web_address as address
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from finance_stock_dao_model.stock_topten_holders_new_import_dto import current_table_dto  as daylydata
from finance_common_utils.common_utils import Logger as loggers

logger = loggers.Logger(logname='log.txt', loglevel=1, logger="main_job").getlog()

class top_ten_holders_new_import(object):

    def get_dayly_add_topten_holders_raw_data(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 指定无界面形式运行
        chrome_options.add_argument('no-sandbox')  # 禁止沙盒
        driver = webdriver.Chrome(options=chrome_options)
        try:
            # 获取对应的地址
            url = address.spider_web_address().DATA_URL['TOP_TEN_HOLDER_ADDER']
            driver.get(url)
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'tb_cgmx')))
            # 当前每天股东新增
            element = driver.find_element_by_id('tb_cgmx')
            tbody = element.find_element_by_tag_name('tbody')
            trdata = tbody.find_elements_by_tag_name('tr')
            for tr in trdata:
                cdata = tr.text.replace('- - ','')
                cdatas = cdata.split('\n')
                sharehdname = cdatas[1]
                cur_tr_data = cdatas[2]
                datas = cur_tr_data.split(' ')
                logger.info(datas)
                sharehdtype = datas[0]
                rank =datas[1]
                scode = datas[2]
                sname = datas[3]
                rdate = datas[7]
                sharehdnum = str(datas[8]).replace(',','')
                zb = datas[9]
                bz = datas[10]
                ltsz = str(datas[11]).replace(',','')
                ndate = datas[12]
                mainkey = sharehdname+ndate+scode
                vo = daylydata(mainkey=mainkey,sname=sname, sharehdname=sharehdname,
                           sharehdtype=sharehdtype,  rank=rank, scode=scode,
                           rdate=rdate, sharehdnum=sharehdnum, zb=zb, ndate=ndate,
                           bz=bz,ltsz=ltsz)
                dbmanager.sql_manager().single_common_save_basedata(vo)
        except Exception as e:
            logger.info('执行出错!', e)
        finally:
            driver.close()





if __name__ == '__main__':
    top_ten_holders_new_import().get_dayly_add_topten_holders_raw_data()

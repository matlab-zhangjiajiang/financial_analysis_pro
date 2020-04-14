#utf-8
import requests
import pandas as pd
import json
from finance_stock_common_spider.eastmoney_datacenter_spider import spider_data_web_address as address
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from finance_stock_dao_model.stock_dayly_increase_holder_dto import stock_dayly_increase_holder_dto as daylydata


class dayly_add_stock_topten_holders(object):

    def get_dayly_add_topten_holders_raw_data(self):
        response = requests.get(address.spider_web_address().DATA_URL['TOP_TEN_HOLDER_ADDER'])
        current_data = str(response.text)
        data = current_data.find('DlswLagO =')+11
        message = current_data[data:-1].replace('pages','\"pages\"').replace('data','\"data\"')
        raw_data = json.loads(message)
        print(raw_data)



if __name__ == '__main__':
    dayly_add_stock_topten_holders().get_dayly_add_topten_holders_raw_data()

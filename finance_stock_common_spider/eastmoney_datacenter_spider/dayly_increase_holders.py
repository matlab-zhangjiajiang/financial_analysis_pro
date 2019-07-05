#utf-8
import requests
import pandas as pd
import json
from finance_stock_common_spider.eastmoney_datacenter_spider import spider_web_address as address


class dayly_increase_holders(object):

    def get_dayly_increase_holders_raw_data(self):
        response = requests.get(address.spider_web_address().DATA_URL['DAYLY_INCREASE_HOLDINGS'])
        raw_data = json.loads(response.text)
        data = raw_data['Data'][0]['Data']
        for cdata in data:
            splitdata = cdata.split('|')
            datalist = splitdata[2:]




            #print('当前集合长度:'+str(len(splitdata)))


if __name__ == '__main__':
    dayly_increase_holders().get_dayly_increase_holders_raw_data()

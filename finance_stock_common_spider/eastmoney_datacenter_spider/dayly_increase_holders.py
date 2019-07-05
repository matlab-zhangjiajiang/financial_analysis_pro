#utf-8
import requests
import pandas as pd
import json
from finance_stock_common_spider.eastmoney_datacenter_spider import spider_web_address as address
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from finance_stock_dao_model.stock_dayly_increase_holder_dto import stock_dayly_increase_holder_dto as daylydata


class dayly_increase_holders(object):

    def get_dayly_increase_holders_raw_data(self):
        response = requests.get(address.spider_web_address().DATA_URL['DAYLY_INCREASE_HOLDINGS'])
        raw_data = json.loads(response.text)
        data = raw_data['Data'][0]['Data']
        for cdata in data:
            splitdata = cdata.split('|')
            daylyvo = splitdata[2:]
            main_key = daylyvo[0]+daylyvo[16].replace('-','')
            vo = daylydata(mainkey=main_key,stock_code=daylyvo[0],current_price=daylyvo[1],up_and_down=daylyvo[2],
                           stock_name=daylyvo[3],holder_name=daylyvo[4],mark_flag=1,cgbd_bd_num=daylyvo[6],
                           cgbd_zzgb_ratio=daylyvo[7],cgbd_zltg_ratio=daylyvo[8],bdhcd_cg_sum_num=daylyvo[10],
                           bdhcd_zzgb_ratio=daylyvo[11],bdhcd_cltg_num=daylyvo[12],bdhcd_zltg_ratio=daylyvo[13],
                           bd_start_date=daylyvo[14],bd_end_date=daylyvo[15],gg_date=daylyvo[16])
            dbmanager.sql_manager().single_common_save_basedata(vo)


if __name__ == '__main__':
    dayly_increase_holders().get_dayly_increase_holders_raw_data()

# coding=utf-8
import tushare as tu
import pandas as pd
from finance_common_utils.common_utils import datetime_utils as dateutils
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from finance_stock_dao_model.stock_money_flow_dto import stock_money_flow_dto as dto

#设置TOKEN
tu.set_token('b2d9cda1ccac47a845fc2dd31e41a39185bfa43d5b6fa110fddf21e2')
#设置PRO-API
pro = tu.pro_api()

class stock_money_flow_data(object):

    def init_money_flow_data(self):
        data = pro.moneyflow_hsgt(start_date='20181231', end_date=dateutils.datetimeutils().get_current_time_new())
        for idx, row in data.iterrows():
            vodto = dto(trade_date=row['trade_date'],ggt_ss=row['ggt_ss'],ggt_sz=row['ggt_sz'],
                        hgt=row['hgt'],sgt=row['sgt'],north_money=row['north_money'],south_money=row['south_money'])
            dbmanager.sql_manager().single_common_save_basedata(vodto)



if __name__ == '__main__':
    stock_money_flow_data().init_money_flow_data()


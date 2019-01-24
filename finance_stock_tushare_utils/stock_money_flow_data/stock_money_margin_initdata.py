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

def init_stock_money_margin():
    data = tu.sh_margins(start='2015-01-01', end='2015-04-19')
    print(data)



if __name__ == '__main__':
    init_stock_money_margin()
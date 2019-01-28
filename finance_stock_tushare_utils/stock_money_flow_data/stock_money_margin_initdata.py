# coding=utf-8
import tushare as tu
import pandas as pd
from finance_common_utils.common_utils import datetime_utils as dateutils
from finance_common_utils.common_utils import loggger_factory as loggers

#设置TOKEN
tu.set_token('b2d9cda1ccac47a845fc2dd31e41a39185bfa43d5b6fa110fddf21e2')
#设置PRO-API
pro = tu.pro_api()
logger = loggers.Logger(logname='log.txt', loglevel=1, logger="fox").getlog()

def init_stock_money_margin():

    logger.info("------------------####---------------")



if __name__ == '__main__':
    init_stock_money_margin()
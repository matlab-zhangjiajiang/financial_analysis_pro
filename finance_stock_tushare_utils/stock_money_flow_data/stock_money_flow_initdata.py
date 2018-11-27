# coding=utf-8
import tushare as tu
import pandas as pd
from finance_common_utils.common_utils.datetime_model import datetime_utils as dateutils
from finance_common_utils.matplotlib_common_utils import histogram_common_utils as drawutils
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager

#设置TOKEN
tu.set_token('b2d9cda1ccac47a845fc2dd31e41a39185bfa43d5b6fa110fddf21e2')
#设置PRO-API
pro = tu.pro_api()

class stock_money_flow_data(object):

    def init_money_flow_data(self):
        data = pro.moneyflow_hsgt(start_date='20180125', end_date=dateutils.datetimeutils().get_current_time_new())
        engine = dbmanager.sql_manager().init_engine()
        pd.io.sql.to_sql(data, 'finance_system_stock_money_flow_data', con=engine,
                         if_exists='replace', index=False,chunksize=1000)
        self.change_table_structure()

    def change_table_structure(self):
        engine = dbmanager.sql_manager().init_engine()
        enginesql = " ALTER TABLE `finance_system_stock_money_flow_data` " \
                    " MODIFY COLUMN `trade_date`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '交易日期' FIRST , " \
                    " MODIFY COLUMN `ggt_ss`  double NULL DEFAULT NULL COMMENT '港股通(上海)' AFTER `trade_date`, " \
                    " MODIFY COLUMN `ggt_sz`  double NULL DEFAULT NULL COMMENT '港股通(深圳)' AFTER `ggt_ss`, " \
                    " MODIFY COLUMN `hgt`  double NULL DEFAULT NULL COMMENT '沪股通(百万元)' AFTER `ggt_sz`, " \
                    " MODIFY COLUMN `sgt`  double NULL DEFAULT NULL COMMENT '深股通(百万元)' AFTER `hgt`, " \
                    " MODIFY COLUMN `north_money`  double NULL DEFAULT NULL COMMENT '北向资金(百万元)' AFTER `sgt`, " \
                    " MODIFY COLUMN `south_money`  double NULL DEFAULT NULL COMMENT '南向资金(百万元)' AFTER `north_money` ;"
        engine.execute(enginesql)

if __name__ == '__main__':
    stock_money_flow_data().init_money_flow_data()


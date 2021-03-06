# coding=utf-8
import tushare as tu
import pandas as pd
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from finance_common_utils.common_utils import Logger as loggers
import time

logger = loggers.Logger(logname='log.txt', loglevel=1, logger="hodlers_topten_job").getlog()

class stock_circulat_holdlers(object):

      def __init__(self):
          #设置TOKEN
          tu.set_token('b2d9cda1ccac47a845fc2dd31e41a39185bfa43d5b6fa110fddf21e2')


      def init_stock_holders_topten(self):
          # 设置PRO-API
          pro = tu.pro_api('b2d9cda1ccac47a845fc2dd31e41a39185bfa43d5b6fa110fddf21e2')
          basicdata = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
          currentlist = list(basicdata['ts_code'])


          #2019年第二季度
          current_start_date = '20190531'
          current_end_date = '20190731'

          #2019年第一季度
          #current_start_date = '20190331'
          #current_end_date = '20190531'

          #2018年第四季度
          #current_start_date = '20181030'
          #current_end_date = '20190331'

          ##2018年第三季度
          #current_start_date = '20180830'
          #current_end_date = '20181030'

          ##2018年第二季度
          #current_start_date='20180630'
          #current_end_date='20180830'

          ##2018年第一季度
          #current_start_date='20180301'
          #current_end_date='20180530'

          data = []
          try:
             sql = ' SELECT  DISTINCT ts_code  from  finance_system_stock_circulat_holds_data_'\
                + current_start_date + '  GROUP BY ts_code'
             conengine = dbmanager.sql_manager().init_engine()
             df = pd.read_sql_query(sql, conengine)
             data = list(df['ts_code'])
          except Exception as error:
             logger.info(error.args)

          for tradecode in currentlist:
              if tradecode in data:
                 logger.info("已经存在的CODE:"+tradecode)
                 continue
              try:
                  time.sleep(2)
                  df = pro.top10_floatholders(ts_code=tradecode, start_date=current_start_date,
                                              end_date=current_end_date)
                  #holders_pandas = pd.concat([holders_pandas, df])
                  df.drop_duplicates(subset='holder_name',keep='first', inplace=True)
                  engine = dbmanager.sql_manager().init_engine()
                  pd.io.sql.to_sql(df, 'finance_system_stock_circulat_holds_data_' + current_start_date, con=engine,
                                   if_exists='append', index=False,chunksize=1000)
              except Exception as error:
                  logger.info(error.args)

          self.formate_current_stock_holders_topten_table(current_start_date)

      def test_init_stock_holders_topten(self):
          # 设置PRO-API
          pro = tu.pro_api()
          df = pro.top10_floatholders(ts_code='600468.SH', start_date='20190531', end_date='20190731')
          print(df)


      def formate_current_stock_holders_topten_table(self,current_start_date):
          engine = dbmanager.sql_manager().init_engine()
          enginesql = ' ALTER TABLE finance_system_stock_circulat_holds_data_'+ current_start_date+\
                      ' MODIFY COLUMN `ts_code`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL FIRST ,' \
                      ' MODIFY COLUMN `holder_name`  varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL AFTER `end_date` ,' \
                      ' ADD INDEX `ts_holder_name` (`holder_name`) USING BTREE , ADD INDEX `ts_code_index` (`ts_code`) USING BTREE ;'
          engine.execute(enginesql)


if __name__ == '__main__':
      #stock_circulat_holdlers().init_stock_holders_topten()
      stock_circulat_holdlers().test_init_stock_holders_topten()
# coding=utf-8
import tushare as tu
import pandas as pd
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from itertools import combinations


class stock_topten_holdlers_change(object):

    def __init__(self):
        # 设置TOKEN
        tu.set_token('b2d9cda1ccac47a845fc2dd31e41a39185bfa43d5b6fa110fddf21e2')
        pd.set_option('display.max_rows', None)

    def init_strong_stock_holder(self, tablenameid):
        sql = ' SELECT  *  FROM (SELECT  COUNT(ts_code) AS counts, DATAS.holder_name AS holdername,' \
              ' DATAS.hold_amount AS holdamount , DATAS.ann_date as anndate ' \
              ' FROM finance_system_stock_circulat_holds_data_' + tablenameid + ' AS DATAS' \
              ' WHERE 1=1 GROUP BY holder_name) AS TEMP WHERE TEMP.counts >=2 ORDER BY TEMP.counts DESC '
        conengine = dbmanager.sql_manager().init_engine()
        data = pd.read_sql_query(sql, conengine)
        holdername = data['holdername']
        counts = data['counts']
        pdd = pd.DataFrame({'holdername': holdername, 'counts': counts}, index=data.index)
        return pdd
        # print(pdd)




    # 大股东增持的股票
    def increase_hold_stock_infor(self, tablestartid, tableendid, holdername):
        sql = " SELECT DISTINCT stockdata.* FROM (SELECT SUBSTR(ts_code, 1, 6) AS STOCKCODE " \
              " FROM finance_system_stock_circulat_holds_data_%s " \
              " WHERE ts_code NOT IN (SELECT ts_code FROM finance_system_stock_circulat_holds_data_%s " \
              " WHERE holder_name = '%s')" \
              " AND holder_name ='%s' ) CODES" \
              " LEFT JOIN finance_system_basic_stock_data AS stockdata" \
              " ON stockdata. CODE = CODES.STOCKCODE" % (tableendid, tablestartid, holdername, holdername)
        conengine = dbmanager.sql_manager().init_engine()
        data = pd.read_sql_query(sql, conengine)
        return data

    def all_increase_hold_stock_infor(self, tablestartid, tableendid):
        pds = self.init_strong_stock_holder(tableendid)
        listholds = list(pds['holdername'])
        newdata = None
        for holdername in listholds:
            data = self.increase_hold_stock_infor(tablestartid, tableendid, holdername)
            if data.empty != True:
               newdata = pd.concat([newdata, data])
        engine = dbmanager.sql_manager().init_engine()
        pd.io.sql.to_sql(newdata, 'finance_system_stock_topholder_increase_data', con=engine, if_exists='replace',
                         index=False, chunksize=1000)
        engine.execute(" ALTER TABLE `finance_system_stock_topholder_increase_data` "
                       " MODIFY COLUMN `area`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL FIRST,"
                       " MODIFY COLUMN `code`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL AFTER `area`,"
                       " MODIFY COLUMN `industry`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL AFTER `holders`,"
                       " MODIFY COLUMN `name`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL AFTER `industry`; ")

    # 大庄家穿插
    def topten_holders_across_hold(self, tablestartid, tableendid):
        pds = self.init_strong_stock_holder(tableendid)
        listholds = list(pds.head(300)['holdername'])
        conengine = dbmanager.sql_manager().init_engine()
        newdata = None
        for holdcomb in combinations(listholds, 2):
            holdonename = holdcomb[0]
            holdtwoname = holdcomb[1]
            sql = " SELECT *  FROM ( SELECT DISTINCT * FROM( SELECT SUBSTR(ts_code, 1, 6) AS STOCKCODE FROM" \
                  " finance_system_stock_circulat_holds_data_%s WHERE ts_code NOT IN" \
                  " ( SELECT ts_code FROM finance_system_stock_circulat_holds_data_%s" \
                  " WHERE holder_name = '%s')" \
                  " AND holder_name = '%s') CODES" \
                  " LEFT JOIN finance_system_basic_stock_data AS stockdata ON stockdata. CODE = CODES.STOCKCODE" \
                  " UNION ALL" \
                  " SELECT DISTINCT * FROM (SELECT SUBSTR(ts_code, 1, 6) AS STOCKCODE" \
                  " FROM finance_system_stock_circulat_holds_data_%s " \
                  " WHERE ts_code NOT IN (SELECT ts_code FROM finance_system_stock_circulat_holds_data_%s " \
                  " WHERE holder_name = '%s' ) AND holder_name = '%s') CODES" \
                  " LEFT JOIN finance_system_basic_stock_data AS stockdata ON stockdata. CODE = CODES.STOCKCODE)" \
                  " ALLSDATA GROUP BY ALLSDATA.STOCKCODE" \
                  " HAVING COUNT(ALLSDATA.STOCKCODE) > 1 " % (tableendid, tablestartid, holdonename, holdonename,
                                                              tableendid, tablestartid, holdtwoname, holdtwoname)
            print (sql)
            data = pd.read_sql_query(sql, conengine)
            if data.empty!=True:
                newdata = pd.concat([newdata,data])
        #去除重复项
        newdata.drop_duplicates(subset='STOCKCODE', keep='first', inplace=True)
        engine = dbmanager.sql_manager().init_engine()
        pd.io.sql.to_sql(newdata,'finance_system_stock_holder_across_data',con=engine,if_exists='replace',index=False,chunksize=1000)
        engine.execute(" ALTER TABLE `finance_system_stock_holder_across_data` "
                       " MODIFY COLUMN `STOCKCODE`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL FIRST ,"
                       " MODIFY COLUMN `area`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL AFTER `STOCKCODE`,"
                       " MODIFY COLUMN `code`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL AFTER `area`,"
                       " MODIFY COLUMN `industry`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL AFTER `holders`,"
                       " MODIFY COLUMN `name`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL AFTER `industry`; ")




if __name__ == '__main__':
    # current_start_date='20180301'
    # current_start_date = '20180630'

    #current_table_start_id = '20180630'
    #current_table_end_id = '20180830'

    current_table_start_id = '20180830'
    current_table_end_id = '20181030'

    #current_holdname = '徐开东'
    # stock_topten_holdlers_change().init_strong_stock_holder(current_start_date)
    # stock_topten_holdlers_change().increase_hold_stock_infor(current_table_start_id,current_table_end_id,current_holdname)
    # stock_topten_holdlers_change().topten_holders_across_hold(current_table_start_id, current_table_end_id)
    stock_topten_holdlers_change().all_increase_hold_stock_infor(current_table_start_id, current_table_end_id)

# coding=utf-8
import tushare as tu
import pandas as pd
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from decimal import Decimal
import decimal
from sqlalchemy import func
import matplotlib.pyplot as plt
from finance_common_utils.common_utils.datetime_model import datetime_utils as dateutils
from finance_stock_dao_model.topten_holders_circulat_extdata_dto import topten_holders_circulat_extdata_dto as extdata

class topten_holders_radio_object(object):



    def research_current_circulates_ratio(self,tableId):
        conengine = dbmanager.sql_manager().init_engine()
        sql = " SELECT SS.SUMAMOUNT/100000000/DATAS.totals AS sum_circulat_radio," \
              " DATAS.code as st_code , DATAS.name as st_name " \
              " FROM finance_system_basic_stock_data DATAS " \
              " LEFT JOIN (SELECT SUBSTR(ts_code, 1, 6) AS STOCKCODE, sum(hold_amount) AS SUMAMOUNT" \
              " FROM finance_system_stock_circulat_holds_data_%s GROUP BY ts_code) AS SS" \
              " ON SS.STOCKCODE = DATAS.code" %(tableId)
        data = pd.read_sql_query(sql, conengine)
        conengine.execute('delete from finance_system_topten_holders_circulat_extdata')
        for i in range(0,len(data)):
            sum_circulat_radio = data.iloc[i]['sum_circulat_radio']
            st_code = data.iloc[i]['st_code']
            st_name = data.iloc[i]['st_name']
            vo = extdata(st_code=st_code,st_name=st_name,sum_circulat_radio=sum_circulat_radio)
            dbmanager.sql_manager().single_common_save_basedata(vo)


if __name__ == '__main__':
    start_table_id='20180830'
    topten_holders_radio_object().research_current_circulates_ratio(start_table_id)
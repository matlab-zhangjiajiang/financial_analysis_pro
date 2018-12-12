# coding=utf-8
import tushare as tu
import pandas as pd
import numpy as np
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from decimal import Decimal
import decimal
from sqlalchemy import func
import matplotlib.pyplot as plt
from finance_common_utils.common_utils.datetime_model import datetime_utils as dateutils
from finance_stock_dao_model.stock_infor_bigplate_dto import stock_infor_bigplate_dto as bigplate
from finance_stock_dao_model.stock_infor_base_dto import stock_infor_base_dto as stockbaseinfo
import init_current_stock_infor as initstock

##https://www.cnblogs.com/xiaonq/p/8420826.html

class init_bigplate_infor(object):


    def init_basic_stock_infor(self):
        initstock.init_stock_infor().init_stock_basic_data()


    def init_current_bigplate_info(self):
        ##获取当前所有的上市公司数量.
        session = dbmanager.sql_manager().open_session()
        res = session.query(func.count(stockbaseinfo.code)).scalar()
        pbres = session.query(func.count(stockbaseinfo.code)).filter(stockbaseinfo.pb<1).scalar()
        peres = session.query(func.count(stockbaseinfo.code)).filter(stockbaseinfo.pe<20).scalar()
        index = dateutils.datetimeutils().get_current_time_new()
        decimal.getcontext().prec =4
        brokenpb = Decimal(pbres)/Decimal(res)
        peratio = Decimal(peres)/Decimal(res)
        current_rs = session.query(bigplate).filter(bigplate.dateid == index).all()
        if len(current_rs) ==0:
           vo = bigplate(dateid=index, broken_pb_ratio=brokenpb, pe_ratio=peratio)
           dbmanager.sql_manager().single_common_save_basedata(vo)
        dbmanager.sql_manager().close_current_session(session)


    def current_bigplate_infor_show(self):
        conengine = dbmanager.sql_manager().init_engine()
        ##finance_system_basic_bigplate_data
        sql ="select  *  from  finance_system_basic_bigplate_data"
        data = pd.read_sql_query(sql,conengine)
        indexlist = list(data['dateid'])
        pbratios = data.broken_pb_ratio.T.values.astype(float)
        newdata = pd.DataFrame({'broken_pb_ratio': pbratios}, index=pd.to_datetime(indexlist))
        newdata.plot(title='Broken Pb Show')
        plt.show()

if __name__ == '__main__':
    init_bigplate_infor().init_basic_stock_infor()
    init_bigplate_infor().init_current_bigplate_info()
    #init_bigplate_infor().current_bigplate_infor_show()

#coding=utf-8
from sqlalchemy import Column, Integer, String, Text ,Float,DateTime,FLOAT
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


#集合竞价集合数据.
class stock_dayly_increase_holder_dto(Base):

    __tablename__ = 'finance_system_stock_dayly_increase_holder_data'
    mainkey = Column(String(32), primary_key=True)
    stock_code = Column(String(10))
    stock_name = Column(String(20))
    current_price = Column(FLOAT(10,2))
    up_and_down = Column(FLOAT(10,2))
    holder_name = Column(String(200))
    mark_flag = Column(Integer())
    cgbd_bd_num = Column(FLOAT(12,2))
    cgbd_zzgb_ratio = Column(FLOAT(5,2))
    cgbd_zltg_ratio = Column(FLOAT(5,2))
    bdhcd_cg_sum_num = Column(FLOAT(12,2))
    bdhcd_zzgb_ratio = Column(FLOAT(5,2))
    bdhcd_cltg_num = Column(FLOAT(12,2))
    bdhcd_zltg_ratio = Column(FLOAT(5,2))
    bd_start_date = Column(DateTime)
    bd_end_date = Column(DateTime)
    gg_date = Column(DateTime)
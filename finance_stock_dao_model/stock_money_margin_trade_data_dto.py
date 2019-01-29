#coding=utf-8
from sqlalchemy import Column, Integer, String, Text ,Float,DateTime,FLOAT
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class stock_money_margin_trade_data_dto(Base):

    __tablename__ = 'finance_system_stock_money_margin_trade_data'

    trade_date = Column(String(32),primary_key=True)
    hushen_300_index = Column(Float(15,2))
    up_down_point = Column(Float(4,2))
    rz_drye = Column(Float(20,2))
    rz_drye_zltszb = Column(Float(5,2))
    rz_sr_mre = Column(Float(20, 2))
    rz_sr_che = Column(Float(20, 2))
    rz_sr_jmr = Column(Float(20, 2))
    rq_drye = Column(Float(20, 2))
    rq_dryl = Column(Float(20, 2))
    rq_sr_mcl = Column(Float(20, 2))
    rq_sr_chl = Column(Float(20, 2))
    rq_sr_jmc = Column(Float(20, 2))
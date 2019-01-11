#coding=utf-8
from sqlalchemy import Column, Integer, String, Text ,Float,DateTime,FLOAT
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class stock_money_flow_dto(Base):

    __tablename__ = 'finance_system_stock_money_flow_data'

    trade_date = Column(String(32),primary_key=True)
    ggt_ss = Column(FLOAT(15,2))
    ggt_sz = Column(FLOAT(15,2))
    hgt = Column(FLOAT(15,2))
    sgt =Column(FLOAT(15,2))
    north_money = Column(FLOAT(15, 2))
    south_money = Column(FLOAT(15, 2))
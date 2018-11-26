#coding=utf-8
from sqlalchemy import Column, Integer, String, Text ,Float,DateTime,FLOAT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class stock_set_bid_base_rate_dto(Base):

    __tablename__ = 'finance_system_stock_set_bid_data_rate'

    code = Column(String(32), primary_key=True)
    industry = Column(String(100))
    name = Column(String(100))
    createtime = Column(DateTime)
    outstanding = Column(FLOAT(15,2))
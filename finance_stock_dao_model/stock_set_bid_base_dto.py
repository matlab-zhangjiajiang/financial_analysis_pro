#coding=utf-8
from sqlalchemy import Column, Integer, String, Text ,Float,DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

###集合竞价集合数据.
class stock_set_bid_base_dto(Base):

    __tablename__ = 'finance_system_stock_set_bid_data'
    mainkey = Column(String(32), primary_key=True)
    code = Column(String(32))
    industry = Column(String(150))
    name = Column(String(100))
    createtime = Column(DateTime)
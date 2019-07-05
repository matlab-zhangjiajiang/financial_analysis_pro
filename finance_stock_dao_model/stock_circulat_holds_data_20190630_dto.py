#coding=utf-8
from sqlalchemy import Column, Integer, String, Text ,Float,DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class stock_circulat_holds_data_20190630_dto(Base):

    __tablename__ = 'finance_system_stock_circulat_holds_data_20190630'

    stock_code = Column(String(32))
    info_url = Column(String(150))
    info_title = Column(String(200),primary_key=True)
    key_time = Column(DateTime)
    news_flag = Column(Integer())
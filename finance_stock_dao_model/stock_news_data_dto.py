#coding=utf-8
from sqlalchemy import Column, Integer, String, Text ,Float,DateTime,FLOAT
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class stock_news_data_dto(Base):

    __tablename__ = 'finance_system_stock_news_data'

    index_date = Column(String(32))
    context = Column(String(500))
    href = Column(String(100),primary_key=True)
    news_platform = Column(String(10))
    create_time =Column(DateTime)
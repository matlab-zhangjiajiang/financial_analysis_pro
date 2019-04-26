#coding=utf-8
from sqlalchemy import Column, Integer, String, Text ,Float,DateTime,FLOAT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class stock_core_words_data_dto(Base):

    __tablename__ = 'finance_system_stock_core_words_data'

    core_word = Column(String(225),primary_key=True)
    word_weight = Column(Integer())

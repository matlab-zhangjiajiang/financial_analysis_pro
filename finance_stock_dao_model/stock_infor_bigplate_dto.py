#coding=utf-8
from sqlalchemy import Column, Integer, String, Text ,Float,DateTime,FLOAT
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class stock_infor_bigplate_dto(Base):

    __tablename__ = 'finance_system_basic_bigplate_data'

    dateid = Column(String(10), primary_key=True)
    broken_pb_ratio = Column(FLOAT(10,5))
    pe_ratio = Column(FLOAT(10,5))
#coding=utf-8
from sqlalchemy import Column, Integer, String, Text ,Float,DateTime,FLOAT
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class current_table_dto(Base):

    __tablename__ = 'finance_system_stock_topten_holders_newimport'

    mainkey = Column(String(32),primary_key=True)
    company_code = Column(String(50))
    ssname = Column(String(50))
    sharehdname = Column(String(50))
    sharehdtype = Column(String(50))
    sharestype = Column(String(50))
    rank = Column(String(10))
    scode = Column(String(15))
    sname = Column(String(30))
    rdate = Column(DateTime)
    sharehdnum = Column(FLOAT(15, 2))
    ltag = Column(FLOAT(15, 2))
    zb = Column(FLOAT(17,15))
    ndate = Column(DateTime)
    bz = Column(String(10))
    bdbl = Column(String(100))
    sharehdcode = Column(String(50))
    sharehdratio = Column(FLOAT(10,8))
    bdsum = Column(String(50))
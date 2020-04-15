#coding=utf-8
from sqlalchemy import Column, Integer, String, Text ,Float,DateTime,FLOAT
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class stock_money_flow_dto(Base):

    __tablename__ = 'finance_system_stock_topten_holders_newimport'

    mainkey = Column(String(32),primary_key=True)
    company_code = Column(String(50))
    ssname = Column(String(50))
    sharehdname = Column(String(50))
    sharehdtype = Column(FLOAT(15,2))
    sharestype = Column(FLOAT(15, 2))
    rank = Column(FLOAT(15, 2))
    scode = Column(FLOAT(15, 2))
    sname = Column(FLOAT(15, 2))
    rdate = Column(FLOAT(15, 2))
    sharehdnum = Column(FLOAT(15, 2))
    ltag = Column(FLOAT(15, 2))
    zb = Column(FLOAT(15, 2))
    ndate = Column(FLOAT(15, 2))
    bz = Column(FLOAT(15, 2))
    bdbl = Column(FLOAT(15, 2))
    sharehdcode = Column(FLOAT(15, 2))
    sharehdratio = Column(FLOAT(15, 2))
    bdsum = Column(FLOAT(15, 2))
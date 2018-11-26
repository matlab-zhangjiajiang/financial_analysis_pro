#coding=utf-8
from sqlalchemy import Column, Integer, String, Text ,Float,DateTime,FLOAT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class topten_holders_circulat_extdata_dto(Base):

    __tablename__ = 'finance_system_topten_holders_circulat_extdata'

    st_code = Column(String(32), primary_key=True)
    st_name = Column(String(32))
    sum_circulat_radio = Column(FLOAT(15,8))
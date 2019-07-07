#coding=utf-8
from sqlalchemy import Column, Integer, String, Text ,Float,DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class stock_circulat_holds_data_20190630_dto(Base):

    __tablename__ = 'finance_system_stock_circulat_holds_data_20190630'
    id = Column(String(100),primary_key=True)
    ts_code = Column(String(32))
    ann_date = Column(DateTime)
    end_date = Column(DateTime)
    holder_name = Column(String(150))
    hold_amount = Column(Float(15,2))
    holder_nature = Column(String(150))
    stock_type = Column(String(50))
    zzltg_cg_ratio = Column(Float(5,2))
    zj_state = Column(String(50))
    bd_ratio = Column(Float(5,2))
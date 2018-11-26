#coding=utf-8
from sqlalchemy import Column, String, Text ,Float
from sqlalchemy.ext.declarative import declarative_base
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from sqlalchemy.orm import scoped_session

Base = declarative_base()

class stock_infor_base_dto(Base):

    __tablename__ = 'finance_system_basic_stock_data'

    code = Column(String(32), primary_key=True)
    area = Column(String(32))
    industry = Column(Text)
    name = Column(Text)
    outstanding = Column(Float)
    pb = Column(Float)
    pe = Column(Float)

    def get_basic_stock_infor(self):
        Session = scoped_session(dbmanager.sql_manager().open_session_factory())
        session = Session()
        data = session.query(stock_infor_base_dto).all()
        session.close()
        return data


if __name__ == '__main__':
    Session = scoped_session(dbmanager.sql_manager().open_session_factory())
    session = Session()
    for row in session.query(stock_infor_base_dto).all():
        print(row.name)
    session.close()
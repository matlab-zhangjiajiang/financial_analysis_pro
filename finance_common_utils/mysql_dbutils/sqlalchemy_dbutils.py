#coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

class sql_manager(object):

    def init_engine(self):
        try:
            return create_engine('mysql://root:yougou@127.0.0.1/finance_db?charset=utf8',echo=True)
        except Exception as error:
            print("open connection database catch Error.", error)

    def open_session_factory(self):
        try:
            return sessionmaker(bind=self.init_engine())
        except Exception as error:
            print("open session factory catch Error.",error)


    def single_session_commit(self,session):
        try:
            session.commit()
        except Exception as error:
            print('commit error',error)
            session.rollback()
        session.close()


    def open_session(self):
        current_dbmanager = sql_manager()
        Session = scoped_session(current_dbmanager.open_session_factory())
        session = Session()
        return session


    def close_current_session(self,session):
        if session is not None:
            session.close()


    #单个对象提交.
    def single_common_save_basedata(self,vo):
        current_dbmanager = sql_manager()
        Session = scoped_session(current_dbmanager.open_session_factory())
        session = Session()
        session.add(vo)
        current_dbmanager.single_session_commit(session)
        session.close()

    #查询当前所有的封装对象.
    def common_get_all_basedata(self,dto):
        current_dbmanager = sql_manager()
        Session = scoped_session(current_dbmanager.open_session_factory())
        session = Session()
        data = session.query(dto).all()
        session.close()
        return data
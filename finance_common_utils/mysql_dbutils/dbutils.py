#coding=utf-8
import MySQLdb

class dbutils(object):

    def getDBconn(self):
        mysql_conn = MySQLdb.connect(host='10.0.30.201',port=3306,user='belle',passwd='belle@belle',db='cds_big_data',charset='utf8')
        return mysql_conn

    def closeDBconn(self,dbconn):
        dbconn.close()


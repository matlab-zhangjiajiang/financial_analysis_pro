#coding=utf-8
import jieba
import jieba.analyse
import pandas as pd
import tushare as tu
import os
import sys
from collections import Counter
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from finance_news_report_analysis.utils import spider_common_utils as utils


#新增关键词
# 设置TOKEN
tu.set_token('b2d9cda1ccac47a845fc2dd31e41a39185bfa43d5b6fa110fddf21e2')
# 设置PRO-API
pro = tu.pro_api()

def words_frequency_count():
    worddict={}
    stopwords=[]

    basicdata = tu.get_stock_basics()
    for idx,row in basicdata.iterrows():
        jieba.add_word(row['name'])
        jieba.add_word(idx)
        stopwords.append(row['name'].replace(' ',''))
        #stopwords.append(idx.replace(' ',''))


    conengine = dbmanager.sql_manager().init_engine()
    sql ='SELECT * FROM finance_system_stock_news_data WHERE DATE(CREATE_TIME) = CURDATE()'
    df = pd.read_sql_query(sql,conengine)
    df = df[df.context.isnull() == False]
    for idx, row in df.iterrows():
        context = row['context']
        word_list = jieba.cut(context,cut_all=False)
        for kv in word_list:
            kv = kv.replace(' ','')
            if kv in stopwords:
               if kv not in worddict:
                  worddict[kv] = 1
               else:
                  worddict[kv] = worddict[kv]+1
    result = pd.DataFrame({'key':[x for x in worddict.keys()],'value':[x for x in worddict.values()]}).sort_values(['value'],ascending=[False])
    engine = dbmanager.sql_manager().init_engine()
    pd.io.sql.to_sql(result, 'finance_system_stock_word_frequency_data', con=engine, if_exists='replace', index=False,
                 chunksize=1000)
    engine.execute('ALTER TABLE `finance_system_stock_word_frequency_data` '
                   'MODIFY COLUMN `key`  varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL FIRST')


if __name__ == '__main__':
    words_frequency_count()
#coding=utf-8
import jieba
import jieba.analyse
import pandas as pd
import tushare as tu
import os
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
import sys
sys.getdefaultencoding()
#新增关键词
stopwords_dict = ['雄安新区', '区块链', '数字货币', '虚拟货币',  '比特币', '对冲基金', '自贸区', '自由贸易区','乡村振兴','美丽中国','共享经济','租购同权','新零售',
             '共有产权房','楼市调控', '产权保护', '互联网金融', '5G', '4G', '国企改革', '大湾区', '长江经济带','一带一路']


# 设置TOKEN
tu.set_token('b2d9cda1ccac47a845fc2dd31e41a39185bfa43d5b6fa110fddf21e2')
# 设置PRO-API
pro = tu.pro_api()

def words_frequency_count():
    worddict={}
    stopwords=[]
    for word in stopwords_dict:
        jieba.add_word(word)
        stopwords.append(word)

    basicdata = tu.get_stock_basics()
    for idx,row in basicdata.iterrows():
        jieba.add_word(row['name'])
        jieba.add_word(idx)
        stopwords.append(row['name'].replace(' ',''))
        #stopwords.append(idx.replace(' ',''))

    conengine = dbmanager.sql_manager().init_engine()
    sql ='SELECT * FROM FINANCE_SYSTEM_STOCK_NEWS_DATA WHERE DATE(CREATE_TIME) = CURDATE()'
    df = pd.read_sql_query(sql,conengine)
    df = df[df.context.isnull() == False]
    for idx, row in df.iterrows():
        context = row['context']
        word_list = jieba.analyse.extract_tags(context, topK=3)
        for kv in word_list:
            if kv not in worddict:
               worddict[kv] = 1
            else:
               worddict[kv] = worddict[kv]+1
    result = pd.DataFrame({'key':[x for x in worddict.keys()],'value':[x for x in worddict.values()]}).sort_values(['value'],ascending=[False])
    engine = dbmanager.sql_manager().init_engine()
    pd.io.sql.to_sql(result, 'finance_system_news_word_frequency_data', con=engine, if_exists='replace', index=False,
                 chunksize=1000)



if __name__ == '__main__':
    words_frequency_count()
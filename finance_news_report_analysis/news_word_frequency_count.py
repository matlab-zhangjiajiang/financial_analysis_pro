#coding=utf-8
import jieba
import jieba.analyse
import pandas as pd
import tushare as tu
import os
from collections import Counter
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
import utils.spider_common_utils as utils
#过滤关键词
blacklist = ['责任编辑', '一定','一年', '一起', '一项', '一点儿', '一度','一系列','一道','一次','一亿','进行', '实现', '已经', '指出',
            '为什么', '是不是', '”', '一个', '一些', 'cctv', '一边', '一部', '一致', '一窗', '万亿元', '亿元', '一致同意', '本台记住', '发生', 
            '上述', '不仅', '不再 ', '下去', '首次', '合作', '发展', '国家', '加强', '共同', '重要', '我们', '你们', '他们', '目前',
            '领导人', '推进', '中方', '坚持', '支持', '表示', '时间', '协调', '时间', '制度', '工作', '强调', '进行', '推动', '通过',
            '北京时间', '有没有', '新闻联播', '本台消息', '这个', '那个', '就是', '今天', '明天', '参加', '今年', '明天']

#新增关键词
stopwords_dict = ['一带一路', '雄安新区', '区块链', '数字货币', '虚拟货币',  '比特币', '对冲基金', '自贸区', '自由贸易区','乡村振兴','美丽中国','共享经济','租购同权','新零售',
             '共有产权房','楼市调控', '产权保护', '互联网金融', '5G', '4G', '国企改革', '大湾区', '长江经济带']


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
        stopwords.append(row['name'])
        stopwords.append(idx)

    project_path = os.path.dirname(os.path.realpath(__file__))
    url = project_path+'\\main_word_dict.txt.big'
    stop_url = project_path+'\\stop_word_dict.txt'
    ##新的词义写入到当前的文档
    writefile = open(url, 'a')
    #writefile.truncate()
    for adddata in stopwords:
        writefile.write('\n' + adddata+' 11.598092559')

    jieba.analyse.set_stop_words(stop_url)
    #jieba.analyse.set_idf_path(url)
    conengine = dbmanager.sql_manager().init_engine()
    sql ='SELECT * FROM FINANCE_SYSTEM_STOCK_NEWS_DATA WHERE DATE(CREATE_TIME) = CURDATE()'
    df = pd.read_sql_query(sql,conengine)
    df = df[df.context.isnull() == False]
    for idx, row in df.iterrows():
        context = row['context']
        word_list = jieba.analyse.extract_tags(context, topK=100, withWeight=False, allowPOS=('n','nr','ns'))
        for kv in word_list:
            if kv not in worddict:
               worddict[kv] = 1
            else:
               worddict[kv] = worddict[kv]+1
    result = pd.DataFrame({'key':[x for x in worddict.keys()],'value':[x for x in worddict.values()]}).sort_values(['value'],ascending=[False])
    print(result)
    #engine = dbmanager.sql_manager().init_engine()
    #pd.io.sql.to_sql(result, 'finance_system_news_word_frequency_data', con=engine, if_exists='replace', index=False,
    #             chunksize=1000)

if __name__ == '__main__':
    words_frequency_count()
# coding=utf-8
# 定时调度机制
from apscheduler.schedulers.blocking import BlockingScheduler
from finance_stock_tushare_utils.stock_basic_data import init_current_bigplate_infor as bigplate
# from finance_stock_tushare_utils.stock_large_holders_data import holdlers_change_data as holderchange
from finance_stock_tushare_utils.stock_large_holders_data import hodlers_topten_data as top10change
from finance_news_report_analysis import spider_stock_notice_utils as remanager
from finance_news_report_analysis import stock_news_research_utils as newsmanager
from finance_news_report_analysis import spider_web_news_utils as webmaneger
from finance_news_report_analysis import news_word_frequency_count as wordsearch
from finance_news_report_analysis import stock_word_frequency_count as stockwordsearch
from finance_stock_tushare_utils.stock_money_flow_data import stock_money_flow_initdata as flowdata
from finance_stock_tushare_utils.stock_money_flow_data import stock_money_margin_trade_data as margindata
from finance_stock_common_spider.eastmoney_datacenter_spider import dayly_increase_holders as daylyincrease
from finance_stock_common_spider.eastmoney_datacenter_spider import top_ten_holders_new_import as newimport
from finance_stock_common_spider.eastmoney_datacenter_spider import top_ten_holders_current_add as currentadd
from finance_stock_pytdx_utils import stock_set_bid_price as setbidprice
from finance_news_report_analysis import notice_constant as constant
from finance_common_utils.common_utils import Logger as loggers

sched = BlockingScheduler()

logger = loggers.Logger(logname='log.txt', loglevel=1, logger="main_job").getlog()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=12, minute=30, end_date='2089-04-24')
def holders_across_holdes_job():
    holder = top10change.stock_circulat_holdlers()
    holder.init_stock_holders_topten()


# 南上北下资金流向--融资融券信息
@sched.scheduled_job('interval', seconds=3600)
def init_stock_money_flow_data_job():
    flowdatajob = flowdata.stock_money_flow_data()
    flowdatajob.init_money_flow_data()
    # 融资融券数据
    margindata.init_stock_money_margin()


# 新闻及时爬取
@sched.scheduled_job('interval', seconds=480)
def init_current_stock_news_data():
    webmaneger.daily_wallstreetcn_spider()
    webmaneger.daily_tonghuasun_spider()
    webmaneger.daily_eastmoney_spider()
    webmaneger.daily_yuncaijing_spider()
    webmaneger.daily_sina_spider()
    # 词频分析
    wordsearch.words_frequency_count()
    stockwordsearch.words_frequency_count()


# [公告信息]---->有利
@sched.scheduled_job('interval', seconds=1200)
def news_report_research_job():
    jobone = remanager.exchange_stock_notice_manager()
    spidernotices = jobone.get_announcement_all_notice()
    constantdict = constant.notice_constant()
    jobtwo = newsmanager.stock_news_research_utils(spidernotices)
    # 利好消息
    jobtwo.study_stock_notice_news(constantdict.GOOD_NEWS_FLAG)
    jobtwo.select_current_news_stock(constantdict.GOOD_NEWS_FLAG)
    # 利空消息
    jobtwo.study_stock_notice_news(constantdict.BAD_NEWS_FLAG)
    jobtwo.select_current_news_stock(constantdict.BAD_NEWS_FLAG)


# 每日股东增持情况.
@sched.scheduled_job('interval', seconds=1200)
def dayly_increase_holders_job():
    # 每日股东增持
    daylyincrease.dayly_increase_holders().get_dayly_increase_holders_raw_data()
    # 每日股东新增
    newimport.top_ten_holders_new_import.get_dayly_add_topten_holders_raw_data()
    # 流通股东前十(当前流通股东在原有基础上增加)
    currentadd.top_ten_holders_current_add.get_topten_holders_current_add_row_data()


# 表示从星期一到星期五下午19:30（AM）直到2089-04-24 00:00:00
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=19, minute=30, end_date='2089-04-24')
def init_current_day_pe_job():
    plate = bigplate.init_bigplate_infor()
    plate.init_basic_stock_infor()
    plate.init_current_bigplate_info()


# 集合竞价大于1000手的股票序列.
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=9, minute=40, end_date='2089-04-24')
def init_current_set_bid_price_jon():
    setbidjob = setbidprice.stock_set_bid_price()
    # 开盘每笔成交数大于1000手
    setbidjob.init_bid_price_stock(1000)


# 爬取
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=21, minute=30, end_date='2089-04-24')
def init_cron_top_ten_circulate_holder():
    print('--------------')


logger.info('sched----->start---->job')
sched.start()

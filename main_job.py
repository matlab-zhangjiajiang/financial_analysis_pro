#coding=utf-8
#定时调度机制
from apscheduler.schedulers.blocking import BlockingScheduler
from finance_stock_tushare_utils.stock_basic_data import init_current_bigplate_infor as bigplate
from finance_stock_tushare_utils.stock_large_holders_data import holdlers_change_data as holderchange
from finance_news_report_analysis import spider_stock_notice_utils as remanager
from finance_news_report_analysis import stock_news_research_utils as newsmanager
from finance_news_report_analysis import spider_web_news_utils as webmaneger
from finance_news_report_analysis import news_word_frequency_count as wordsearch
from finance_news_report_analysis import stock_word_frequency_count as stockwordsearch
from finance_stock_tushare_utils.stock_money_flow_data import stock_money_flow_initdata as flowdata
from finance_stock_tushare_utils.stock_money_flow_data import stock_money_margin_trade_data as margindata
from finance_news_report_analysis import notice_research_constant as constant
from finance_common_utils.common_utils import loggger_factory as loggers


sched = BlockingScheduler()
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

logger = loggers.Logger(logname='log.txt', loglevel=1, logger="main_job").getlog()

@sched.scheduled_job('cron',day_of_week='mon-fri', hour=17, minute=30,end_date='2089-04-24')
def holders_across_holdes_job():
    holder = holderchange.stock_topten_holdlers_change()
    current_table_start_id = '20180301'
    current_table_end_id = '20180630'
    #holder.topten_holders_across_hold(current_table_start_id, current_table_end_id)


##南上北下资金流向--融资融券信息
@sched.scheduled_job('interval', seconds=3600)
def init_stock_money_flow_data_job():
    flowdatajob = flowdata.stock_money_flow_data()
    flowdatajob.init_money_flow_data()
    #融资融券数据
    margindata.init_stock_money_margin()



#新闻及时爬取
@sched.scheduled_job('interval', seconds=480)
def init_current_stock_news_data():
    webmaneger.daily_wallstreetcn_spider()
    webmaneger.daily_tonghuasun_spider()
    webmaneger.daily_eastmoney_spider()
    webmaneger.daily_yuncaijing_spider()
    #词频分析
    wordsearch.words_frequency_count()
    stockwordsearch.words_frequency_count()


@sched.scheduled_job('interval', seconds=120)
def crawl_sina_news_data_job():
    webmaneger.daily_sina_spider()


#[公告信息]---->有利
@sched.scheduled_job('interval', seconds=600)
def news_report_research_job():
    jobone = remanager.exchange_stock_notice_manager()
    spidernotices = jobone.get_announcement_all_notice()
    constantdict = constant.notice_research_constant()
    jobtwo = newsmanager.stock_news_research_utils(spidernotices)
    ##利好消息
    jobtwo.study_stock_notice_news(constantdict.get_good_dict_path())
    jobtwo.select_current_news_stock(constantdict.get_good_dict_path(),constantdict.GOOD_NEWS_FLAG)
    ##利空消息
    jobtwo.study_stock_notice_news(constantdict.get_bad_dict_path())
    jobtwo.select_current_news_stock(constantdict.get_bad_dict_path(), constantdict.BAD_NEWS_FLAG)


#表示从星期一到星期五下午19:30（AM）直到2089-04-24 00:00:00
@sched.scheduled_job('cron',day_of_week='mon-fri', hour=20, minute=30,end_date='2089-04-24')
def format_pe_job():
    plate = bigplate.init_bigplate_infor()
    plate.init_basic_stock_infor()
    plate.init_current_bigplate_info()

logger.info('sched----->start')
sched.add_job(format_pe_job,'cron',day_of_week='mon-fri', hour=20, minute=30,end_date='2089-04-24')
sched.start()
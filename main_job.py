#coding=utf-8
#定时调度机制
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from finance_stock_tushare_utils.stock_basic_data import init_current_bigplate_infor as bigplate
from finance_stock_tushare_utils.stock_large_holders_data import holdlers_change_data as holderchange
from finance_news_report_research import exchange_stock_notice as remanager
from finance_news_report_research import stock_news_research_utils as newsmanager
from finance_stock_tushare_utils.stock_money_flow_data import stock_money_flow_initdata as flowdata

sched = BlockingScheduler()
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#表示从星期一到星期五下午4:30（AM）直到2089-04-24 00:00:00
@sched.scheduled_job('cron',day_of_week='mon-fri', hour=17, minute=00,end_date='2089-04-24')
def format_pe_job():
    plate = bigplate.init_bigplate_infor()
    plate.init_basic_stock_infor()
    plate.init_current_bigplate_info()


@sched.scheduled_job('cron',day_of_week='mon-fri', hour=17, minute=30,end_date='2089-04-24')
def holders_across_holdes_job():
    holder = holderchange.stock_topten_holdlers_change()
    current_table_start_id = '20180301'
    current_table_end_id = '20180630'
    #holder.topten_holders_across_hold(current_table_start_id, current_table_end_id)


##南上北下资金流向
@sched.scheduled_job('interval', seconds=3600)
def init_stock_money_flow_data_job():
    flowdatajob = flowdata.stock_money_flow_data()
    flowdatajob.init_money_flow_data()


#公告信息利空
@sched.scheduled_job('interval', seconds=600)
def news_report_research_job():
    jobone = remanager.exchange_stock_notice_manager()
    jobone.get_announcement_all()
    jobtwo = newsmanager.stock_news_research_utils()
    jobtwo.study_stock_notice_news()


print('sched----->start')
sched.start()
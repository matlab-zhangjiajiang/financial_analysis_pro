# coding=utf-8
import tushare as tu
import pandas as pd
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
import init_current_bigplate_infor  as manager

###获取股票市场基础信息
class init_stock_infor(object):
    # 设置TOKEN
    tu.set_token('b2d9cda1ccac47a845fc2dd31e41a39185bfa43d5b6fa110fddf21e2')
    # 设置PRO-API
    pro = tu.pro_api()

    ##获取股票基础信息.
    def init_stock_basic_data(self):

        basicdata = tu.get_stock_basics()

        createdata = pd.DataFrame({'code':list(basicdata.index),
                                   'name':list(basicdata['name']),
                                   'industry':list(basicdata['industry']),
                                   'area':list(basicdata['area']),
                                   'outstanding': list(basicdata['outstanding']*100000000),
                                   'pe':list(basicdata['pe']),
                                   #总股本(亿)
                                   'totals':list(basicdata['totals']),
                                   #总资产(万)
                                   'totalAssets': list(basicdata['totalAssets']),
                                   #流动资产
                                   'liquidAssets': list(basicdata['liquidAssets']),
                                   #固定资产
                                   'fixedAssets': list(basicdata['fixedAssets']),
                                   #公积金
                                   'reserved': list(basicdata['reserved']),
                                   #每股公积金
                                   'reservedPerShare': list(basicdata['reservedPerShare']),
                                   #每股收益
                                   'esp': list(basicdata['esp']),
                                   #每股净资
                                   'bvps': list(basicdata['bvps']),
                                   #未分利润
                                   'undp': list(basicdata['undp']),
                                   #每股未分配
                                   'perundp': list(basicdata['perundp']),
                                   #收入同比(%)
                                   'rev': list(basicdata['rev']),
                                   #利润同比(%)
                                   'profit': list(basicdata['profit']),
                                   #毛利率(%)
                                   'gpr': list(basicdata['gpr']),
                                   #净利润率(%)
                                   'npr': list(basicdata['npr']),
                                   'pb': list(basicdata['pb']),
                                   'holders':list(basicdata['holders'])},
                                  index=list(basicdata.index))
        engine = dbmanager.sql_manager().init_engine()
        pd.io.sql.to_sql(createdata,'finance_system_basic_stock_data',con=engine,if_exists='replace',index=False,chunksize=1000)
        engine.execute('ALTER TABLE `finance_system_basic_stock_data` '
                       'MODIFY COLUMN `area`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL FIRST ,'
                       'MODIFY COLUMN `code`  varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL AFTER `area`,'
                       'MODIFY COLUMN `industry`  varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL AFTER `holders`, '
                       'MODIFY COLUMN `name`  varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL AFTER `industry` , '
                       'ADD PRIMARY KEY (`code`)')
        engine.execute("ALTER TABLE `finance_system_basic_stock_data` "
                       "MODIFY COLUMN `outstanding`  double NULL DEFAULT NULL COMMENT '流通市值' AFTER `name`,"       
                       "MODIFY COLUMN `totals`  double NULL DEFAULT NULL COMMENT '总股本(亿)' AFTER `outstanding`,"
                       "MODIFY COLUMN `totalAssets`  double NULL DEFAULT NULL COMMENT '总资产(万)' AFTER `totals`,"
                       "MODIFY COLUMN `liquidAssets`  double NULL DEFAULT NULL COMMENT '流动资产' AFTER `totalAssets`,"
                       "MODIFY COLUMN `fixedAssets`  double NULL DEFAULT NULL COMMENT '流通市值' AFTER `liquidAssets`,"
                       "MODIFY COLUMN `reserved`  double NULL DEFAULT NULL COMMENT '公积金' AFTER `fixedAssets`")
        engine.execute("ALTER TABLE `finance_system_basic_stock_data` "
                       " MODIFY COLUMN `reservedPerShare`  double NULL DEFAULT NULL COMMENT '每股公积金' AFTER `reserved`,"
                       " MODIFY COLUMN `esp`  double NULL DEFAULT NULL COMMENT '每股收益' AFTER `reservedPerShare`,"
                       " MODIFY COLUMN `bvps`  double NULL DEFAULT NULL COMMENT '每股净资' AFTER `esp`,"
                       " MODIFY COLUMN `undp`  double NULL DEFAULT NULL COMMENT '未分利润' AFTER `bvps`,"
                       " ADD INDEX `code_index` (`code`) USING BTREE")

        manager.init_bigplate_infor().init_current_bigplate_info()



if __name__ == '__main__':
    init_stock_infor().init_stock_basic_data()
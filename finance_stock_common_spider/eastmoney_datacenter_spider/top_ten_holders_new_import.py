#utf-8
import requests
import json
from finance_stock_common_spider.eastmoney_datacenter_spider import spider_data_web_address as address
from finance_common_utils.mysql_dbutils import sqlalchemy_dbutils as dbmanager
from finance_stock_dao_model.stock_topten_holders_new_import_dto import current_table_dto  as daylydata


class top_ten_holders_new_import(object):

    def get_dayly_add_topten_holders_raw_data(self):
        response = requests.get(address.spider_web_address().DATA_URL['TOP_TEN_HOLDER_ADDER'])
        current_data = str(response.text)
        data = current_data.find('DlswLagO =')+11
        message = current_data[data:-1].replace('pages','\"pages\"').replace('data','\"data\"')
        raw_data = json.loads(message)
        data = raw_data['data']
        for cdata in data:
            company_code = cdata['COMPANYCODE']
            ssname = cdata['SSNAME']
            sharehdname = cdata['SHAREHDNAME']
            sharehdtype = cdata['SHAREHDTYPE']
            sharestype = cdata['SHARESTYPE']
            rank = cdata['RANK']
            scode = cdata['SCODE']
            sname = cdata['SNAME']
            rdate = cdata['RDATE'].replace('T',' ')
            sharehdnum = cdata['SHAREHDNUM']
            ltag = cdata['LTAG']
            zb = cdata['ZB']
            ndate = cdata['NDATE'].replace('T',' ')
            bz = cdata['BZ']
            bdbl = cdata['BDBL']
            sharehdcode = cdata['SHAREHDCODE']
            sharehdratio =cdata['SHAREHDRATIO']
            bdsum = cdata['BDSUM']
            mainkey = sharehdcode
            vo = daylydata(mainkey=mainkey, company_code=company_code, ssname=ssname, sharehdname=sharehdname,
                           sharehdtype=sharehdtype, sharestype=sharestype, rank=rank, scode=scode,
                           sname=sname, rdate=rdate, sharehdnum=sharehdnum,
                           ltag=ltag, zb=zb, ndate=ndate,
                           bz=bz, bdbl=bdbl, sharehdcode=sharehdcode,sharehdratio=sharehdratio,bdsum=bdsum)
            dbmanager.sql_manager().single_common_save_basedata(vo)



if __name__ == '__main__':
    top_ten_holders_new_import().get_dayly_add_topten_holders_raw_data()

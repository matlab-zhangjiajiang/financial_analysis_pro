# coding=utf-8
#深圳创业板股票的代码是：300XXX 的股票
#而深圳中小板股票的代码是：002XXX 开头的股票
#上海主板的股票代码是：60XXXX 开头的股票
#深圳主板的股票代码是：000XXX 开头的股票

class stock_area_tools(object):

     def get_stock_area_code(self,stockcode):
         if stockcode.startswith('300'):
             return 'SZ'
         elif stockcode.startswith('002'):
             return 'SZ'
         elif stockcode.startswith('60'):
             return 'SH'
         elif stockcode.startswith('000'):
             return 'SZ'
         return 'SH'


if __name__ == '__main__':
    print(stock_area_tools().get_stock_area_code('002401'))
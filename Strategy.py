import pywencai
from MyUtil import MyUtil
from TRADE_DAY import TRADE_DAY
from datetime import datetime

class Strategy(object):

    def __init__(self):
        self.trade = TRADE_DAY()
    
    # 创业板1进2
    def 创业板1进2(self):
        trade = self.trade
        cur = MyUtil.now().strftime('%Y-%m-%d')
        yes = trade.get_last_trading_day(cur)
        cmd = '创业板，'+yes+'首板涨停，'+cur+'集合竞价成交量除以自由流通股大于0.019，'+cur+'竞价涨跌幅，'+yes+'流通市值，非st'
        print('[创业板1进2]: ' + cmd)
        res = pywencai.get(query=cmd, sort_order='asc', loop=True, sleep=0.1)
        if res is None:
            return
        # print(res.columns)
        cur_str = datetime.strptime(cur, "%Y-%m-%d").strftime('%Y%m%d') 
        yes_str = datetime.strptime(yes, "%Y-%m-%d").strftime('%Y%m%d') 
        data = res.loc[:, ['股票代码', '股票简称','竞价涨幅['+cur_str+']', '{(}竞价量['+cur_str+']{/}自由流通股['+cur_str+']{)}','自由流通市值['+yes_str+']']]
        data.columns = ["股票代码", "股票简称",'竞价涨幅','实际换手','流通市值']  # 重新命名

        # 格式化输出
        text = ''
        for index, row in data.iterrows():

            text += '---------------------\n'
            text += '股票名称: '+ row[1] + ' ('+row[0]+')\n'
            text += '实际换手: '+ str('%.2f'%(row[3]*100)) + '% '+ ('[抢筹]' if row[3]>=0.02 else '') +'\n'
            text += '竞价涨幅: ' + str(row[2]) + '%\n'
            text += '流通市值: ' + str('%.2f'%(row[4]/(100000000))) + '亿\n'
        return text

    # 主板1进2
    def 主板1进2(self):
        trade = self.trade
        cur = MyUtil.now().strftime('%Y-%m-%d')
        yes = trade.get_last_trading_day(cur)
        cmd = yes + '首板涨停，'+ cur +'集合竞价成交量除以自由流通股大于0.01，竞价涨跌幅大于0，'+yes+'自由流通市值，非st非创业板非科创板'
        res = pywencai.get(query=cmd, sort_order='asc', loop=True, sleep=0.1)
        if res is None:
            return
        print(res.columns)
        cur_str = datetime.strptime(cur, "%Y-%m-%d").strftime('%Y%m%d') 
        yes_str = datetime.strptime(yes, "%Y-%m-%d").strftime('%Y%m%d') 
        data = res.loc[:, ['股票代码', '股票简称','分时涨跌幅:前复权['+cur_str+' 09:25]', '{(}竞价量['+cur_str+']{/}自由流通股['+cur_str+']{)}','自由流通市值['+yes_str+']']]
        data.columns = ["股票代码", "股票简称",'竞价涨幅','实际换手','流通市值']  # 重新命名

        # 格式化输出
        text = ''
        for index, row in data.iterrows():

            text += '---------------------\n'
            text += '股票名称: '+ row[1] + ' ('+row[0]+')\n'
            text += '实际换手: '+ str('%.2f'%(row[3]*100)) + '% '+ ('[抢筹]' if row[3]>=0.02 else '') +'\n'
            text += '竞价涨幅: ' + str(row[2]) + '%\n'
            text += '流通市值: ' + str('%.2f'%(row[4]/(100000000))) + '亿\n'
        return text  
    
if __name__ == "__main__":
    # i = 0.0026189940306016197
    # print(str('%.2f'%(i*100)))
    # f = 1454444444.9
    # print(str('%.2f'%(f/(100000000))) + '亿')

    stg = Strategy()
    # res = stg.创业板1进2()
    ret = stg.主板1进2()
    print(ret)
    pass
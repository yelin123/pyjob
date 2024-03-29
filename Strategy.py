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
        # cur = '2023-10-27'
        yes = trade.get_last_trading_day(cur)
        cmd = '创业板，'+yes+'首板涨停，'+cur+'集合竞价成交量除以自由流通股大于0.019，'+cur+'竞价涨跌幅，非st'
        print('[创业板1进2]: ' + cmd)
        res = pywencai.get(query=cmd, sort_order='asc', loop=True, sleep=0.1)
        if res is None:
            print('[创业板1进2]数据源为空')
            return
        # print(res.columns)
        cur_str = datetime.strptime(cur, "%Y-%m-%d").strftime('%Y%m%d') 
        yes_str = datetime.strptime(yes, "%Y-%m-%d").strftime('%Y%m%d') 
        data = res.loc[:, ['股票代码', '股票简称','分时涨跌幅:前复权['+cur_str+' 09:25]', '{(}竞价量['+cur_str+']{/}自由流通股['+cur_str+']{)}']]
        data['流通市值'] = res['最新价'].astype(float) * res[('自由流通股['+cur_str+']')]
        data.columns = ["股票代码", "股票简称",'竞价涨幅','实际换手','流通市值']  # 重新命名

            #data['涨跌幅'].apply(lambda x: '成功' if float(x) >= 19.95 else '失败') # 处理结果新增一列
        # 格式化输出
        text = ''
        for index, row in data.iterrows():

            text += '---------------------\n'
            text += '股票名称: '+ row[1] + ' ('+row[0]+')\n'
            text += '实际换手: '+ str('%.2f'%(row[3]*100)) + '% '+ ('[抢筹]' if row[3]>=0.02 else '') +'\n'
            text += '竞价涨幅: ' + str('%.2f'%float(row[2])) + '%\n'
            text += '流通市值: ' + str('%.2f'%(row[4]/(100000000))) + '亿\n'
        return text

    # 主板1进2
    def 主板1进2(self):
        trade = self.trade
        cur = MyUtil.now().strftime('%Y-%m-%d')
        # cur = '2024-01-10'
        yes = trade.get_last_trading_day(cur)
        cmd = yes + '首板涨停，'+ cur +'集合竞价成交量除以自由流通股大于0.01，'+cur+'竞价涨跌幅大于等于0，'+yes+'自由流通市值，非st非创业板非科创板'
        print(cmd)
        res = pywencai.get(query=cmd, sort_order='asc', loop=True, sleep=0.1)
        if res is None:
            print('[主板1进2]数据源为空')
            return
        # 
        print(res.columns)
        cur_str = datetime.strptime(cur, "%Y-%m-%d").strftime('%Y%m%d') 
        yes_str = datetime.strptime(yes, "%Y-%m-%d").strftime('%Y%m%d') 
        竞价涨幅 = '分时涨跌幅:前复权['+cur_str+' 09:25]' if '分时涨跌幅:前复权['+cur_str+' 09:25]' in res.columns else '竞价涨幅['+cur_str+']'
        data = res.loc[:, ['股票代码', '股票简称',竞价涨幅, '{(}竞价量['+cur_str+']{/}自由流通股['+cur_str+']{)}','自由流通市值['+yes_str+']']]
        data.columns = ["股票代码", "股票简称",'竞价涨幅','实际换手','流通市值']  # 重新命名

        # 格式化输出
        text = ''
        for index, row in data.iterrows():

            text += '---------------------\n'
            text += '股票名称: '+ row[1] + ' ('+row[0]+')\n'
            text += '实际换手: '+ str('%.2f'%(row[3]*100)) + '% '+ ('[抢筹]' if row[3]>=0.02 else '') +'\n'
            text += '竞价涨幅: ' + str('%.2f'%float(row[2])) + '%\n'
            text += '流通市值: ' + str('%.2f'%(row[4]/(100000000))) + '亿\n'
        return text  
    
    # 连板高标
    def 连板高标(self):
        trade = self.trade
        cur = MyUtil.now().strftime('%Y-%m-%d')
        yes = trade.get_last_trading_day(cur)
        cmd = yes + '连续涨停天数大于1，'+ cur +'集合竞价成交量除以自由流通股大于0，竞价分时涨跌幅大于-11，'+yes+'自由流通市值，连续涨停天数排序，非st非创业板非科创板'
        print(cmd)
        res = pywencai.get(query=cmd, sort_order='asc', loop=True, sleep=0.1)
        if res is None:
            print('[连板高标]数据源为空')
            return
        print(res.columns)
        cur_str = datetime.strptime(cur, "%Y-%m-%d").strftime('%Y%m%d') 
        yes_str = datetime.strptime(yes, "%Y-%m-%d").strftime('%Y%m%d') 
        data = res.loc[:, ['股票代码', '股票简称','分时涨跌幅:前复权['+cur_str+' 09:25]', '{(}竞价量['+cur_str+']{/}自由流通股['+cur_str+']{)}','自由流通市值['+yes_str+']', '连续涨停天数['+ yes_str +']']]
        data.columns = ["股票代码", "股票简称",'竞价涨幅','实际换手','流通市值','连板数']  # 重新命名

        # 格式化输出
        text = ''
        for index, row in data.iterrows():
            text += '---------------------\n'
            text += '股票名称: '+ row[1] + ' ('+row[0]+')\n'
            text += '连板晋级: '+ str(row[5]) +'进'+ str(row[5]+1) +'\n'
            text += '实际换手: '+ str('%.2f'%(row[3]*100)) + '% '+ ('[量不够]' if row[3]<=0.03 else '') +'\n'
            text += '竞价涨幅: ' + str('%.2f'%float(row[2])) + '%\n'
            text += '流通市值: ' + str('%.2f'%(row[4]/(100000000))) + '亿\n'
        return text  

     # 连板高标
  
    # 创业板振幅选股
    def 创业板振幅选股(self):
        trade = self.trade
        cur = MyUtil.now().strftime('%Y-%m-%d')
        if not(MyUtil.isTradeDay(MyUtil.now())):
            cur = trade.get_last_trading_day(cur)
        yes = trade.get_last_trading_day(cur)
        bfyes = trade.get_last_trading_day(yes)
        #  创业板，2023-11-22至2023-11-24振幅达到29%，2023-11-22至2023-11-24的曾涨停次数大于0或者涨停次数大于0，2023-11-24收红盘，按照2023-11-22至2023-11-24振幅排序
        # 创业板，11月20至11月22日振幅达到29%，11月20至11月22日的曾涨停次数大于0或者涨停次数大于0，11月22日收红盘，按照11月20至11月22日振幅排序
        cmd = '创业板，'+bfyes+'至'+cur+'振幅达到29%，'+bfyes+'至'+cur+'的曾涨停次数大于0或者涨停次数大于0，'+cur+'收红盘，按照'+bfyes+'至'+cur+'振幅排序'
        print(cmd)
        res = pywencai.get(query=cmd, sort_order='asc', loop=True, sleep=0.1)
        if res is None:
            print('[创业板振幅选股]数据源为空')
            return
        # print(res.columns)
        cur_str = datetime.strptime(cur, "%Y-%m-%d").strftime('%Y%m%d') 
        yes_str = datetime.strptime(yes, "%Y-%m-%d").strftime('%Y%m%d') 
        data = res.loc[:, ['股票代码', '股票简称']]
        data.columns = ["股票代码", "股票简称"]  # 重新命名

        # 格式化输出
        text = cmd + '\n---------------------\n'
        for index, row in data.iterrows():
            text += row[1] + ' ('+row[0]+')\n'
        return text  

if __name__ == "__main__":
    stg = Strategy()
    print('运行')
    #res = stg.创业板1进2()
    #res = stg.创业板振幅选股()
    res = stg.主板1进2()
    print(res) 
    # cmd = '创业板，2023-10-26首板涨停，2023-10-27集合竞价成交量除以自由流通股大于0.019，2023-10-27竞价涨跌幅，非st'
    # i = 0.0026189940306016197
    # print(str('%.2f'%(i*100)))
    # f = 1454444444.9
    # print(str('%.2f'%(f/(100000000))) + '亿')
    pass
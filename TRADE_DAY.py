import chinese_calendar
import datetime
import pandas as pd
from MyUtil import MyUtil
        
class TRADE_DAY(object):
    def __init__(self):
        '''
        st: str,开始日期,格式如'2023-03-01'
        et: str,终止日期,格式如'2023-03-01'
        data:转换后的交易日数据源
        '''
        # print('4')
        # print(self.get_tradeday('2010-01-01', MyUtil.now().strftime("%Y-%m-%d")))
        #trade_date = ak.tool_trade_date_hist_sina()
        # 对初始的数据进行清洗转换,此处可依据获取的数据源进行自主转换
        # 转换后的数据格式为DataFrame,只有一列,列名为date,值的格式为str,例如'2023-03-03'
        #new_df = pd.DataFrame({'date': trade_date['trade_date']})
        #new_df['date'] = new_df['date'].apply(lambda x: pd.to_datetime(str(x)).strftime("%Y-%m-%d"))
        #print(new_df)
        new_df = pd.DataFrame(self.get_tradeday('2010-01-01', MyUtil.now().strftime("%Y-%m-%d")), columns=['date'])
        self.data = new_df

    @staticmethod
    def add_date(date, st, et):
        # date:TRADE_DAY对应获取的交易日数据
        # 对所获频率的日期加上开始和结束日
        new_date = pd.DataFrame({'date': [st, et]})
        new_date = new_date.append(date)
        new_date = new_date.drop_duplicates()
        add_date = new_date.sort_values(by=['date'], ascending=True)
        return add_date
 
    @staticmethod
    def get_time_diff(one_day, other_day):
        # 获取两个交易日之间相差的自然日天数
        min_day = pd.to_datetime(min([one_day, other_day]))
        max_day = pd.to_datetime(max([one_day, other_day]))
        return (max_day - min_day).days
    
    # 调用交易日列表，设置起始日期和终止日期
    @staticmethod
    def get_tradeday(start_str,end_str):
        start = datetime.datetime.strptime(start_str, '%Y-%m-%d') # 将字符串转换为datetime格式
        end = datetime.datetime.strptime(end_str, '%Y-%m-%d')
        # 获取指定范围内工作日列表
        lst = chinese_calendar.get_workdays(start,end)
        expt = []
        # 找出列表中的周六，周日，并添加到空列表
        for time in lst:
            if time.isoweekday() == 6 or time.isoweekday() == 7:
                expt.append(time)
        # 将周六周日排除出交易日列表
        for time in expt:
            lst.remove(time)
        date_list = [item.strftime('%Y-%m-%d') for item in lst] #列表生成式，strftime为转换日期格式
        return date_list
    
    def get_last_trading_day(self, day):
        # 获取上一个交易日
        data = self.data
        last_day = data.loc[data['date'] < day]
        return last_day['date'].max()
 
    def get_next_trading_day(self, day):
        # 获取下一个交易日
        data = self.data
        last_day = data.loc[data['date'] > day]
        return last_day['date'].min()
 
    def get_week_day(self):
        # 获取区间对应的周度交易日日期
        data = self.data
        data['last'] = data['date'].shift(1)
        data['next'] = data['date'].shift(-1)
        new_data = data.loc[(data['date'] >= self.st) & (data['date'] <= self.et)]
        # 求时间差
        last_diff = []
        next_diff = []
        for num in range(len(new_data)):
            now = new_data['date'].values[num]
            last = new_data['last'].values[num]
            next = new_data['next'].values[num]
            last_diff.append(TRADE_DAY.get_time_diff(now, last))
            next_diff.append(TRADE_DAY.get_time_diff(now, next))
        new_data['next_diff'] = next_diff
        new_data['last_diff'] = last_diff
        me_df = new_data.loc[new_data['next_diff']>2]
        me_df = me_df.sort_values(by=['date'], ascending=True)
        out_df = pd.DataFrame({'date': me_df['date']})
        return out_df
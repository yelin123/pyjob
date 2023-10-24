from chinese_calendar import is_workday
from datetime import datetime
from dateutil import tz


class MyUtil:
    # 判断是否是交易日，传入date类型
    @staticmethod
    def isTradeDay(date):
        if is_workday(date):
            if datetime.isoweekday(date) < 6:
                return True
        return False
    
    # 获取当前时间，上海时区
    @staticmethod
    def now():
        time_zone = tz.gettz('Asia/Shanghai')
        now = datetime.now(tz=time_zone)
        return now;

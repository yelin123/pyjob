# 从同花顺问财中获取数据源的方法
# api文档地址：https://github.com/zsrl/pywencai
import pywencai

# sleep 单位是秒
res = pywencai.get(query='退市股票', sort_key='退市@退市日期', sort_order='asc', loop=True, sleep=1)
print(res)
print(res.info())
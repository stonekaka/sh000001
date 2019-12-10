#!/usr/bin/env python
# -*- coding: cp936 -*-


#获取5日，10日，20日均线数据

import tushare as ts
import talib
from matplotlib import pyplot as plt

#通过tushare获取股票信息
df=ts.get_k_data('601888',start='2018-01-30',end='2018-10-30') #以股票代码[601888]中国国旅为例，提取从2018-01-12到2018-10-30的收盘价
    #提取收盘价
closed=df['close'].values
    #获取均线的数据，通过timeperiod参数来分别获取 5,10,20 日均线的数据。
ma5=talib.SMA(closed,timeperiod=5)
ma10=talib.SMA(closed,timeperiod=10)
ma20=talib.SMA(closed,timeperiod=20)

    #打印出来每一个数据
print (closed)
print (ma5)
print (ma10)
print (ma20)

    #通过plog函数可以很方便的绘制出每一条均线
plt.plot(closed)
plt.plot(ma5)
plt.plot(ma10)
plt.plot(ma20)
    #添加网格，可有可无，只是让图像好看点
plt.grid()
    #记得加这一句，不然不会显示图像
plt.show()

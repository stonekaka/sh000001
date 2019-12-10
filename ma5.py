#!/usr/bin/env python
# -*- coding: cp936 -*-


#��ȡ5�գ�10�գ�20�վ�������

import tushare as ts
import talib
from matplotlib import pyplot as plt

#ͨ��tushare��ȡ��Ʊ��Ϣ
df=ts.get_k_data('601888',start='2018-01-30',end='2018-10-30') #�Թ�Ʊ����[601888]�й�����Ϊ������ȡ��2018-01-12��2018-10-30�����̼�
    #��ȡ���̼�
closed=df['close'].values
    #��ȡ���ߵ����ݣ�ͨ��timeperiod�������ֱ��ȡ 5,10,20 �վ��ߵ����ݡ�
ma5=talib.SMA(closed,timeperiod=5)
ma10=talib.SMA(closed,timeperiod=10)
ma20=talib.SMA(closed,timeperiod=20)

    #��ӡ����ÿһ������
print (closed)
print (ma5)
print (ma10)
print (ma20)

    #ͨ��plog�������Ժܷ���Ļ��Ƴ�ÿһ������
plt.plot(closed)
plt.plot(ma5)
plt.plot(ma10)
plt.plot(ma20)
    #������񣬿��п��ޣ�ֻ����ͼ��ÿ���
plt.grid()
    #�ǵü���һ�䣬��Ȼ������ʾͼ��
plt.show()

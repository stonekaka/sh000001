#!/usr/bin/env python
# -*- coding: cp936 -*-


from __future__ import division
import urllib
import time
import json
import sys
import os
import time
from decimal import *

path = sys.path[0]


def get_zhishu(code):
	params = urllib.urlencode({'from':'pc','os_ver':'1','cuid':'xxx','vv':'100', \
			'format':'json','stock_code':code,'timestamp':int(time.time())})

	try:
		f = urllib.urlopen("https://gupiao.baidu.com/api/rails/stockbasicbatch?%s" % params)

		plain = f.read()

		f.close()
	except ValueError, e:
		return 0
	if not plain:
		return 0

	#print(plain)
	try:
		decode = json.loads(plain)
	except ValueError, e:
		return 0

	if not decode:
		return 0

#	print decode.keys()
#	print "errno:",decode["errorNo"]
#	print "sh01:",decode["data"][0]["close"]
	errno = decode["errorNo"]

	if errno != 0:
		return 0

	if decode["data"] and decode["data"][0] and decode["data"][0]["close"]:
		return (decode["data"][0]["close"])


def get_zhishu_fromqq(code):
        f = urllib.urlopen("http://qt.gtimg.cn/?q=s_%s" % code)

        plain = f.read()
        f.close()
        if not plain:
                return 0

        return plain[27:39]

def get_ma5_ma10_ma20_fromqq(name, code):

        #weekly: http://web.ifzq.gtimg.cn/other/klineweb/klineWeb/weekTrends?code=sz002405&type=qfq&_var=trend_qfq
        #k-gif: http://image.sinajs.cn/newchart/daily/n/sz002463.gif
        
        f = urllib.urlopen("http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=%s,day,,,30,qfq" % code)

        plain = f.read()
        f.close()
        if not plain:
                return 0

        try: 
                decode = json.loads(plain[13:])
        except ValueError, e:
                return 0

        if decode["data"][code].has_key("qfqday"):
                full_arr = decode["data"][code]["qfqday"]
        else:
                full_arr = decode["data"][code]["day"]
        #print(full_arr)
        length = len(full_arr)
        #print("aaaaaaaaaaaaa, len=%d" % length)
        sum=0.00
        for num in range(25,30):
                #print(num)
                #print(full_arr[num][2])
                #print(float(full_arr[num][2]))
                sum += float(full_arr[num][2])
                #print("sum=%f" % round(sum,2))

        avg_5 = round(sum/5, 2)
        sum=0.00
        for num in range(20,30):
                sum += float(full_arr[num][2])

        avg_10 = round(sum/10, 2)
        sum=0.00
        for num in range(10,30):
                sum += float(full_arr[num][2])

        avg_20 = round(sum/20, 2)
        sum=0.00
        for num in range(0,30):
                sum += float(full_arr[num][2])

        avg_30 = round(sum/30, 2)

        length = length - 1
        print("[%.2f], [%.2f], [%.2f], [%.2f]" % (avg_5, avg_10, avg_20, avg_30))
        rift_5_int=(float(full_arr[length][2])-avg_5)/float(full_arr[length][2])
        rift_5="{:.2f}%".format(rift_5_int*100)
        #print("rift_5= {:.2f}%".format(rift*100))
        rift_10_int=(float(full_arr[length][2])-avg_10)/float(full_arr[length][2])
        rift_10="{:.2f}%".format(rift_10_int*100)
        #print("rift_10= {:.2f}%".format(rift*100))
        rift_20_int=(float(full_arr[length][2])-avg_20)/float(full_arr[length][2])
        rift_20="{:.2f}%".format(rift_20_int*100)
        rift_30_int=(float(full_arr[length][2])-avg_30)/float(full_arr[length][2])
        rift_30="{:.2f}%".format(rift_30_int*100)
        #print("rift_30= {:.2f}%".format(rift*100))
        current = float(full_arr[length][2])


        ##################
        judge=""
        
        if rift_5_int + 0.02 < 0:
                judge += "___"
        if rift_10_int + 0.02 < 0:
                judge += "---"
        if rift_20_int + 0.02 < 0:
                judge += "~~~"
        if rift_30_int + 0.02 < 0:
                judge += "in"

        if rift_5_int > rift_10_int and rift_10_int > rift_20_int:
                judge = "out"

        ##################
        time.sleep(1)
        return name,current, rift_5,rift_10,rift_20,rift_30, judge

#print(get_ma5_ma10_ma20_fromqq('sz002405'))
#time.sleep(1)
#print(get_zhishu('sh000001'))
#time.sleep(1)
print(get_zhishu_fromqq('sh000001'))
time.sleep(1)
print(get_ma5_ma10_ma20_fromqq('sh','sh000001'))
print(get_ma5_ma10_ma20_fromqq('byd','sz002594'))
print(get_ma5_ma10_ma20_fromqq('siwei','sz002405'))
print(get_ma5_ma10_ma20_fromqq('hudian','sz002463'))
print(get_ma5_ma10_ma20_fromqq('changcheng','sz000066'))
print(get_ma5_ma10_ma20_fromqq('zhongruan','sz600536'))
print(get_ma5_ma10_ma20_fromqq('zhongxing','sz000063'))
print(get_ma5_ma10_ma20_fromqq('yiyuan','sh603236'))
print(get_ma5_ma10_ma20_fromqq('changfei','sh601869'))

os.system('pause')

#!/usr/bin/env python
#coding=utf8

from __future__ import division
import urllib
import time
import json
import sys
import os

path = sys.path[0]
RESULT_FILE = path + "/" + "result.txt"

def get_holiday():
	str_time = time.strftime("%Y%m%d", time.localtime())
	g_time = str_time
	params = urllib.urlencode({'d':str_time})

	f = urllib.urlopen("http://www.easybots.cn/api/holiday.php?%s" % params)

	plain = f.read()

	f.close()
	if not plain:
		return 0

#	print plain
	decode = json.loads(plain)
	if not decode:
		return 0
	
	return decode[str_time].encode("utf-8")

def get_zhishu():
	params = urllib.urlencode({'from':'pc','os_ver':'1','cuid':'xxx','vv':'100', \
			'format':'json','stock_code':'sh000001','timestamp':int(time.time())})

	f = urllib.urlopen("https://gupiao.baidu.com/api/rails/stockbasicbatch?%s" % params)

	plain = f.read()

	f.close()
	if not plain:
		return 0

	print plain
	decode = json.loads(plain)

	if not decode:
		return 0

#	print decode.keys()
#	print "errno:",decode["errorNo"]
#	print "sh01:",decode["data"][0]["close"]
	errno = decode["errorNo"]

	if errno != 0:
		return 0

	if decode["data"] and decode["data"][0] and decode["data"][0]["close"]:
		return int(decode["data"][0]["close"])

def record():
	month = []
	zhishu = get_zhishu()

	fp = open(RESULT_FILE, 'r')
	month = json.loads(fp.read())
	#print string
	fp.close()
	month.append(zhishu)

	#for i in range(len(month)):
	#	print month[i]

	if zhishu:
		fp = open(RESULT_FILE,'w')
		print>>fp,json.dumps(month)
		fp.close()

def sendmail(title, content):
	msg="sleep 3;echo \""+content+"\" |mutt -s \""+title+"\" stoneforfun@aliyun.com"
	ret = os.system(msg)
	print "my send mail ret %d"%ret

def build_mail(val):
	str_time = time.strftime("%Y%m%d", time.localtime())
	title = "T%d_A%d_%0.2f_%0.2f_%s" % (val['last'], val['avg'], val['dirta'], val['percent'], str_time)
	content = title
	sendmail(title, content)

def calc_avg(day):
	fp = open(RESULT_FILE,'r')	
	month = json.loads(fp.read())
	fp.close()
	res = []
	val = {'avgt':0, 'avg':0, 'last':0, 'dirta':0, 'percent':0}

	total_len = len(month);
	total_len = total_len - 1

	if total_len < day:
		return 0

	for i in range(total_len):
		if i >= total_len-day:
			res.append(month[i])

	total = 0
	last = 0
	for i in range(len(res)):
		total = total + res[i]
		last = res[i]

	val['avgt'] = day
	val['last'] = last
	val['avg'] = total/day

	if last >= val['avg']:
		return 0

	val['dirta'] = val['avg'] - last
	val['percent'] = round(val['dirta']*100/val['avg'], 2)
	print "dirta:",val['dirta']," percent: ",val['percent']

	return val


holidy = get_holiday()

print "holidy:",holidy,"=="
if holidy != "0":
	sys.exit()

#get zhishu and write to local file
record()

#define days and threshold percent
val_short = {'maxday':8, 'threshold':2.3}

#cacl avg, return avg and percent
ret=calc_avg(val_short['maxday'])
this_time = time.strftime("%Y/%m/%d", time.localtime())
print "[",this_time,"] 8 days avg:",json.dumps(ret)

if type(ret) != dict:
	sys.exit()

if ret['percent'] >= val_short['threshold']:
	#print 'sendmail'
	build_mail(ret)



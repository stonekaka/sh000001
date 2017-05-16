#!/usr/bin/env python
#coding=utf8

from __future__ import division
import urllib
import time
import json
import sys
import os

path = sys.path[0]
RESULT_FILE = path + "/" + "xau.txt"

def get_xau():
	rand=time.time()/10000000000
	#params = urllib.urlencode({'list':'hf_XAU','_':rand})
	#print params
	f = urllib.urlopen("http://hq.sinajs.cn/?_=%f&list=hf_XAU" % rand)

	plain = f.read()

	f.close()
	if not plain:
		return 0

	#print plain
	decode = plain[19:23]

	if not decode:
		return 0

	#print decode
	return int(decode)

def record():
	month = []
	price = get_xau()

	fp = open(RESULT_FILE, 'r')
	month = json.loads(fp.read())
	#print string
	fp.close()
	month.append(price)

	#for i in range(len(month)):
	#	print month[i]

	if price:
		fp = open(RESULT_FILE,'w')
		print>>fp,json.dumps(month)
		fp.close()

def calc_avg(day):
	fp = open(RESULT_FILE,'r')	
	month = json.loads(fp.read())
	fp.close()
	res = []
	val = {'avgt':0, 'avg':0, 'last':0, 'dirta':0, 'percent':0}

	total_len = len(month);
	#total_len = total_len - 1

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
	print 'avg',val['avg']

	if last >= val['avg']:
		return val

	val['dirta'] = val['avg'] - last
	val['percent'] = round(val['dirta']*100/val['avg'], 2)
	print "dirta:",val['dirta']," percent: ",val['percent']

	return val

def sendmail(title, content):
	msg="sleep 3;echo \""+content+"\" |mutt -s \""+title+"\" stoneforfun@aliyun.com"
	ret = os.system(msg)
	print "my send mail ret %d"%ret

def build_mail(val):
	str_time = time.strftime("%Y%m%d", time.localtime())
	title = "T%d_A%d_%0.2f_%0.2f_%s" % (val['last'], val['avg'], val['dirta'], val['percent'], str_time)
	content = "Welcome to the 3rd Edition of Learn Python the Hard Way. You can visit the companion site to the."
	sendmail(title, content)

record()

#define days and threshold percent
val_short = {'maxday':5, 'threshold':50}

#cacl avg, return avg and percent
ret=calc_avg(val_short['maxday'])
print "5 weeks avg:",json.dumps(ret)

if type(ret) != dict:
	sys.exit()

#define days and threshold percent
val_short2 = {'maxday':10, 'threshold':50}

#cacl avg, return avg and percent
ret2=calc_avg(val_short2['maxday'])
print "10 weeks avg:",json.dumps(ret2)

if type(ret2) != dict:
	sys.exit()

mydirta = ret2['dirta'] - ret['dirta']
print "mydirta =", mydirta
if mydirta >= 18:
	print 'sendmail (xau)'
	build_mail(ret)


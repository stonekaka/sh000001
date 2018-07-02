#!/usr/bin/env python


from __future__ import division
import urllib.request
import urllib.parse
import time
import json
import sys
import os

path = sys.path[0]


def get_zhishu():
	params = urllib.parse.urlencode({'from':'pc','os_ver':'1','cuid':'xxx','vv':'100', \
			'format':'json','stock_code':'sh000001','timestamp':int(time.time())})

	f = urllib.request.urlopen("https://gupiao.baidu.com/api/rails/stockbasicbatch?%s" % params)

	plain = f.read()

	f.close()
	if not plain:
		return 0

	#print(plain)
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


print(get_zhishu())
os.system('pause')

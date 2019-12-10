#!/usr/bin/env python

from decimal import *

text = [u'1.2', u'1.3']
print text[0]
print text[1]
c = Decimal(text[0]) + Decimal(text[1])
print c


arr = [0,1,2,3,4,5]

for i in range(1,2):
    print arr[i]

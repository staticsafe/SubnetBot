#! /usr/bin/env python
import json
import string
import time

obj = None
with open("stockdata.json", 'rb') as f:
    obj = str(json.load(f, 'iso-8859-1')).split('u')
    obj.pop(0)
    for s in obj:
        temp = s
        temp = temp.lstrip("'")
        if temp.endswith("', "):
            temp = temp.rstrip("', ")
        elif temp.endswith("': "):
            temp = temp.rstrip("': ")
        elif temp.endswith("'}"):
            temp = temp.rstrip("'}")
        obj[obj.index(s)] = temp

Change = None
ChangePercent = None
Exchange = None
StockName = None
DateTime = None
CurrentPrice = None

for s in obj:
    if s == 'c':
        Change = obj[obj.index(s)+1]
        print "Change Found:" + Change
    elif s == 'cp':
        ChangePercent = obj[obj.index(s)+1]
        print "Change Percent found: " + ChangePercent
    elif s == 'e':
        Exchange = obj[obj.index(s)+1]
        print "Exchange found: " + Exchange
    elif s == 'lt':
        DateTime = obj[obj.index(s)+1]
        print "DateTime found: " + DateTime
    elif s == 't':
        StockName = obj[obj.index(s)+1]
        print "StockName found: " + StockName
    elif s == 'r':
        CurrentPrice = obj[obj.index(s)+1]
        print "CurrentPrice found: " + CurrentPrice
temp = Exchange + ':' + StockName + ' @ ' + CurrentPrice + ' ' + Change + "(" + ChangePercent + "%) via Google Finance. Current as of " + DateTime
print temp

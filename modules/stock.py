import urllib2
import json
import time

class GoogleFinanceAPI:
    def __init__(self):
        self.prefix = "http://finance.google.com/finance/info?client=ig&q="
    
    def get(self,symbol,exchange):
        url = self.prefix+"%s:%s"%(exchange,symbol)
        u = urllib2.urlopen(url)
        content = u.read()
        with open("stockdata.json", 'wb') as f:
            f.write(content[3:])
            f.close()
            
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

        NASDAQ = None
        #NYSE = None
        #TSE = None

        with open('NASDAQ.json', 'rb') as f:
            NASDAQ = json.load(f, encoding='utf-8')

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
            elif s == 'l':
                CurrentPrice = obj[obj.index(s)+1]
                print "CurrentPrice found: " + CurrentPrice
        if (Exchange == 'NASDAQ'):
            temp = NASDAQ[StockName]
       #elif (Exchange == 'NYSE'):
            #temp = NYSE[StockName]
        else:
            temp = ''
            print 'Unsupported exchange found, should get data for that'
        temp += '(' + Exchange + ':' + StockName + ')@' + CurrentPrice + ' ' + Change + "(" + ChangePercent + "%) via Google Finance. Current as of " + DateTime
        print temp
        return temp

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

    def parse():
        obj = None
        with open("stockdata.json", 'rb') as f:
            obj = str(json.load(f)).split('u')
            f.close()

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
            temp = None

        NASDAQ = None
        NYSE = None
        TSE = None

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

        returnval = ''
        if (Exchange == 'NASDAQ'):
             print StockName
             try:
                 with open('./NASDAQ.txt', 'rb') as f:
                     for line in f:
                         print line
                         temp = line.split()
                         if temp[0] == StockName:
                             for s in temp:
                                 if s == temp[0]:
                                     continue
                                 else:
                                     returnval += s
             except IOError, err_msg:
                print err_msg
        elif (Exchange == 'NYSE'):
            print StockName
            with open('NYSE.txt', 'rb') as f:
                 for line in f:
                     temp = line.split()
                     if temp[0] == StockName:
                         for s in temp:
                             if s == temp[0]:
                                 continue
                             else:
                                 returnval += s
        else:
            returnval = ''
            print 'Unsupported exchange found, should get data for that'
                    
        if Change.startswith('-'):
            Change_ = '4' + '-' + '1' + Change.lstrip('-') + '(' + ChangePercent + '%)'
        else:
            Change_ = '9' + '+' + '1' + Change.lstrip('+') + '(' + ChangePercent + '%)'
                    
        returnval += '(' + Exchange + ':' + StockName + ')@' + CurrentPrice + ' ' + Change_ + " via Google Finance. Current as of " + DateTime
        print returnval
        return returnval

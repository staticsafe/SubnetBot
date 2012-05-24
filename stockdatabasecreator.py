import json

NASDAQ = dict()
NYSE = dict()
TSE = dict()
CVE = dict()

with open('NASDAQ.txt', 'rb') as f:
    for line in f:
        temp = line.split()
        string = ''
        for s in temp:
            if (s == temp[0]):
                continue
            else:
                string += ' ' + s
        NASDAQ[temp[0]] = string

with open('NYSE.txt', 'rb') as f:
    for line in f:
        temp = line.split()
        string = ''
        for s in temp:
            if (s == temp[0]):
                continue
            else:
                string += ' ' + s
        NYSE[temp[0]] = string

with open('TSE.txt', 'rb') as f:
    for line in f:
        temp = line.split()
        string = ''
        for s in temp:
            if (s == temp[0]):
                continue
            else:
                string += ' ' + s
        TSE[temp[0].rstrip('.TO')] = string

with open('CVE.txt', 'rb') as f:
    for line in f:
        temp = line.split()
        string = ''
        for s in temp:
            if (s == temp[0]):
                continue
            else:
                string += ' ' + s
        CVE[temp[0].rstrip('.V')] = string

with open('NASDAQ.json', 'wb') as f:
    json.dump(NASDAQ, f, encoding='utf-8')
with open('NYSE.json', 'wb') as f:
    json.dump(NYSE, f, encoding='utf-8')
with open('TSE.json', 'wb') as f:
    json.dump(TSE, f, encoding='utf-8')
with open('CVE.json', 'wb') as f:
    json.dump(CVE, f, encoding='utf-8')

NASDAQ = None

with open('NASDAQ.json', 'rb') as f:
    NASDAQ = json.load(f, encoding='utf-8')
    print NASDAQ['AAPL']

import json

NASDAQ = dict()
NYSE = dict()
TSE = dict()

response = 'y'
while response != 'n':
    stocksymbol = raw_input('Enter the stock symbol:')
    stockexchange = raw_input('enter the exchange this symbol trades on:')
    companyname = raw_input('enter the full name of the company:')

    if (stockexchange == 'NASDAQ'):
        NASDAQ[stocksymbol] = companyname
    elif (stockexchange == 'NYSE'):
        NYSE[stocksymbol] = companyname
    elif (stockexchange == 'TSE'):
        TSE[stocksymbol] = companyname
    else:
        print 'that exchange is not supported'

    response = raw_input('Do you wish to continue?')

with open('NASDAQ.json', 'wb') as f:
    json.dump(NASDAQ, f)
with open('NYSE.json', 'wb') as f:
    json.dump(NYSE, f)
with open('TSE.json', 'wb') as f:
    json.dump(TSE, f)

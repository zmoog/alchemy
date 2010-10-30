#! /bin/env python

import httplib2
import json
from datetime import datetime
from cash.models import Account, Transfer

BASE='http://alchemy.couchone.com/cash-test/'

def request(uri, body=None, method="GET"):
    headers, body =  client.request("%s/%s" % (BASE, uri) , method=method, headers={'Content-Type': 'application/json'}, body=json.dumps(body))
    if headers.status != 201:
        raise Exception("status: %s - but 201 was expected.")


if __name__ == '__main__':

    client = httplib2.Http()
    client.add_credentials('hippo', '*')

    accounts = dict()
 
    for account in Account.objects.all():
        doc = dict(name=account.name, category=account.type, type='account', active=True, created_at=datetime.now().isoformat())

        h, b = post(doc) 
   
        accounts[account.id] = h['location'].split('/')[-1:][0]

    for transfer in Transfer.objects.all():
        doc = dict(amount=transfer.amount, description=transfer.description,source=accounts[transfer.source.id],destination=accounts[transfer.destination.id],opertation_date=transfer.validity_date.isoformat(),validity_date=transfer.validity_date.isoformat(),type='transaction')

        h, b = post(doc)

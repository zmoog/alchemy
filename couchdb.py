#! /bin/env python

import httplib2
import json
import logging
from datetime import datetime
from cash.models import Account, Transfer

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('couchdb-loader')

SERVER="http://localhost:5984"
DATABASE="test"
USERNAME="zmoog"
PASSWORD=""

BASE='%s/%s/' % (SERVER, DATABASE)


def request(uri, body=None, method="GET"):
    headers, body =  client.request(uri , method=method, headers={'Content-Type': 'application/json'}, body=json.dumps(body))
    if headers.status != 201:
        logger.error(body)
        raise Exception("status: %s - but 201 was expected." %(headers.status))
    return headers, body

def post(document):
    return request(BASE, document, method='POST')


if __name__ == '__main__':

    client = httplib2.Http()
    client.add_credentials(USERNAME, PASSWORD)

    accounts = dict()
 
    logger.debug('processing %d account(s)..' % (Account.objects.all().count()))

    for account in Account.objects.all():

        doc = dict(name=account.name, category=account.type, type='account', active=True, created_at=datetime.now().isoformat())

        h, b = post(doc) 
   
        accounts[account.id] = h['location'].split('/')[-1:][0]
        
        logger.debug('account _id is %s for account id %s (%s)' % (accounts[account.id], account.id, account.name))

    logger.info('created %d accounts' % (len(accounts)))

    transfers = Transfer.objects.all()
  
    for transfer in transfers:
        doc = dict(amount=float(transfer.amount), description=transfer.description,source=accounts[transfer.source.id],destination=accounts[transfer.destination.id],opertation_date=transfer.validity_date.isoformat(),validity_date=transfer.validity_date.isoformat(),type='transaction')

        h, b = post(doc)

        
    logger.info('created %d transactions' % (len(transfers)))

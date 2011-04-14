#! /bin/env python

import sys
import csv
import locale
import datetime

from decimal import Decimal
from datetime import datetime
from cash.models import *
from django.db.models import Q

locale.setlocale(locale.LC_ALL,'')

if __name__ == '__main__':

    print('fineco!')
    print(sys.argv)
 
    movimenti = []

    reader = csv.reader(open(sys.argv[1], 'rb'), delimiter=';', quotechar='"')

    for row in reader:
        movimenti.append(row)

    print('Ho trovato %d movimenti.' % (len(movimenti)))

    print('popped %s' % movimenti.pop())

    for t in movimenti:

        dt_operazione = datetime.datetime.strptime(t[0], '%d/%m/%Y')
        dt_valuta = datetime.datetime.strptime(t[1], '%d/%m/%Y')
        amount = Decimal(str(locale.atof(t[2] or t[3])))

        #print('cerco amount di %s ' % amount)

        m = Transfer.objects.filter(amount=amount).filter(Q(validity_date=dt_operazione) | Q(validity_date=dt_valuta))

        if not m: 
            #    print('found! %s' % len(m))
            #else:
            print('MISSING: %s (%s)' % (t[4], t[5]))

        

    print(m)


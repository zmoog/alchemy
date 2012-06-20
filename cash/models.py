# -*- encoding: utf-8 -*-

from django.db import models
from django import forms 
from django.contrib.auth.models import User

import datetime


ACCOUNT_TYPES = (
    ('as', 'Asset'),
    ('cc', 'Conto corrente'),
    ('eq', 'Equity'),
    ('ex', 'Expenses'),
    ('in', 'Income'),
    ('cr', 'Carta di credito'),
)

class Account(models.Model):
    """
    'luogo' dove risiede il denaro (portafogli, conto corrente, tipologia di spesa, etc..).
    """
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=2, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
  
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Transfer(models.Model):
    """
    Trasferimento di denaro da un Account ad un'altro.
    """
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    source = models.ForeignKey(Account, related_name = 'source', help_text="Account da cui prelevare")
    destination = models.ForeignKey(Account, related_name = 'destination', help_text="Account in cui depositare")
    description = models.TextField(help_text="Descrizione del contenuto dell'operazione di trasferimento")
    validity_date = models.DateField(default=datetime.date.today, help_text="Data in cui il trasferimento è diventato effettivo. Ad esempio la valuta di un bonifico, o la data in cui hai acquistato il pane")
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
 
    def __unicode__(self):
        return "%d da %s a %s" % (self.amount, self.source.name, self.destination.name)

    class Meta:
        ordering = ['validity_date']


class TransferForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, localize=True, help_text="Quantità di denaro da trasferire")

    class Meta:
        model = Transfer



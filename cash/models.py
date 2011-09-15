# - encodig: utf8 -
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
    amount = models.DecimalField(max_digits = 10, decimal_places = 2, help_text="Quantita di denaro da trasferire.")
    source = models.ForeignKey(Account, related_name = 'source')
    destination = models.ForeignKey(Account, related_name = 'destination')
    description = models.TextField()
    validity_date = models.DateField(default=datetime.date.today)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
 
    def __unicode__(self):
        return "%d da %s a %s" % (self.amount, self.source.name, self.destination.name)

    class Meta:
        ordering = ['validity_date']


class TransferForm(forms.ModelForm):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, localize=True, help_text="Quantita")

    class Meta:
        model = Transfer



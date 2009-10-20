from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django import forms 
from django.db.models import Q
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic import list_detail

import decimal
import datetime

from alchemy.cash.models import Account, Transfer, TransferForm


def my_object_list(request, paginate_by, page=None):
    queryset = Transfer.objects.filter()

    if request.GET.has_key('description'):
        queryset = queryset.filter(description__icontains=request.GET['description'])

    return list_detail.object_list(request, queryset=queryset, paginate_by=paginate_by, page=page)
        


def transfer(request, object_id):
    latest = Transfer.objects.order_by('-created_on')[:10] 
    transfer = get_object_or_404(Transfer, pk=object_id)

    if request.method == 'POST':
        form = TransferForm(request.POST, instance=transfer)   
        if form.is_valid():
            form.save()
            request.user.message_set.create(message="Transfer aggiornato con successo")
            return HttpResponseRedirect(reverse('transfer-detail', kwargs=dict(object_id=transfer.id))) # redirect after post

    else:
        form = TransferForm(instance=transfer)

    return render_to_response('cash/transfer_add.html', {'form': form, 'latest': latest}, context_instance=RequestContext(request))


def transfer_add(request):
    """
    View for handling the creation/modify of the Transfer objects.
    """
    latest = Transfer.objects.order_by('-created_on')[:10] 
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            form.save()
            request.user.message_set.create(message="%s" % form['notify_recipients'].field)
            return HttpResponseRedirect(reverse('transfer-add')) # redirect after post
    else:
        form = TransferForm() # an unbound form

    return render_to_response('cash/transfer_add.html', {'form': form, 'latest': latest}, context_instance=RequestContext(request))


def report(request):
    now = datetime.datetime.now()
    return HttpResponseRedirect( reverse('report-month', kwargs=dict(year=now.year, month=now.month)))


def report_month(request, year, month):
    """
    Build the monthly report view
    """
    queryset = Transfer.objects.filter(Q(destination__type='ex') | Q(source__type='in'), validity_date__month=int(month), validity_date__year=int(year)).order_by('-validity_date')
 
    income = { 'tot': 0, 'transfers': []}
    expense = { 'tot': 0, 'transfers': [], 'x': {} }

    for transfer in queryset:

        if transfer.destination.type == 'ex':
            expense['transfers'].append(transfer)
            expense['tot'] += transfer.amount

            if expense['x'].has_key(transfer.destination.id):
                expense['x'][transfer.destination.id]['tot'] += transfer.amount
            else:
                expense['x'][transfer.destination.id] = { 'name': transfer.destination.name, 'tot': transfer.amount }

        if transfer.source.type == 'in':
            income['transfers'].append(transfer)
            income['tot'] += transfer.amount

    else:
        expense['y'] = list()
        for key in expense['x'].keys(): 
            x = expense['x'][key]
            x['id'] = key
            expense['y'].append(x)
 

    context = {
        'year': int(year),
        'month': int(month),
        'first_day': datetime.date(int(year), int(month), 1),
        'months': Transfer.objects.filter(Q(destination__type='ex') | Q(source__type='in')).dates('validity_date', 'month'),
        'expense_list': expense,
        'income_list': income,
        'balance': income['tot'] - expense['tot']
    }

    return render_to_response('cash/report_month.html', context, context_instance=RequestContext(request))



def account_detail_monthly(request, object_id, year, month):
    """
    """
    return account_detail(request, object_id, year, month)
    
    

def account_detail(request, object_id, year=None, month=None):

    print object_id, year, month

    account = get_object_or_404(Account, pk=object_id)
    transfer_list = Transfer.objects.filter(Q(source__id = object_id) | Q(destination__id = object_id)).order_by('-validity_date')
   
    # Aggiornamento del bilancio dell'Account
    # FIXME: occorre sostituire questo metodo con qualcosa di diverso..
    if not year and not month:
    
        account.balance = decimal.Decimal('0')

        for transfer in transfer_list: 
            if account.id == transfer.destination.id:
                account.balance += transfer.amount
            else:
                account.balance -= transfer.amount
   
        account.save()

    months = transfer_list.dates('validity_date', 'month')

    if year:
        print 'append %s' % year
        transfer_list = transfer_list.filter(validity_date__year=int(year))

    if month:
        print 'append %s' % month
        transfer_list = transfer_list.filter(validity_date__month=int(month))


	print transfer_list

    context = {
        'object': account,
        'transfer_list': transfer_list,
        'months': months
    }
    
    return render_to_response('cash/account_detail.html', context, context_instance=RequestContext(request))



def sandbox(request, object_id, year):
    """
    View for hacks experimentation.
    """
    
    account = get_object_or_404(Account, pk=object_id)
    
    queryset = Transfer.objects.filter(Q(destination__id=account.id) | Q(source__id=account.id), validity_date__year=int(year)).order_by('validity_date')
   
    tot = { 
        'deposit': { 'data': {}, 'op': lambda a,b : a + b }, 
        'withdraw': { 'data': {}, 'op': lambda a,b : a - b },
        'balance': {}
    }
        
    balance = 0
    last = None
    
    for transfer in queryset:

        if transfer.destination.id == account.id:
            kind = 'deposit'
        else:
            kind = 'withdraw'
    
        balance = tot[kind]['op'](balance, transfer.amount)
    
        key = transfer.validity_date.month


        tot['balance'][key] = balance

            
        if tot[kind]['data'].has_key(key):
            tot[kind]['data'][key]['amount'] += transfer.amount
        else:
            tot[kind]['data'][key] = {'date': transfer.validity_date, 'amount': transfer.amount } 
        

    data = { 'deposit': 0, 'withdraw': 0, 'balance': 0 }
    summary = []
    
    for month in range(1,13):
    
        data = { 'deposit': 0, 'withdraw': 0, 'balance': data['balance'] }
        
        if tot['balance'].has_key(month):
            data['balance']  = tot['balance'][month]
            
        if tot['deposit']['data'].has_key(month):
            data['deposit'] = tot['deposit']['data'][month]['amount']

        if tot['withdraw']['data'].has_key(month):
            data['withdraw'] = tot['withdraw']['data'][month]['amount']
            
        summary.append(data.copy())
        
        
    context = { 'object': account, 'accounts': Account.objects.all().order_by('type', 'name'), 'year': int(year), 'tot': tot, 'summary': summary }
    
    return render_to_response('cash/sandbox.html', context, context_instance=RequestContext(request))


def _sandbox(request, object_id):
    """
    View for hacks experimentation.
    """
    
    account = get_object_or_404(Account, pk=object_id)
    
    
    deposits = account.destination.all()
    withdraws = account.source.all()
    
    tot = { 
        'deposit': { 'queryset': deposits, 'data': {}, 'op': lambda a,b : a + b }, 
        'withdraw': { 'queryset': withdraws, 'data': {}, 'op': lambda a,b : a - b } 
    }
        
    for kind in tot.keys():
        
        for transfer in tot[kind]['queryset']:
            
            key = transfer.validity_date.month
            
            if tot[kind]['data'].has_key(key):
                tot[kind]['data'][key]['amount'] += transfer.amount
            else:
                tot[kind]['data'][key] = {'date': transfer.validity_date, 'amount': transfer.amount } 
        
    context = { 'account': account, 'tot': tot }
    
    return render_to_response('cash/sandbox.html', context, context_instance=RequestContext(request))

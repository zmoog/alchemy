from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect
from django import forms 
from django.db import transaction
from django.db.models import Q, Sum
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic import list_detail
from django.contrib import messages

import decimal
import datetime

from cash.models import Account, Transfer, TransferForm


def transfer_archive(request, queryset, paginate_by):
    """
    """
 
    if request.GET.has_key('description'):
        queryset = queryset.filter(description__icontains=request.GET['description'])

    paginator = Paginator(queryset, paginate_by) # Show 'paginate_by' transfers per page
    
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    # If page request (9999) is out of range, deliver last page of results.
    try:
       transfers = paginator.page(page)
    except (EmptyPage, InvalidPage):
       transfers = paginator.page(paginator.num_pages)

    return render_to_response('cash/transfer_list.html', {'transfers': transfers}, context_instance=RequestContext(request)) 


def transfer_archive_year(request, year, queryset, paginate_by):
    return transfer_archive(request, queryset.filter(validity_date__year=int(year)), paginate_by)


def transfer_archive_month(request, year, month, queryset, paginate_by):
    return transfer_archive(request, queryset.filter(
            validity_date__year=int(year),
            validity_date__month=int(month)), paginate_by)


def transfer_archive_day(request, year, month, day, queryset, paginate_by):
    return transfer_archive(request,
        queryset.filter(
            validity_date__year=int(year),
            validity_date__month=int(month),
            validity_date__day=int(day)), paginate_by)


@transaction.commit_on_success()
def transfer(request, object_id):
    latest = Transfer.objects.order_by('-created_on')[:10] 
    transfer = get_object_or_404(Transfer, pk=object_id)

    if request.method == 'POST':
        form = TransferForm(request.POST, instance=transfer)   
        if form.is_valid():
            form.save()
            #request.user.message_set.create(message="Transfer aggiornato con successo")
            messages.success(request, 'Transfer updated successfully.')
            _update_balance([form.instance.source, form.instance.destination])
            return HttpResponseRedirect(reverse('transfer-detail', kwargs=dict(object_id=transfer.id))) # redirect after post

    else:
        form = TransferForm(instance=transfer)

    return render_to_response('cash/transfer_add.html', {'form': form, 'latest': latest}, context_instance=RequestContext(request))


@transaction.commit_on_success()
def transfer_add(request):
    """
    View for handling the creation/modify of the Transfer objects.
    """
    latest = Transfer.objects.order_by('-created_on')[:10] 
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            form.save()
            _update_balance([form.instance.source, form.instance.destination])
            #request.user.message_set.create(message="%s" % form['notify_recipients'].field)
            return HttpResponseRedirect(reverse('transfer-add')) # redirect after post
    else:
        form = TransferForm() # an unbound form

    return render_to_response('cash/transfer_add.html', {'form': form, 'latest': latest}, context_instance=RequestContext(request))


def report(request):
    now = datetime.datetime.now()
    return HttpResponseRedirect(reverse('report-month', kwargs=dict(year=now.year, month=now.month)))


def _do_balance(queryset):
    """
    """

    income = { 'tot': 0, 'transfers': []}
    expense = { 'tot': 0, 'transfers': [], 'x': {} }
    rebate = { 'tot': 0, 'transfers': []}

    final_queryset = queryset.filter(
        Q(destination__type='ex') | 
        Q(source__type='in') | 
        Q(source__type='ex'))
 
    for transfer in final_queryset:

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

        if transfer.source.type == 'ex':
            rebate['transfers'].append(transfer)
            rebate['tot'] += transfer.amount

            if expense['x'].has_key(transfer.source.id):
                expense['x'][transfer.source.id]['tot'] -= transfer.amount
            else:
                expense['x'][transfer.source.id] = { 'name': transfer.source.name, 'tot': -transfer.amount }


    else:
        expense['y'] = list()
        for key in expense['x'].keys(): 
            x = expense['x'][key]
            x['id'] = key
            expense['y'].append(x)
 

    balance = income['tot'] - expense['tot'] + rebate['tot']

    return balance, income, expense, rebate, final_queryset
    

def report_year(request, year):
    """
    Build the year report view
    """
    #base_queryset = Transfer.objects.filter(Q(destination__type='ex') | Q(source__type='in'))
        
    queryset = Transfer.objects.filter(validity_date__year=int(year)).order_by('-validity_date')
 
    balance, income, expense, rebate, qs = _do_balance(queryset)

    context = {
        'year': int(year),
        #'month': int(month),
        #'first_day': datetime.date(int(year), int(month), 1),
        'months': qs.dates('validity_date', 'month', order="DESC"),
        'expense_list': expense,
        'income_list': income,
        'rebate_list': rebate,
        'balance': balance
    }


    return render_to_response(
        'cash/report_year.html', 
        context, 
        context_instance=RequestContext(request))


def report_month(request, year, month):
    """
    Build the monthly report view
    """
    #base_queryset = Transfer.objects.filter(
    #    Q(destination__type='ex') | 
    #    Q(source__type='in') | 
    #    Q(source__type='ex'))
        
    queryset = Transfer.objects.filter(
        validity_date__month=int(month), validity_date__year=int(year)).order_by('-validity_date')
 
    balance, income, expense, rebate, qs = _do_balance(queryset)

    context = {
        'year': int(year),
        'month': int(month),
        'first_day': datetime.date(int(year), int(month), 1),
        'months': qs.dates('validity_date', 'month', order="DESC"),
        'expense_list': expense,
        'income_list': income,
        'rebate_list': rebate,
        'balance': balance
    }

    return render_to_response(
        'cash/report_month.html', 
        context, 
        context_instance=RequestContext(request))


def report_day(request, year, month, day):
    """
    Build the monthly report view
    """
    #base_queryset = Transfer.objects.filter(Q(destination__type='ex') | Q(source__type='in'))
        
    queryset = Transfer.objects.filter(
        validity_date__month=int(month), 
        validity_date__year=int(year),
        validity_date__day=int(day)).order_by('-validity_date')
 
    balance, income, expense, rebate, qs = _do_balance(queryset)

    context = {
        'year': int(year),
        'month': int(month),
        'day': int(day),        
        'first_day': datetime.date(int(year), int(month), int(day)),
        'months': qs.dates('validity_date', 'month', order="DESC"),
        'expense_list': expense,
        'income_list': income,
        'balance': balance
    }

    return render_to_response(
        'cash/report_day.html', 
        context, 
        context_instance=RequestContext(request))



def old_report_month(request, year, month):
    """
    Build the monthly report view
    """
    base_queryset = Transfer.objects.filter(Q(destination__type='ex') | Q(source__type='in'))
        
    queryset = base_queryset.filter(
        validity_date__month=int(month), validity_date__year=int(year)).order_by('-validity_date')
 
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
        'months': base_queryset.dates('validity_date', 'month', order="DESC"),
        'expense_list': expense,
        'income_list': income,
        'balance': income['tot'] - expense['tot']
    }


    return render_to_response(
        'cash/report_month.html', 
        context, 
        context_instance=RequestContext(request))



def account_detail_monthly(request, object_id, year, month):
    """
    """
    return account_detail(request, object_id, year, month)
    
    

def account_detail(request, object_id, year=None, month=None):
    """
    """

    account = get_object_or_404(Account, pk=object_id)
    transfer_list = Transfer.objects.filter(
            Q(source__id = object_id) | Q(destination__id = object_id)
        ).order_by('-validity_date')

    months = transfer_list.dates('validity_date', 'month', order="DESC")

    if year:
        transfer_list = transfer_list.filter(validity_date__year=int(year))

    if month:
        transfer_list = transfer_list.filter(validity_date__month=int(month))

    context = {
        'now': datetime.datetime.now(),
        'object': account,
        'transfer_list': transfer_list[:10],
        'count': transfer_list.count(),
        'months': months
    }
    
    return render_to_response(
        'cash/account_detail.html', 
        context, 
        context_instance=RequestContext(request))



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


def _update_balance(account_list):
    """
    Update the balance for each Account in the list given as a parameter.

    The current implementation uses a sum() aggregation function to obtain INs and OUTs transfer sums
    and then apply this formula: 

        balance = INs - OUTs.

    """

    for account in account_list:
 
        print('current %s balance is %f' % (account.name, account.balance))
        ins = Transfer.objects.filter(Q(destination__id=account.id)).aggregate(Sum('amount'))['amount__sum'] or 0
        outs = Transfer.objects.filter(Q(source__id=account.id)).aggregate(Sum('amount'))['amount__sum'] or 0
        balance = ins - outs
        print('in %f and out %f, so new balance for %s is %f' % (ins, outs, account, balance))
        account.balance = balance
        account.save() 

  

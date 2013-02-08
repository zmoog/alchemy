from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q, Sum
from django.template import RequestContext

import datetime

from cash.models import Account, Transfer



def report(request):
    """ 
    Redirect to the current monthly report.
    """
    now = datetime.datetime.now()
    return HttpResponseRedirect(reverse('report-month', kwargs=dict(year=now.year, month=now.month)))



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
        'report/report_year.html', 
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
        'report/report_month.html', 
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
        'report/report_day.html', 
        context, 
        context_instance=RequestContext(request))


def _do_balance(queryset):
    """
    """

    income = { 'tot': 0, 'transfers': []}
    expense = { 'tot': 0, 'transfers': [], 'x': {} }
    rebate = { 'tot': 0, 'transfers': []}

    final_queryset = queryset.select_related().filter(
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
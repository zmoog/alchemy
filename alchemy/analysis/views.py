from django.shortcuts import get_object_or_404, render_to_response
from django.db.models import Q, Sum
from django.template import RequestContext

from cash.models import Account, Transfer


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
    
    return render_to_response('analysis/sandbox.html', context, context_instance=RequestContext(request))


# def _sandbox(request, object_id):
#     """
#     View for hacks experimentation.
#     """
#     
#     account = get_object_or_404(Account, pk=object_id)
#     
#     
#     deposits = account.destination.all()
#     withdraws = account.source.all()
#     
#     tot = { 
#         'deposit': { 'queryset': deposits, 'data': {}, 'op': lambda a,b : a + b }, 
#         'withdraw': { 'queryset': withdraws, 'data': {}, 'op': lambda a,b : a - b } 
#     }
#         
#     for kind in tot.keys():
#         
#         for transfer in tot[kind]['queryset']:
#             
#             key = transfer.validity_date.month
#             
#             if tot[kind]['data'].has_key(key):
#                 tot[kind]['data'][key]['amount'] += transfer.amount
#             else:
#                 tot[kind]['data'][key] = {'date': transfer.validity_date, 'amount': transfer.amount } 
#         
#     context = { 'account': account, 'tot': tot }
#     
#     return render_to_response('cash/sandbox.html', context, context_instance=RequestContext(request))


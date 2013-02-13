from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django import forms 
from django.db import transaction
from django.db.models import Q, Sum
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.generic import list_detail
from django.views.generic import DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import decimal
import datetime
import unicodecsv as csv

from cash.models import Account, Transfer, TransferForm


def transfer_archive(request, queryset, paginate_by):
    """
    """
 
    if request.GET.has_key('description'):
        queryset = queryset.filter(description__icontains=request.GET['description'])

    queryset = queryset.select_related()

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

    latest = Transfer.objects.select_related().order_by('-created_on')[:10] 

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
    latest = Transfer.objects.select_related().order_by('-created_on')[:10] 

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



    


def account_detail_monthly(request, object_id, year, month):
    """
    """
    return account_detail(request, object_id, year, month)
    
@login_required
def account_detail_csv(request, object_id, year=None, month=None):
    """
    Accounts transfers as CSV file.
    """

    response = HttpResponse(mimetype='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename=somefilename.csv'

    writer = csv.writer(response)

    #writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    #writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    transfer_list, month_list = _account_detail(object_id, year, month)

    for transfer in transfer_list:
        writer.writerow([transfer.validity_date, transfer.source, transfer.destination, transfer.amount, transfer.description])

    return response



def _account_detail(object_id, year=None, month=None):
    """
    """
    
    transfer_list = Transfer.objects.select_related().filter(
            Q(source__id = object_id) | Q(destination__id = object_id)
        ).order_by('-validity_date')

    month_list = transfer_list.dates('validity_date', 'month', order="DESC")

    if year:
        transfer_list = transfer_list.filter(validity_date__year=int(year))

    if month:
        transfer_list = transfer_list.filter(validity_date__month=int(month))

    return transfer_list, month_list




class BaseAccountDetailView(DetailView):

    model = Account

    def get_context_data(self, **kwargs):

        context = super(BaseAccountDetailView, self).get_context_data(**kwargs)

        object_id = self.object.id

        #transfer_list, month_list = _account_detail(self.object.id)
        transfer_list = Transfer.objects.select_related().filter(
            Q(source__id = object_id) | Q(destination__id = object_id)
        ).order_by('-validity_date')

        # add extra context data
        context['now'] = datetime.datetime.now()
        context['transfer_list'] = transfer_list
        context['count'] = transfer_list.count()

        return context


class AccountDetailView(BaseAccountDetailView):

    def get_context_data(self, **kwargs):
        context = super(AccountDetailView, self).get_context_data(**kwargs)
        context['transfer_list'] = context['transfer_list'][:10]
        return context


def account_detail(request, object_id, year=None, month=None):
    """
    All transfers of the given account.
    """

    account = get_object_or_404(Account, pk=object_id)

    #account = get_object_or_404(Account, pk=object_id)
    #transfer_list = Transfer.objects.filter(
    #        Q(source__id = object_id) | Q(destination__id = object_id)
    #    ).order_by('-validity_date')
    #
    #months = transfer_list.dates('validity_date', 'month', order="DESC")
    #
    #if year:
    #    transfer_list = transfer_list.filter(validity_date__year=int(year))
    #
    #if month:
    #    transfer_list = transfer_list.filter(validity_date__month=int(month))

    transfer_list, month_list = _account_detail(object_id, year, month)

    context = {
        'now': datetime.datetime.now(),
        'object': account,
        'transfer_list': transfer_list[:10],
        'count': transfer_list.count(),
        'months': month_list
    }
    
    return render_to_response(
        'cash/account_detail.html', 
        context, 
        context_instance=RequestContext(request))

    

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

  

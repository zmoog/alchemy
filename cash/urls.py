from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template
from alchemy.cash.models import Account, Transfer
from alchemy.cash.views import account_detail, account_detail_monthly, report, report_month, transfer, transfer_add, sandbox, my_object_list

account_info = {
    'queryset': Account.objects.all().order_by('type', 'name')
}

transfer_list_info = {
    #'queryset': Transfer.objects.all().order_by('-validity_date'),
    'paginate_by': 10
}

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'cash/home.html'}, name='cash-home'),
    
    url(r'^transfer/$', login_required(my_object_list), transfer_list_info, name='transfer-list'),
    url(r'^transfer/-description-like-/(?P<description>\d+)/$', login_required(my_object_list), transfer_list_info, name='transfer-list-description-like'),
    
    url(r'^transfer/add/$', login_required(transfer_add), name='transfer-add'),
    url(r'^transfer/(?P<object_id>\d+)/$', login_required(transfer), name='transfer-detail'),
    url(r'^report/$', login_required(report), name="report"), 
    url(r'^report/(?P<year>\d+)/(?P<month>\d+)/$', login_required(report_month), name="report-month"), 
    url(r'^account/$', login_required(object_list), account_info, name='account'),
    
    url(r'^account/(?P<object_id>\d+)/$', login_required(account_detail), name="account-detail"),
    url(r'^account/(?P<object_id>\d+)/(?P<year>\d+)/$', login_required(account_detail), name="account-detail-annual"),
    url(r'^account/(?P<object_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', login_required(account_detail_monthly), name="account-detail-monthly"),
    
    url(r'^account/(?P<object_id>\d+)/analysis/(?P<year>\d+)/$', login_required(sandbox), name='sandbox'),
)

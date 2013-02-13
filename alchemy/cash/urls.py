from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required

from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template

from django.views.generic import DetailView

from .models import Account, Transfer
#from cash.views import *
from .views import AccountDetailView
from .views import transfer_add, transfer, account_detail, account_detail_monthly, transfer_archive, transfer_archive_year, transfer_archive_month, transfer_archive_day, account_detail_csv



account_info = {
    'queryset': Account.objects.all().order_by('type', 'name')
}

transfer_list_info = {
    'queryset': Transfer.objects.all().order_by('-validity_date'),
    'paginate_by': 10
}



urlpatterns = patterns('',

    url(r'^$', direct_to_template, {'template': 'cash/home.html'}, name='cash-home'),
    
    #url(r'^transfer/-description-like-/(?P<description>\d+)/$', login_required(my_object_list), transfer_list_info, name='transfer-list-description-like'),
    
    url(r'^transfer/add/$', login_required(transfer_add), name='transfer-add'),
    url(r'^transfer/(?P<object_id>\d+)/$', login_required(transfer), name='transfer-detail'),
    url(r'^transfer/(?P<pk>\d+)/delete/$', login_required(DetailView.as_view(model=Transfer, template_name='cash/transfer_delete.html')), name='transfer-delete'),

    url(r'^transfer/archive/$', login_required(transfer_archive), transfer_list_info, name='transfer-archive'),
    url(r'^transfer/archive/(?P<year>\d+)/$', login_required(transfer_archive_year), transfer_list_info, name='transfer-archive-year'),
    url(r'^transfer/archive/(?P<year>\d+)/(?P<month>\d+)/$', login_required(transfer_archive_month), transfer_list_info, name='transfer-archive-month'),
    url(r'^transfer/archive/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', login_required(transfer_archive_day), transfer_list_info, name='transfer-archive-day'),

    # url(r'^report/$', login_required(report), name="report"),    
    # url(r'^report/(?P<year>\d+)/$', login_required(report_year), name="report-year"),    
    # url(r'^report/(?P<year>\d+)/(?P<month>\d+)/$', login_required(report_month), name="report-month"), 
    # url(r'^report/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', login_required(report_day), name="report-day"), 
    
    url(r'^account/$', login_required(object_list), account_info, name='account'),
    
    #url(r'^account/(?P<object_id>\d+)/$', login_required(account_detail), name="account-detail"),
    url(r'^account/(?P<pk>\d+)/$', AccountDetailView.as_view(), name="account-detail"),



    url(r'^account/(?P<object_id>\d+)/csv/$', account_detail_csv, name="account-detail-csv"),
    url(r'^account/(?P<object_id>\d+)/(?P<year>\d+)/$', login_required(account_detail), name="account-detail-annual"),
    url(r'^account/(?P<object_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$', login_required(account_detail_monthly), name="account-detail-monthly"),
    
    
)

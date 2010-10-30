from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.simple import direct_to_template
from cash.models import Account, Transfer
from cash.views import account_detail, account_detail_monthly, report, report_year, report_month, report_day, transfer, transfer_archive, transfer_archive_year, transfer_archive_month, transfer_archive_day, transfer_add, sandbox

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'mobile/index.html'}, name='mobile-index'),
)

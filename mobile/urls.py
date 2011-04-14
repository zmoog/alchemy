from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.generic.simple import direct_to_template
from cash.models import Account, Transfer

from django.views.generic import ListView, DetailView


urlpatterns = patterns('',
    (r'^accounts/$', 
        ListView.as_view(model=Account, template_name='mobile/account_list.html')
    ),
    (r'^accounts/(?P<pk>\d+)/$', 
        DetailView.as_view(model=Account, template_name='mobile/account_detail.html')
    ),
 
    #url(r'^$', direct_to_template, {'template': 'mobile/index.html'}, name='mobile-index'),
)

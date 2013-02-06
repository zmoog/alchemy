from django.conf.urls.defaults import *

from .views import report, report_year, report_month, report_day

urlpatterns = patterns('',

    url(r'^$', report, name="report"),    
    url(r'^(?P<year>\d+)/$', report_year, name="report-year"),    
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$', report_month, name="report-month"), 
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', report_day, name="report-day"), 

)
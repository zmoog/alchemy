from django.conf.urls.defaults import *

from .views import sandbox

urlpatterns = patterns('',

    url(r'^account/(?P<object_id>\d+)/(?P<year>\d+)/$', sandbox, name='sandbox'), 
)
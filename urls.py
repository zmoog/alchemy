from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib import databrowse
from cash.models import Account, Transfer
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment this for admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^databrowse/(.*)', databrowse.site.root, name='databrowse'),

    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

    url(r'^m/(.*)', include('mobile.urls')),


    url(r'^', include('cash.urls')),
)

if settings.DEBUG:

    urlpatterns += patterns('', 
        url(r'^media/static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),
    )

databrowse.site.register(Account)
databrowse.site.register(Transfer)

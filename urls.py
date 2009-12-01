from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib import databrowse
from alchemy.cash.models import Account, Transfer
import settings

admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment this for admin:
    url(r'^admin/(.*)', admin.site.root, name='admin'),
    url(r'^databrowse/(.*)', databrowse.site.root, name='databrowse'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),

    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),

    url(r'^', include('alchemy.cash.urls')),
)

databrowse.site.register(Account)
databrowse.site.register(Transfer)
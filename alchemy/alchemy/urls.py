from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib import databrowse
from cash.models import Account, Transfer
from django.conf import settings
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.api import Api
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.authentication import ApiKeyAuthentication

admin.autodiscover()

class AccountResource(ModelResource):
    class Meta:
        queryset = Account.objects.all()
        filtering = {
            'name': ALL
        }
        excludes = ['balance']
        authentication = ApiKeyAuthentication()

class TransferResource(ModelResource):
    source = fields.ForeignKey(AccountResource, 'source', full=True)
    destination = fields.ForeignKey(AccountResource, 'destination', full=True)
    class Meta:
        queryset = Transfer.objects.all()
        filtering = {
            'description': ALL,
            'amount': ALL
        }
        ordering = ['created_on', 'validity_date']
        authentication = ApiKeyAuthentication()



v1_api = Api(api_name='v1')
v1_api.register(AccountResource())
v1_api.register(TransferResource())



urlpatterns = patterns('',

    # Uncomment this for admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^databrowse/(.*)', databrowse.site.root, name='databrowse'),

    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

    # url(r'^m/', include('mobile.urls')),

    url(r'^api/', include(v1_api.urls)),

    url(r'^report/', include('report.urls')),
    url(r'^analysis/', include('analysis.urls')),

    url(r'^', include('cash.urls')),
)

#if settings.DEBUG:
#    urlpatterns += patterns('', 
#        url(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),
#    )

databrowse.site.register(Account)
databrowse.site.register(Transfer)

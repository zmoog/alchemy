from django.conf.urls.defaults import *
from django.contrib import admin
###from django.contrib import databrowse
#from cash.models import Account, Transfer
from api import views
from django.conf import settings
from rest_framework import routers


admin.autodiscover()


router = routers.DefaultRouter()
router.register(r'accounts', views.AccountViewSet)
router.register(r'transfers', views.TransferViewSet)
#
#router.register(r'accounts2', views.AccountView)


urlpatterns = patterns('',

    # Uncomment this for admin:
    url(r'^admin/', include(admin.site.urls)),
    ##url(r'^databrowse/(.*)', databrowse.site.root, name='databrowse'),#

    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

    # url(r'^m/', include('mobile.urls')),

    #url(r'^api/', include(v1_api.urls)),
 
    url(r'^api/', include(router.urls)),
    url(r'^api/api-auth', include('rest_framework.urls', namespace='api/rest_framework')),



    url(r'^report/', include('report.urls')),
    url(r'^analysis/', include('analysis.urls')),

    # Singe Page App
    url(r'^spa/', include('spa.urls')),

    url(r'^', include('cash.urls')),
)

#if settings.DEBUG:
#    urlpatterns += patterns('', 
#        url(r'^(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT, 'show_indexes': True}),
#    )

#databrowse.site.register(Account)
#databrowse.site.register(Transfer)

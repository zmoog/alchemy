from django.conf.urls import patterns, url

from spa.views import SpaView

urlpatterns = patterns('',
    url(r'^$', SpaView.as_view(), name='home'),
)
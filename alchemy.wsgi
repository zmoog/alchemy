ALLDIRS = ['/home/django/domains/alchemy.selfip.biz/alchemy.selfip.biz/lib/python2.6/site-packages']
# note that the above directory depends on the locale of your virtualenv,
# and will thus be *different for each project!*
import os
import sys
import site

prev_sys_path = list(sys.path)

for directory in ALLDIRS:
    site.addsitedir(directory)

new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
       new_sys_path.append(item)
       sys.path.remove(item)
sys.path[:0] = new_sys_path

# this will also be different for each project!
sys.path.append('/home/django/domains/alchemy.selfip.biz/alchemy/')

os.environ['PYTHON_EGG_CACHE'] = '/home/django/.python-eggs'
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    environ['wsgi.url_scheme'] = environ.get('HTTP_X_URL_SCHEME', 'http')
    return _application(environ, start_response)

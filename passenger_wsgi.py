import os, sys
import site

site.addsitedir('/opt/webapps/viriato.reactivelab.com/lib/python2.6/site-packages')
site.addsitedir('/opt/webapps/viriato.reactivelab.com/src/viriato-trunk')
site.addsitedir('/opt/webapps/viriato.reactivelab.com/src/viriato-trunk/viriato')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

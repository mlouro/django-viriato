# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^account/',  include('django_authopenid.urls')),

    # apps
    #(r'^calendar/', include('schedule.urls')),
    (r'^projects/', include('projects.urls')),

    (r'^invoices/contract/', include('contract.urls')),
    (r'^invoices/company/', include('company.urls')),
    (r'^invoices/receipt/', include('receipt.urls')),



    (r'^$',         include('core.urls')),
)



if getattr(settings, 'LOCAL_DEV', True):
    urlpatterns += patterns('django.views.static',
        (r'^static/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )
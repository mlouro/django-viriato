# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    (r'^admin/translations/', include('rosetta.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),

    # apps
    #(r'^calendar/', include('schedule.urls')),
    (r'^projects/', include('projects.urls')),

    (r'^invoices/$', include('invoices.urls')),
    (r'^invoices/contract/', include('contract.urls')),
    (r'^invoices/company/', include('company.urls')),
    (r'^invoices/receipt/', include('receipt.urls')),


    (r'^newsletter/', include('newsletter.urls')),

    (r'^$',         include('core.urls')),
)


urlpatterns += patterns('',
    url(r'^set_language/(?P<lang_code>\w+)/$', 'urls.set_language', name="set_language"),
)


if getattr(settings, 'LOCAL_DEV', True):
    urlpatterns += patterns('django.views.static',
        (r'^static/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )


# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext

def set_language(request, lang_code):
    request.session['django_language'] = lang_code
    return HttpResponseRedirect("/")
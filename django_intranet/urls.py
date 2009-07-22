# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^account/',  include('django_authopenid.urls')),
    (r'^avatar/',   include('avatar.urls')),

    # apps
    (r'^$',         include('dashboard.urls')),
    (r'^calendar/', include('schedule.urls')),
    (r'^projects/', include('projects.urls')),
    (r'^issues/',   include('issue.urls')),


    url(r'^show_url_patterns/', 'common.views.show_url_patterns'),
)



if getattr(settings, 'LOCAL_DEV', True):
    urlpatterns += patterns('django.views.static',
        (r'^site_media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
    )

# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^(?P<contact_type>\w+)/save/$', 'contact.views.save'),
    #(r'^(?P<contact_type>\w+)/(?P<contact_id>\w+)/addnote/$', 'contact.views.addnote'),
    (r'^(?P<contact_type>\w+)/save/(?P<contact_id>\w+)/$', 'contact.views.save'),
    (r'^(?P<contact_type>\w+)/(?P<contact_id>\w+)/$', 'contact.views.details'),
    (r'^search/$', 'contact.views.search'),
    (r'^$', 'contact.views.search'),
)
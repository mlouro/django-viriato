# -*- coding: utf-8 -*-
# invoices
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'invoices.views.index', name="invoices_index"),
)
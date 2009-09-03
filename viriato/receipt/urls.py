# -*- coding: utf-8 -*-
#Receipt
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'receipt.views.receipt', name="receipt_index"),
    (r'^(?P<object_id>\d+)/$', 'receipt.views.receipt'),
    (r'^receipt_document/(?P<object_id>\d+)/$', 'receipt.views.receipt_document'),
)
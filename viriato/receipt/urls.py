# -*- coding: utf-8 -*-
#Receipt
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^index/$', 'receipt.views.index', name="receipt_index"),
    url(r'^$', 'receipt.views.receipt', name="receipt"),
    (r'^(?P<object_id>\d+)/$', 'receipt.views.receipt'),
    url(r'^download_document/(?P<object_id>\d+)/$', 'receipt.views.download_document', name="download_document"),
    url(r'^send_document/(?P<object_id>\d+)/$', 'receipt.views.send_document', name="send_document"),
)
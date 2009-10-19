# -*- coding: utf-8 -*-
#Receipt
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'receipt.views.index', name="receipt_index"),
    url(r'^add/$', 'receipt.views.receipt', name="receipt_add"),
    url(r'^(?P<object_id>\d+)/$', 'receipt.views.receipt', name="receipt_add"),
    url(r'^download_document/(?P<object_id>\d+)/$', 'receipt.views.download_document', name="download_document"),
    url(r'^send_document/(?P<object_id>\d+)/$', 'receipt.views.send_document', name="send_document"),
)
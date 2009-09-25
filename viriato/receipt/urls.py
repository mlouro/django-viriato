# -*- coding: utf-8 -*-
#Receipt
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'receipt.views.receipt', name="receipt_index"),
    (r'^(?P<object_id>\d+)/$', 'receipt.views.receipt'),
    url(r'^download_document/(?P<object_id>\d+)/$', 'receipt.views.download_document', name="download_document"),
    url(r'^send_document/(?P<object_id>\d+)/$', 'receipt.views.send_document', name="send_document"),
)
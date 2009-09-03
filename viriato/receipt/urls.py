# -*- coding: utf-8 -*-
#Receipt
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'receipt.views.receipt'),
    (r'^(?P<object_id>\d+)/$', 'receipt.views.receipt'),
    (r'^receipt_document/(?P<object_id>\d+)/$', 'receipt.views.receipt_document'),
)
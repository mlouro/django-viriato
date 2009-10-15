# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 'company.views.company', name="company"),
    (r'^company_ajax/$', 'company.views.company_ajax'),
)


# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^$', 'company.views.company'),
    (r'^company_ajax/$', 'company.views.company_ajax'),
)


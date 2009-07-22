# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 'issue.views.dashboard', name='issue_dashboard'),
)


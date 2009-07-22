# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^$', 'project.views.dashboard', name='project_dashboard'),
    url(r'^(?P<trash>.*)/$', 'project.views.trashboard', name='project_trashboard'),
    url(r'^(?P<trash>.*)/(?P<can>.*)/$', 'project.views.trashcan', name='project_trashcan'),
)


# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *


# milestone views
urlpatterns = patterns('projects.views.milestone',
    url(r'(?P<project_id>\d+)/milestone/save/$', 'save'),
    url(r'(?P<project_id>\d+)/milestone/save/(?P<milestone_id>[0-9]+)/$', 'save'),
    url(r'(?P<project_id>\d+)/milestone/$', 'index', name="milestone_index"),
)

# message views
urlpatterns += patterns('projects.views.message',
    url(r'(?P<project_id>\d+)/message/details/(?P<message_id>[0-9]+)/$', 'details', name="message_details"),
    url(r'(?P<project_id>\d+)/message/save/$', 'save', name='message_add'),
    url(r'(?P<project_id>\d+)/message/save/(?P<message_id>[0-9]+)/$', 'save'),
    url(r'(?P<project_id>\d+)/message/$', 'index', name="milestone_index"),
)

# task views
urlpatterns += patterns('projects.views.task',
    url(r'(?P<project_id>\d+)/task/save/$', 'save', name='task_add'),
    url(r'(?P<project_id>\d+)/task/save/(?P<task_id>[0-9]+)/$', 'save', name='task_edit'),
    url(r'(?P<project_id>\d+)/task/delete/(?P<task_id>[0-9]+)/$', 'delete', name='task_delete'),
    url(r'(?P<project_id>\d+)/task/(?P<task_id>[0-9]+)/$', 'detail', name='task_detail'),
    url(r'(?P<project_id>\d+)/task/$', 'index', name="task_index"),
)

# task ajax views
urlpatterns += patterns('projects.views.task_ajax',
    url(r'(?P<project_id>\d+)/task/ajax/add_task/$', 'add_task', name="task_ajax_add"),
    url(r'(?P<project_id>\d+)/task/ajax/remove_task/$', 'remove_task', name="task_ajax_remove"),
    url(r'(?P<project_id>\d+)/task/ajax/complete/(?P<task_id>\d+)/$', 'complete_task', name="task_ajax_complete"),
)

# time views
urlpatterns += patterns('projects.views.time',
    url(r'(?P<project_id>\d+)/time/save/$', 'save', name='time_add'),
    url(r'(?P<project_id>\d+)/time/save/(?P<time_id>[0-9]+)/$', 'save', name='time_edit'),
    url(r'(?P<project_id>\d+)/time/delete/(?P<time_id>[0-9]+)/$', 'delete', name='time_delete'),
    url(r'(?P<project_id>\d+)/time/$', 'index', name="time_index"),
)

# issue views
urlpatterns += patterns('projects.views.issue',
    url(r'(?P<project_id>\d+)/issue/save/$', 'save', name='issue_add'),
    url(r'(?P<project_id>\d+)/issue/save/(?P<issue_id>[0-9]+)/$', 'save', name='issue_edit'),
    url(r'(?P<project_id>\d+)/issue/delete/(?P<issue_id>[0-9]+)/$', 'delete', name='issue_delete'),
    url(r'(?P<project_id>\d+)/issue/$', 'index', name="issue_index"),
)

# project views
#urlpatterns += patterns('projects.views.project',
    #url(r'(?P<project_id>\d+)/$', 'dashboard', name="project_dashboard"),
    #url(r'(?P<project_id>\d+)/settings/$', 'settings', name="project_settings"),
    #url(r'$', 'index', name="project_index"),
#)

urlpatterns += patterns('django_vcs.views',
    url('^(?P<project_id>\d+)/browser/$', 'repo_list', name='repo_list'),
    url('^(?P<project_id>\d+)/browser/(?P<slug>[\w-]+)/$', 'recent_commits', name='recent_commits'),
    url('^(?P<project_id>\d+)/browser/(?P<slug>[\w-]+)/browser/(?P<path>.*)$', 'code_browser', name='code_browser'),
    url('^(?P<project_id>\d+)/browser/(?P<slug>[\w-]+)/commit/(?P<commit_id>.*)/$', 'commit_detail', name='commit_detail'),
)

urlpatterns += patterns('projects.views.project',
    url(r'(?P<project_id>\d+)/dashboard/$', 'dashboard', name="project_dashboard"),
    url(r'(?P<project_id>\d+)/people/$', 'people', name="project_people"),
    url(r'(?P<project_id>\d+)/people/change/(?P<member_id>\d+)/$', 'membership_change', name="membership_change"),
    url(r'(?P<project_id>\d+)/people/add/$', 'membership_add', name="membership_add"),
    url(r'(?P<project_id>\d+)/settings/$', 'settings', name="project_settings"),
    url(r'add/$', 'add', name="project_add"),
    url(r'$', 'index', name="project_index"),
)


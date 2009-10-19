# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from newsletter.models import Newsletter, Subscriber, Group, Submission
from newsletter.forms import NewsletterForm, SubscriberForm,GroupForm
from django.views.generic import list_detail, date_based
from django.views.generic.simple import direct_to_template
from django.views.generic.create_update import create_object,update_object,delete_object
from django.contrib.auth.decorators import login_required, permission_required

#Subscribers dict's
subscriber_create_dict = {
    'form_class': SubscriberForm,
    'template_name': 'newsletter/subscriber_add.html',
    'post_save_redirect': '/newsletter/subscriber/list/',
}
subscriber_update_dict = {
    'form_class': SubscriberForm,
    'template_name': 'newsletter/subscriber_edit.html',
    'post_save_redirect': '/newsletter/subscriber/list/',
}
subscriber_delete_dict = {
    'model': Subscriber,
    'template_name': 'newsletter/subscriber_delete.html',
    'post_delete_redirect':'/newsletter/subscriber/list/',
}
subscriber_list_dict = {
    'queryset': Subscriber.objects.all(),
    #'date_field': 'created',
    'template_name': 'newsletter/subscriber_list.html',
    #'template_object_name' : "subscriber", # default is object_list
}
subscriber_by_group_list_dict = {
    'queryset': Subscriber.objects.all(),
    #'date_field': 'created',
    'template_name': 'newsletter/subscriber_by_group.html',
    #'template_object_name' : "subscriber", # default is object_list
    'extra_context': {'group_list' : Group.objects.all}
}


#Group Dict's
group_create_dict = {
    'form_class': GroupForm,
    'template_name': 'newsletter/group_add.html',
    'post_save_redirect':'/newsletter/group/list/',
}
group_update_dict = {
    'form_class': GroupForm,
    'template_name': 'newsletter/group_edit.html',
    'post_save_redirect':'/newsletter/group/list/',
}
group_delete_dict = {
    'model': Group,
    'template_name': 'newsletter/group_delete.html',
    'post_delete_redirect':'/newsletter/group/list/',
}
group_list_dict = {
    'queryset':Group.objects.all(),
    'template_name': 'newsletter/group_list.html',
    #'template_object_name' : "group", # default is object_list
}

#Newsletter
newsletter_delete_dict = {
    'model':Newsletter,
    'template_name': 'newsletter/newsletter_delete.html',
    'post_delete_redirect':'/newsletter/list/',
}

#Dashboard
#dashboard_dict = {
    #'template': 'newsletter/dashboard.html',
    #}
dashboard_dict = {
    'queryset':Submission.objects.all(),
    'date_field': 'sent_date',
    'num_latest':3,
    'template_name': 'newsletter/dashboard.html',
    }

urlpatterns = patterns('newsletter.views',

    #Newsletters
    url(r'^add/$', 'newsletter_add', name='newsletter_add'),
    url(r'^list/$','index', name='newsletter_list'),
    url(r'^edit/(?P<newsletter_id>\w+)/$', 'newsletter_edit', name='newsletter_edit'),
    url(r'^delete/(?P<object_id>\w+)/$', login_required(delete_object), newsletter_delete_dict, name='newsletter_delete'),
    url(r'^content/(?P<newsletter_id>\w+)/$', 'newsletter_content', name = 'newsletter_content'),
    url(r'^analytics/(?P<newsletter_id>\w+)/$', 'newsletter_analytics', name = 'newsletter_analytics'),
    url(r'^edit/links/(?P<object_id>\w+)/$', 'manage_links', name='newsletter_links'),
    url(r'^send/(?P<object_id>\d+)/$','newsletter_send', name='newsletter_send'),

    #Ajax Call's
    url(r'^get_links/$', 'links_ajax', name = 'links_ajax'),
    url(r'^get_dashboard/$', 'dashboard_ajax', name = 'dashboard_ajax'),

    #Subscribers
    url(r'^subscriber/add/$', login_required(create_object), subscriber_create_dict, name='subscriber_create'),
    url(r'^subscriber/list/$', login_required(list_detail.object_list), subscriber_list_dict, name='subscriber_list'),
    url(r'^subscriber/update/(?P<object_id>\d+)/$', login_required(update_object), subscriber_update_dict, name='subscriber_update'),
    url(r'^subscriber/delete/(?P<object_id>\d+)/$', login_required(delete_object), subscriber_delete_dict, name='subscriber_delete'),
    url(r'^subscriber/by-group/$', login_required(list_detail.object_list), subscriber_by_group_list_dict, name='subscriber_by_group_list'), # with a generic view in view.py
    url(r'^subscriber/by-group/(?P<object_id>\d+)/$', 'subscriber_by_group', name='subscriber_by_group'), # with a generic view in view.py

    #Groups
    url(r'^group/add/$', login_required(create_object), group_create_dict, name='group_create'),
    url(r'^group/list/$', login_required(list_detail.object_list), group_list_dict, name='group_list'),
    url(r'^group/update/(?P<object_id>\d+)/$', login_required(update_object), group_update_dict, name='group_update'),
    url(r'^group/delete/(?P<object_id>\d+)/$', login_required(delete_object), group_delete_dict, name='group_delete'),

    #Extra
    url(r'^news/(?P<link_hash>\w+)/$', 'link_count', name='link_count'),
    url(r'^host', 'host', name='host'),

    #testing
    url(r'^display_meta/$', 'display_meta', name='display_meta'),

    #Dashboard
    url(r'^dashboard',login_required(date_based.archive_index), dashboard_dict, name='dashboard'),
    
    #Index
    #url(r'^$', 'index', name="newsletter_index"),
    url(r'^$',login_required(date_based.archive_index), dashboard_dict, name="newsletter_index"),
)
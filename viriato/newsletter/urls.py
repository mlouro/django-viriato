# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from newsletter.models import Newsletter, Subscriber, Group
from newsletter.forms import NewsletterForm, SubscriberForm,GroupForm
from django.views.generic import list_detail, date_based
from django.views.generic.simple import direct_to_template
from django.views.generic.create_update import create_object,update_object,delete_object

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



urlpatterns = patterns('newsletter.views',

    #Dashboard
    url(r'^dashboard','index', name='dashboard'),

    #Newsletters
    url(r'^add/$', 'newsletter_add', name='newsletter_add'),
    url(r'^list/$','index', name='newsletter_list'),
    url(r'^edit/(?P<newsletter_id>\w+)/$', 'newsletter_edit', name='newsletter_edit'),
    url(r'^delete/(?P<object_id>\w+)/$', delete_object, newsletter_delete_dict, name='newsletter_delete'),
    url(r'^content/(?P<newsletter_id>\w+)/$', 'newsletter_content', name = 'newsletter_content'),
    url(r'^analytics/(?P<newsletter_id>\w+)/$', 'newsletter_analytics', name = 'newsletter_analytics'),
    #created by Emanuel
    url(r'^get_links/$', 'links_ajax', name = 'links_ajax'),

    #Testing Links
    url(r'^links/(?P<object_id>\w+)/$', 'manage_links', name='manage_links'),

    #Subscribers
    url(r'^subscriber/add/$', create_object, subscriber_create_dict, name='subscriber_create'),
    url(r'^subscriber/list/$', list_detail.object_list, subscriber_list_dict, name='subscriber_list'),
    url(r'^subscriber/update/(?P<object_id>\d+)/$', update_object, subscriber_update_dict, name='subscriber_update'),
    url(r'^subscriber/delete/(?P<object_id>\d+)/$', delete_object, subscriber_delete_dict, name='subscriber_delete'),
    url(r'^subscriber/by-group/$', list_detail.object_list, subscriber_by_group_list_dict, name='subscriber_by_group_list'), # with a generic view in view.py
    url(r'^subscriber/by-group/(?P<object_id>\d+)/$', 'subscriber_by_group', name='subscriber_by_group'), # with a generic view in view.py

    #Groups
    url(r'^group/add/$', create_object, group_create_dict, name='group_create'),
    url(r'^group/list/$', list_detail.object_list, group_list_dict, name='group_list'),
    url(r'^group/update/(?P<object_id>\d+)/$', update_object, group_update_dict, name='group_update'),
    url(r'^group/delete/(?P<object_id>\d+)/$', delete_object, group_delete_dict, name='group_delete'),

    #Extra
    url(r'^news/(?P<link_hash>\w+)/$', 'link_count', name='link_count'),
    url(r'^host', 'host', name='host'),

    #testing
    url(r'^send/(?P<object_id>\d+)/$','newsletter_send', name='newsletter_send'),
    url(r'^display_meta/$', 'display_meta', name='display_meta'),

    #Index
    url(r'^$', 'index'),
)
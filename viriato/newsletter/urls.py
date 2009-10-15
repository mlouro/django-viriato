# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from newsletter.models import Subscriber, Group
from newsletter.forms import NewsletterForm, SubscriberForm,GroupForm
from django.views.generic import list_detail, date_based
from django.views.generic.simple import direct_to_template
from django.views.generic.create_update import create_object,update_object,delete_object

"""Subscribers dict's"""
subscriber_create_dict = {
    'form_class': SubscriberForm,
    'post_save_redirect': '/newsletter/subscriber-list/',
    }
subscriber_list_dict = {
    'queryset': Subscriber.objects.all(),
    #'date_field': 'created',
    'template_name': 'newsletter/subscriber_list.html',
    #'template_object_name' : "subscriber", # default object
    'extra_context' : {"group_list" : Group.objects.all()},
}


"""Group Dict's"""
group_create_dict = {
    'form_class': GroupForm,
    'post_save_redirect':'/newsletter/subscriber-list/',
    }
group_list_dict = {
    'queryset':Group.objects.all(),
    'template_name': 'newsletter/group_list.html',
    }


urlpatterns = patterns('newsletter.views',
    #Working
    (r'^$', 'index'),

    (r'^add-newsletter/$', 'add_newsletter'),
    (r'^newsletter-edit/(?P<newsletter_id>\w+)/$', 'newsletter_edit'),
    (r'^newsletter-content/(?P<newsletter_id>\w+)/$', 'newsletter_content'),

    (r'^subscriber-create/$', create_object, subscriber_create_dict),
    (r'^subscriber-list/$', list_detail.object_list, subscriber_list_dict),
    (r'^subscriber-update/(?P<object_id>\d+)/$', update_object, subscriber_create_dict),
    (r'^subscriber-delete/(?P<object_id>\d+)/$', delete_object, subscriber_create_dict),
    (r'^subscribers-by-group/(?P<object_id>\d+)/$', 'subscribers_by_group'), # with a generic view in view.py

    (r'^group-create/$', create_object, group_create_dict),
    (r'^group-list/$', list_detail.object_list, group_list_dict),

    (r'^news/(?P<link_hash>\w+)/$', 'link_count'),
    (r'^host', 'host'),
    #testing
    (r'^send-newsletter/$','send_newsletter'),
    (r'^display_meta/$', 'display_meta'),
)
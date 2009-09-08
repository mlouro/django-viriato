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
    
    #Newsletters
    url(r'^$', 'index', name='newsletter_list'),
    url(r'^add-newsletter/$', 'add_newsletter', name='newsletter_add'),
    url(r'^newsletter-edit/(?P<newsletter_id>\w+)/$', 'newsletter_edit', name='newsletter_edit'),
    url(r'^newsletter-content/(?P<newsletter_id>\w+)/$', 'newsletter_content', name = 'newsletter_content'),
    
    #Subscribers
    url(r'^subscriber-create/$', create_object, subscriber_create_dict, name='subscriber_create'),
    url(r'^subscriber-list/$', list_detail.object_list, subscriber_list_dict, name='subscriber_list'),
    url(r'^subscriber-update/(?P<object_id>\d+)/$', update_object, subscriber_create_dict, name='subscriber_update'),
    url(r'^subscriber-delete/(?P<object_id>\d+)/$', delete_object, subscriber_create_dict, name='subscriber_delete'),
    url(r'^subscribers-by-group/(?P<object_id>\d+)/$', 'subscribers_by_group', name='subscriber_by_group'), # with a generic view in view.py
    
    #Groups
    url(r'^group-create/$', create_object, group_create_dict, name='group_create'),
    url(r'^group-list/$', list_detail.object_list, group_list_dict, name='group_list'),
    
    #Extra
    url(r'^news/(?P<link_hash>\w+)/$', 'link_count', name='link_count'),
    url(r'^host', 'host', name='host'),
    #testing
    url(r'^newsletter-send/(?P<object_id>\d+)/$','newsletter_send', name='newsletter_send'),
    url(r'^display_meta/$', 'display_meta', name='display_meta'),
)
# -*- coding: utf-8 -*-
from django.forms import forms, ModelForm
from newsletter.models import Subscriber,Group,Newsletter

class NewsletterForm(ModelForm):
    class Meta:
        model = Newsletter
        exclude = ('view_count')

class SubscriberForm(ModelForm):
    class Meta:
        model = Subscriber


class GroupForm(ModelForm):
    class Meta:
        model = Group

# -*- coding: utf-8 -*-
from django.forms import forms, ModelForm
from django.forms.models import inlineformset_factory
from newsletter.models import Subscriber,Group,Newsletter,Link
from django import forms

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

class LinkForm(ModelForm):
    class Meta:
        model = Link
        fields = ('link','slug')

LinkFormset = inlineformset_factory(Newsletter,Link,extra=0)

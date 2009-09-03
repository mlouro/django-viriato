# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from contact.models import Website, Address, Email, Phone, InstantMessaging
from django import forms    


class MyCompany(models.Model):
    title = models.CharField(max_length=200)
    legal_name = models.CharField(blank=True, max_length=200)
    nif = models.CharField(blank=True, max_length=200)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    retention = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    bill_name = models.CharField(blank=True, max_length=30)
    addresses = generic.GenericRelation(Address)
    emails = generic.GenericRelation(Email)
    phones = generic.GenericRelation(Phone)
    websites = generic.GenericRelation(Website)
    InstantMessagings = generic.GenericRelation(InstantMessaging)
    photo = models.ImageField(blank=True, upload_to="fotos")
    info = models.TextField(blank=True,)
    
    def __unicode__(self):
        return self.title

# -*- coding: utf-8 -*-
from django.db import models


CONTACT_TYPE_CHOICES = (
    ('WK', 'Work'),
    ('PS', 'Personal'),
    ('OT', 'Other'),
)

ADDRESS_TYPE_CHOICES = (
    ('WK', 'Work'),
    ('HM', 'Home'),
    ('OT', 'Other'),
)

PHONE_TYPE_CHOICES = (
    ('HM', 'Work'),
    ('WK', 'Mobile'),
    ('FX', 'Fax'),
    ('PG', 'Pager'),
    ('HM', 'Home'),
    ('PS', 'Personal'),
    ('SK', 'Skype'),
    ('OT', 'Other'),
)


class MyCompany(models.Model):
    title = models.CharField(max_length=200)
    legal_name = models.CharField(blank=True, max_length=200)
    nif = models.CharField(blank=True, max_length=200)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    retention = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    photo = models.ImageField(blank=True, upload_to="fotos")
    info = models.TextField(blank=True,)

    def __unicode__(self):
        return self.title


class EmailHostSettings(models.Model):
    company = models.ForeignKey(MyCompany)
    host = models.EmailField()
    pwd = models.CharField(max_length=30)
    from_user = models.EmailField()
    server = models.URLField()
    #host, pwd, from_user, server

class ContactTypes(models.Model):
    description = models.CharField(max_length=20,)

    def __unicode__(self):
        return self.description


class Email(models.Model):
    address = models.EmailField(blank=True, max_length=200)
    contact_type = models.ForeignKey(ContactTypes)
    company = models.ForeignKey(MyCompany)

    def __unicode__(self):
        return address


class Address(models.Model):
    street = models.CharField(blank=True, max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(blank=True, max_length=200)
    zipcode = models.CharField(blank=True, max_length=200)
    country = models.CharField(blank=True, max_length=200)
    contact_type = models.ForeignKey(ContactTypes)
    company = models.ForeignKey(MyCompany)

    def __unicode__(self):
        return '%s, %s - %s | %s' % (self.street, self.zipcode, self.state, self.country)

class Phone(models.Model):
    number = models.CharField(blank=True, max_length=200)
    contact_type = models.ForeignKey(ContactTypes)
    company = models.ForeignKey(MyCompany)

    def __unicode__(self):
        return self.number


class Website(models.Model):
    url = models.CharField(blank=True, max_length=200)
    contact_type = models.ForeignKey(ContactTypes)
    company = models.ForeignKey(MyCompany)

    def __unicode__(self):
        return self.url


class InstantMessaging(models.Model):
    im = models.EmailField(max_length=20)
    contact_type = models.ForeignKey(ContactTypes)
    company = models.ForeignKey(MyCompany)

    def __unicode__(self):
        return self.im

# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from project import Project
from milestone import Milestone

# Issue Type
# (bug, feature, none, etc...)
class Type(models.Model):
    title    = models.CharField(max_length=200)

    class Meta:
        app_label = 'project'

    def __unicode__(self):
        return self.title

# Issue Status
# (completed, pending, none, etc...)
class Status(models.Model):
    title    = models.CharField(max_length=200)

    class Meta:
        app_label = 'projects'

    def __unicode__(self):
        return self.title

# Issue Priority
# (high, regular, low, very low, none. etc...)
class Priority(models.Model):
    title    = models.CharField(max_length=200)
    value    = models.IntegerField()

    class Meta:
        app_label = 'projects'

    def __unicode__(self):
        return self.title

# Issue
class Issue(models.Model):
    title     = models.CharField(max_length=200)
    summary   = models.TextField()
    project   = models.ForeignKey(Project)
    type      = models.ForeignKey(Type)
    status    = models.ForeignKey(Status)
    priority  = models.ForeignKey(Priority, blank=True, )
    milestone = models.ForeignKey(Milestone, blank=True, )
    owner     = models.ForeignKey(User)
    private   = models.BooleanField()

    created = models.DateTimeField(blank=False, auto_now_add=True)
    modified = models.DateTimeField(blank=False, auto_now=True)

    class Meta:
        app_label = 'projects'
        permissions = (
            ("view_issue", "Can view issues"),
        )

    def __unicode__(self):
        return self.nome


# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from project import Project
from milestone import Milestone
from task import Task


# Issue Type
# (bug, feature, none, etc...)
class IssueCategory(models.Model):
    title    = models.CharField(max_length=200)

    class Meta:
        app_label = 'projects'

    def __unicode__(self):
        return self.title

# Issue Status
# (completed, pending, none, etc...)
class IssueStatus(models.Model):
    title    = models.CharField(max_length=200)

    class Meta:
        app_label = 'projects'

    def __unicode__(self):
        return self.title

# Issue Priority
# (high, regular, low, very low, none. etc...)
class IssuePriority(models.Model):
    title    = models.CharField(max_length=200)
    value    = models.IntegerField()

    class Meta:
        app_label = 'projects'

    def __unicode__(self):
        return self.title


# Issue
class Issue(models.Model):
    title     = models.CharField(max_length=200)
    summary   = models.TextField(blank=True)
    project   = models.ForeignKey(Project)
    category  = models.ForeignKey(IssueCategory)
    status    = models.ForeignKey(IssueStatus)
    priority  = models.ForeignKey(IssuePriority)
    milestone = models.ForeignKey(Milestone, blank=True, null=True)
    task      = models.ForeignKey(Task, blank=True, null=True)
    owner     = models.ForeignKey(User, blank=True, null=True)
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


class IssueChange(models.Model):
    issue   = models.ForeignKey(Issue, related_name="changes")
    user    = models.ForeignKey(User)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'projects'

    def __unicode__(self):
        return self.title


class IssueChangeItem(models.Model):
    issue_change  = models.ForeignKey(IssueChange, related_name="changes")
    option        = models.CharField(max_length=200)
    inital_value  = models.CharField(blank=True, max_length=200)
    change_value  = models.CharField(blank=True, max_length=200)

    class Meta:
        app_label = 'projects'

    def __unicode__(self):
        if self.inital_value and self.change_value:
            return '%s changed from %s to %s' % (self.option, self.inital_value or None, self.change_value or None)
        return 'changed %s' % (self.option)





# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User, Group



class Project(models.Model):
    name        = models.CharField(max_length=200)
    summary     = models.CharField(_('Description'), blank=True, max_length=200)

    users       = models.ManyToManyField(User, through='Membership', blank=True)

    created = models.DateTimeField(blank=False, auto_now_add=True)
    modified = models.DateTimeField(blank=False, auto_now=True)

    class Meta:
        app_label = 'projects'
        permissions = (
            ("view_project", "Can view projects"),
        )

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('projects.views.project.dashboard', [str(self.id)])


class Role(models.Model):
    """
    Lists system wide roles that can exist on projects.
    Roles map to one single group in the Auth.Group model
    the group is checked and enabled to the user on runtime
    when he checks a specific project
    """
    name        = models.CharField(max_length=200)
    summary     = models.CharField(_('Summary'), max_length=200, blank=True)
    group       = models.ForeignKey(Group)

    class Meta:
        app_label = 'projects'

    def __unicode__(self):
        return self.name


class Membership(models.Model):
    """
    ManyToMany table for Project <-> User relation
    """
    user    = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    role    = models.ForeignKey(Role, blank=True, null=True)

    created = models.DateTimeField(blank=False, auto_now_add=True)
    modified = models.DateTimeField(blank=False, auto_now=True)

    class Meta:
        app_label = 'projects'
        permissions = (
            ("manage_membership", "Can manage project memberships"),
        )

    def __unicode__(self):
        return "%s" % self.user
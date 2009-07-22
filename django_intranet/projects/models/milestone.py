# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from project import Project
from django.contrib.auth.models import User
from django.forms import ModelForm
from datetime import datetime

# Milestone
class Milestone(models.Model):
    title        = models.CharField(max_length=200)
    end_date     = models.DateTimeField()
    project      = models.ForeignKey(Project)
    completed    = models.BooleanField()

    created = models.DateTimeField(blank=False, auto_now_add=True)
    modified = models.DateTimeField(blank=False, auto_now=True)

    class Meta:
        app_label = 'projects'
        permissions = (
            ("view_milestone", "Can view milestones"),
        )


    def __unicode__(self):
        return self.title

    def get_parent_tasks(self):
        return self.task_set.filter(parent=None).select_related()
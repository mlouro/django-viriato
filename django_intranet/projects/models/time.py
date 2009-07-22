# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import User
from projects.models.project import Project
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import re

class Time(models.Model):
    date        = models.DateField()
    person      = models.ForeignKey(User)
    time        = models.FloatField()
    description = models.CharField(_('Description'), max_length=255)
    billable    = models.BooleanField(blank=True)

    project     = models.ForeignKey(Project)

    created     = models.DateTimeField(blank=False, auto_now_add=True)
    modified    = models.DateTimeField(blank=False, auto_now=True)

    content_type    = models.ForeignKey(ContentType, blank=True, null=True)
    object_id       = models.PositiveIntegerField(blank=True, null=True)
    content_object  = generic.GenericForeignKey('content_type', 'object_id')



    class Meta:
        app_label = 'projects'
        permissions = (
            ("view_time", "Can view time"),
        )


    def save(self, force_insert=False, force_update=False):
        # convert 10:30 to 10,5
        if self.time:
            try:
                time = float(self.time)
            except ValueError:
                m = re.search("^(\d{0,}):(\d{0,})$",self.time)
                if m:
                    hours   = float(m.group(1))
                    minutes = float(m.group(2)) / 60
                    self.time = hours + round(minutes,2)

        super(Time, self).save(force_insert, force_update)
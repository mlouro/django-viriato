# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class Comment(models.Model):
    comment = models.TextField()
    created = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    def __unicode__(self):
        return self.comment


class File(models.Model):
    file = models.FileField(upload_to="uploads/files/")
    created = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()

    def __unicode__(self):
        return self.user
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from datetime import datetime
from project import Project
from django_generic.models import Comment, File

class Message(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User,related_name="user")
    project = models.ForeignKey(Project)
    private   = models.BooleanField()

    comments = generic.GenericRelation(Comment)

    created = models.DateTimeField(blank=False, auto_now_add=True)
    modified = models.DateTimeField(blank=False, auto_now=True)


    class Meta:
        app_label = 'projects'
        permissions = (
            ("view_message", "Can view messages"),
        )

    def __unicode__(self):
        return self.title

    def get_comment_count(self):
        return self.comments.count()

    @models.permalink
    def get_absolute_url(self):
        return ('message_details', [str(self.project.id), str(self.id)])
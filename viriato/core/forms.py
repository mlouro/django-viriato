# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Comment, File

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ('user','created','content_type','object_id')

class FileForm(ModelForm):
    class Meta:
        model = File
        exclude = ('user','created','content_type','object_id')
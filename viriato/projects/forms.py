# -*- coding: utf-8 -*-
from django import forms
from models.message import Message
from models.milestone import Milestone
from models.project import Project, Membership
from models.task import Task
from models.time import Time


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ('project','user')


class MilestoneForm(forms.ModelForm):
    class Meta:
        model = Milestone
        exclude = ('project')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project


class MembershipForm(forms.ModelForm):
    class Meta:
        model = Membership
        exclude = ('project', )

class TaskForm(forms.ModelForm):

    estimated_duration = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):

        if kwargs.has_key('project'):
            super(TaskForm, self).__init__(*args)
            self.fields['milestone'].queryset = Milestone.objects.filter(completed=False, project=kwargs['project'])
        else:
            super(TaskForm, self).__init__(*args,**kwargs)

    class Meta:
        model = Task
        exclude = ('assignor','project','parent')


class TimeForm(forms.ModelForm):
    time = forms.CharField(required=False)

    class Meta:
        model = Time
        exclude = ('project','content_type','object_id')
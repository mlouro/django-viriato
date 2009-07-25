# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from projects.models.project import Project
from projects.models.message import Message
from projects.forms import MessageForm
from datetime import datetime
# decorators
from django.contrib.auth.decorators import login_required
from projects.decorators import user_in_project
from core.decorators import permission_required_with_403
# shortcuts
from render_project_shortcut import render_project
# generic apps
from core.models import Comment
from core.forms import CommentForm


def index(request,project_id):
    t = 'projects/message/index.html'
    response_vars = { }

    project = Project.objects.get(id=project_id)

    response_vars['project']    = project
    response_vars['messages']   = Message.objects.filter(project=project)

    return render_project(request, project_id, t, response_vars)


def details(request, project_id, message_id):
    t = 'projects/message/details.html'
    response_vars = { }

    project = Project.objects.get(id=project_id)
    message = Message.objects.get(id=message_id)

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            message.comments.create(comment = comment_form.cleaned_data["comment"], user=request.user)
            return HttpResponseRedirect(reverse('projects.views.message.details', args=[unicode(project.id), message_id]))
    else:
        comment_form = CommentForm()

    response_vars['message'] = message
    response_vars['comment_form'] = comment_form
    response_vars['comments'] = message.comments.all().order_by("-created")

    return render_project(request, project_id, t, response_vars)

def save(request, project_id, message_id=False):
    t = 'projects/message/form.html'
    response_vars = { }

    project = Project.objects.get(id=project_id)

    if message_id:
        message = Message.objects.get(id=message_id)
        form = MessageForm(instance=message)
    else:
        message = Message()
        form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)

        if form.is_valid() and message_id:
            message = Message.objects.get(id=message_id)
            tmp_message = form.save(commit=False)

            message.title = tmp_message.title
            message.start_date = tmp_message.start_date
            message.end_date = tmp_message.end_date
            message.completed = tmp_message.completed

            message.save()

            return HttpResponseRedirect(reverse('projects.views.message.index', args=[project.id]))

        elif form.is_valid():
            message = form.save(commit=False)
            message.project = project
            message.user = request.user
            if message_id:
                message.id = message_id
            message.save()

            return HttpResponseRedirect(reverse('projects.views.message.index', args=[project.id]))

    response_vars['form']         = form
    response_vars['message']      = message
    response_vars['project']      = project

    return render_project(request, project_id, t, response_vars)


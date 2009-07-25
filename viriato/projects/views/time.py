# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from projects.models.project import Project
from projects.models.task import Task
from projects.models.time import Time
from projects.forms import TimeForm
from datetime import datetime
from django.db.models import Sum
# decorators
from django.contrib.auth.decorators import login_required
from projects.decorators import user_in_project
from core.decorators import permission_required_with_403
# shortcuts
from render_project_shortcut import render_project

import re


def index(request, project_id):
    t = 'projects/time/index.html'
    response_vars = { }

    project     = Project.objects.get(id=project_id)
    time_list   = Time.objects.filter(project=project)

    if request.method == 'POST':

        form = TimeForm(request.POST)

        if form.is_valid():
            time = form.save(commit=False)
            time.project_id = project_id
            time.save()

    else:
        time = Time()
        time.person = request.user
        time.date = datetime.now().date
        form = TimeForm(instance=time)




    response_vars['project'] = project
    response_vars['form'] = form
    response_vars['time_list'] = time_list

    response_vars['total_time'] = time_list.aggregate(Sum('time'))

    return render_project(request, project_id, t, response_vars)



@login_required
@permission_required_with_403("projects.add_time")
@user_in_project
def save(request, project_id, time_id=False):
    """
    Shows latest activity and other usefull info
    """
    t = 'projects/time/form.html'
    response_vars = {}
    project = Project.objects.get(id=project_id)

    task = None

    if time_id:
        time = Time.objects.get(id=time_id)
        form = TimeForm(instance=time)
        parent = time.parent
    else:
        time = Time()
        form = TimeForm()

    if request.POST.has_key('task_id') and request.POST['task_id']:
        task = Task.objects.get(id=request.POST['task_id'])
    else:
        if request.GET.has_key('task') and request.GET['task']:
            task = Task.objects.get(id=request.GET['task'])


    if request.method == 'POST':

        form = TimeForm(request.POST)

        if form.is_valid():
            if time_id:
                form = TimeForm(request.POST, instance=Time.objects.get(id=time_id))
                time = form.save(commit=False)
            else:
                time = form.save(commit=False)
                time.project = project

            time.content_object  = task
            time.person = request.user
            time.save()

            if task:
                return HttpResponseRedirect(reverse('task_detail', args=[project.id, task.id]))

            return HttpResponseRedirect(reverse('projects.views.time.index', args=[project.id]))


    response = { }
    response_vars['request']      = request
    response_vars['project']      = project
    response_vars['form']         = form
    response_vars['time']         = time
    response_vars['task']         = task

    return render_project(request, project_id, t, response_vars)





def delete(request, project_id):
    t = 'projects/time/delete.html'
    response_vars = { }

    return render_project(request, project_id, t, response_vars)
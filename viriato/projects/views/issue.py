# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from projects.models.project import Project
from projects.models.task import Task
from projects.models.issue import Issue
from projects.forms import IssueForm
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
    t = 'projects/issue/index.html'
    response_vars = { }

    project     = Project.objects.get(id=project_id)
    issue_list   = Issue.objects.filter(project=project)

    response_vars['project'] = project
    response_vars['issue_list'] = issue_list

    return render_project(request, project_id, t, response_vars)



@login_required
@permission_required_with_403("projects.add_issue")
@user_in_project
def save(request, project_id, issue_id=False):
    """
    Shows latest activity and other usefull info
    """
    t = 'projects/issue/form.html'
    response_vars = {}
    project = Project.objects.get(id=project_id)

    task = None

    if issue_id:
        issue = Issue.objects.get(id=issue_id)
        form = IssueForm(instance=issue)
        parent = issue.parent
    else:
        issue = Issue()
        form = IssueForm()

    if request.POST.has_key('task_id') and request.POST['task_id']:
        task = Task.objects.get(id=request.POST['task_id'])
    else:
        if request.GET.has_key('task') and request.GET['task']:
            task = Task.objects.get(id=request.GET['task'])


    if request.method == 'POST':

        form = IssueForm(request.POST)

        if form.is_valid():
            if issue_id:
                form = IssueForm(request.POST, instance=Issue.objects.get(id=issue_id))
                issue = form.save(commit=False)
            else:
                issue = form.save(commit=False)
                issue.project = project

            issue.content_object  = task
            issue.person = request.user
            issue.save()

            if task:
                return HttpResponseRedirect(reverse('task_detail', args=[project.id, task.id]))

            return HttpResponseRedirect(reverse('projects.views.issue.index', args=[project.id]))


    response = { }
    response_vars['request']      = request
    response_vars['project']      = project
    response_vars['form']         = form
    response_vars['issue']         = issue
    response_vars['task']         = task

    return render_project(request, project_id, t, response_vars)





def delete(request, project_id):
    t = 'projects/issue/delete.html'
    response_vars = { }

    return render_project(request, project_id, t, response_vars)
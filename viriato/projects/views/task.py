# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from projects.models.milestone import Milestone
from projects.models.task import Task
from projects.forms import TaskForm
from projects.models.project import Project
from datetime import datetime
# decorators
from django.contrib.auth.decorators import login_required
from projects.decorators import user_in_project
from core.decorators import permission_required_with_403
# shortcuts
from render_project_shortcut import render_project



def index(request,project_id):
    t = 'projects/task/index.html'
    response_vars = {}
    project = Project.objects.get(id=project_id)

    milestones = Milestone.objects.filter(completed=False,project=project).order_by('end_date')
    milestone_list = []
    for milestone in milestones:
        if milestone.task_set.all():
            milestone_list.append(milestone)


    response_vars['project']    = Project.objects.get(id=project_id)
    response_vars['milestones'] = milestone_list


    return render_project(request, project_id, t, response_vars)

@login_required
@permission_required_with_403("projects.add_task")
@user_in_project
def detail(request, project_id, task_id):
    """
    Shows latest activity and other usefull info
    """
    t = 'projects/task/detail.html'
    response_vars = {}
    project = Project.objects.get(id=project_id)

    task = get_object_or_404(Task, pk=task_id)

    response_vars['task'] = task

    return render_project(request, project_id, t, response_vars)


@permission_required_with_403("projects.add_task")
def delete(request,project_id,task_id):

    project = Project.objects.get(id=project_id)
    task = Task.objects.get(id=task_id)

    if request.POST.has_key('task_id'):
        task = Task.objects.get(id=request.POST['task_id'])
        task.delete()

        return HttpResponseRedirect(reverse('projects.task.views.index', args=[project.id]))


    response = { }
    response['request']      = request
    response['project']      = project
    response['object']       = task

    return render_to_response('projects/task/delete.html', response,
                             context_instance=RequestContext(request))


@login_required
@permission_required_with_403("projects.add_task")
@user_in_project
def save(request, project_id, task_id=False):
    """
    Shows latest activity and other usefull info
    """
    t = 'projects/task/form.html'
    response_vars = {}
    project = Project.objects.get(id=project_id)

    parent = None
    kwargs = {}
    kwargs['project'] = project

    if task_id:
        task = Task.objects.get(id=task_id)
        form = TaskForm(instance=task)
        parent = task.parent
    else:
        task = Task()
        form = TaskForm(**kwargs)

        if request.GET.has_key('parent') and request.GET['parent']:
            parent = Task.objects.get(id=request.GET['parent'])

    if request.method == 'POST':
        form = TaskForm(request.POST, **kwargs)
        if form.is_valid():
            if task_id:
                form = TaskForm(request.POST, instance=Task.objects.get(id=task_id))
                task = form.save(commit=False)
            else:
                task = form.save(commit=False)
                task.project = project
                task.parent  = parent

            task.assignor = request.user

            task.save()

            return HttpResponseRedirect(reverse('projects.views.task.index', args=[project.id]))


    response = { }
    response_vars['request']      = request
    response_vars['project']      = project
    response_vars['form']         = form
    response_vars['task']         = task
    response_vars['parent']       = parent

    return render_project(request, project_id, t, response_vars)

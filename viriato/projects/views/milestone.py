# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from projects.models.project import Project
from projects.models.milestone import Milestone
from projects.forms import MilestoneForm
from datetime import datetime
# decorators
from django.contrib.auth.decorators import login_required
from projects.decorators import user_in_project
from core.decorators import permission_required_with_403
# shortcuts
from render_project_shortcut import render_project


def index(request,project_id):

    project        = Project.objects.get(id=project_id)
    milestones     = Milestone.objects.filter(project=project).order_by('end_date')
    late_list      = milestones.filter(end_date__lte=datetime.now()).filter(completed=False).select_related()
    upcoming_list  = milestones.filter(end_date__gt=datetime.now()).filter(completed=False).select_related()
    completed_list = milestones.filter(completed=True,project=project_id)


    return render_to_response('projects/milestone/index.html',{
                                    'late_list' : late_list,
                                    'upcoming_list' : upcoming_list,
                                    'completed_list' : completed_list,
                                    'project' : project ,},
                             context_instance=RequestContext(request))


@login_required
@permission_required_with_403("projects.add_milestone")
@user_in_project
def save(request, project_id, milestone_id=False):
    """
    Shows latest activity and other usefull info
    """
    t = 'projects/milestone/form.html'
    response_vars = {}
    project = Project.objects.get(id=project_id)

    if milestone_id:
        milestone = Milestone.objects.get(id=milestone_id)
        form = MilestoneForm(instance=milestone)
    else:
        milestone = Milestone()
        form = MilestoneForm()

    if request.method == 'POST':
        form = MilestoneForm(request.POST)

        if form.is_valid() and milestone_id:
            milestone = Milestone.objects.get(id=milestone_id)
            tmp_milestone = form.save(commit=False)

            milestone.title = tmp_milestone.title
            milestone.end_date = tmp_milestone.end_date
            milestone.completed = tmp_milestone.completed

            milestone.save()

            return HttpResponseRedirect(reverse('projects.views.milestone.index', args=[project.id]))

        elif form.is_valid():
            milestone = form.save(commit=False)
            milestone.project = project
            milestone.user = request.user
            if milestone_id:
                milestone.id = milestone_id
            milestone.save()

            return HttpResponseRedirect(reverse('projects.views.milestone.index', args=[project.id]))

    response_vars['form'] = form
    response_vars['milestone'] = milestone
    response_vars['project'] = project

    return render_project(request, project_id, t, response_vars)
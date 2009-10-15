# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from projects.models.project import Project, Membership, Role
from projects.forms import ProjectForm, MembershipForm
from django.views.generic.create_update import create_object, update_object
from django.views.generic.list_detail import object_list
from django.core.exceptions import ObjectDoesNotExist
from projects.decorators import user_in_project
from django.core.urlresolvers import reverse
# decorators
from django.contrib.auth.decorators import login_required
from projects.decorators import user_in_project
from core.decorators import permission_required_with_403
# shortcuts
from render_project_shortcut import render_project

from projects import models



@login_required
@permission_required_with_403("projects.view_project")
def index(request):
    """
    Lists all projects where user is Member
    """

    if request.user.is_superuser:
        return object_list(request,queryset=Project.objects.all())

    return object_list(request,queryset=request.user.project_set.all())


@login_required
@permission_required_with_403("projects.view_project")
@user_in_project
def dashboard(request,project_id):
    """
    Shows latest activity and other usefull info
    """
    t = 'projects/dashboard.html'
    response_vars = {}

    return render_project(request, project_id, t, response_vars)



@login_required
@permission_required_with_403("projects.add_project")
def add(request):
    """
    Adds a new project
    """
    c = context_instance=RequestContext(request)
    t = 'projects/project/form.html'
    response_vars = {}

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
            member = Membership(project=project, user=request.user)
            member.save()
            return HttpResponseRedirect('/projects/')
    else:
        form = ProjectForm()

    response_vars['form'] = form
    return render_to_response(t,response_vars,c)



@login_required
@permission_required_with_403("projects.add_membership")
@user_in_project
def people(request,project_id):
    """
    Shows latest activity and other usefull info
    """
    t = 'projects/project/people.html'
    response_vars = {}
    project = Project.objects.get(id=project_id)

    response_vars['members'] = Membership.objects.filter(project=project).select_related()
    response_vars['roles']   = Role.objects.all()
    response_vars['project'] = project

    return render_project(request, project_id, t, response_vars)


@login_required
@permission_required_with_403("projects.change_membership")
@user_in_project
def membership_change(request, project_id, member_id=False):
    """
    Shows latest activity and other usefull info
    """
    t = 'projects/project/membership_form.html'
    response_vars = {}
    project = Project.objects.get(id=project_id)
    member = Membership.objects.get(id=member_id)


    if member_id:
        member = Membership.objects.get(id=member_id)
        form = MembershipForm(instance=member)
    else:
        member = Membership()
        form = MembershipForm()

    if request.method == 'POST':
        form = MembershipForm(request.POST)

        if form.is_valid():
            membership = form.save(commit=False)

            print member
            print membership.role

            member.role = membership.role
            member.save()

            return HttpResponseRedirect(reverse('projects.views.project.people', args=[project.id]))

    response_vars['form'] = form
    response_vars['member'] = member
    response_vars['project'] = project

    return render_project(request, project_id, t, response_vars)


@login_required
@permission_required_with_403("projects.add_membership")
@user_in_project
def membership_add(request, project_id, member_id=False):
    """
    Shows latest activity and other usefull info
    """
    t = 'projects/project/membership_form.html'
    response_vars = {}
    project = Project.objects.get(id=project_id)


    if member_id:
        member = Membership.objects.get(id=member_id)
        form = MembershipForm(instance=member)
    else:
        member = Membership()
        form = MembershipForm()

    if request.method == 'POST':
        form = MembershipForm(request.POST)

        if form.is_valid():
            membership = form.save(commit=False)
            membership.project = project
            membership.save()

            return HttpResponseRedirect(reverse('project_people', args=[project.id]))

    response_vars['form'] = form
    response_vars['member'] = member
    response_vars['project'] = project

    return render_project(request, project_id, t, response_vars)



@login_required
@permission_required_with_403("projects.view_project","projects.change_project")
def settings(request,project_id):
    project = Project.objects.get(id=project_id)

    formset = ProjectForm(instance=project)
    if request.method == 'POST':
        formset = ProjectForm(request.POST)
        if formset.is_valid():
            project = formset.save(commit=False)
            project.id = project_id;
            project.save()
            return HttpResponseRedirect('/project/')
        else:
            return render_to_response('projects/settings.html', {
                                            'form'    : formset,
                                            'project' : project })

    else:
        return render_to_response('projects/settings.html', {
                                        'form'    : formset,
                                        'project' : project})
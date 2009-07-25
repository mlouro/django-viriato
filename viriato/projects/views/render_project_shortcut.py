# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from projects.models.project import Project

def render_project(request, project_id, template, response_vars):
    """
    A wrapper around render_to_response that
    adds context_instance and Project instance automaticly
    """
    c = context_instance=RequestContext(request)

    if not "project" in response_vars:
        response_vars['project'] = Project.objects.get(id=project_id)
    return render_to_response(template,response_vars,c)

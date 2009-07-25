# -*- coding: utf-8 -*-
from django.utils.functional import wraps
from projects.models.project import Project, Membership, Role
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template import Context
from django.contrib.auth.models import Group


def user_in_project(view):
    """
    Checks if user exists in project and returns 403 if not
    """
    def wrapper(request, *args, **kwargs):

        try:
            # if user is a superuser, it has access to all projects
            if not request.user.is_superuser:
                #project = request.user.project_set.get(id=kwargs['project_id'])
                membership = Membership.objects.get(user=request.user, project__id=kwargs['project_id'])
                roles = Role.objects.all()
                for role in roles:
                    request.user.groups.remove(role.group)
                if membership.role.group:
                    request.user.groups.add(membership.role.group)

                print request.user.get_group_permissions()
        except ObjectDoesNotExist:
            resp = render_to_response('403.html', context_instance=RequestContext(request))
            resp.status_code = 403
            return resp

        return view(request, *args, **kwargs)

    return wraps(view)(wrapper)
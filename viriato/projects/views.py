# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from decorators import permission_required_with_403

@permission_required_with_403('sites.can_add_site')
def dashboard(request):

    c = context_instance=RequestContext(request)
    return render_to_response('project/dashboard.html',{},c)


@login_required
def trashboard(request,trash):

    c = context_instance=RequestContext(request)
    return render_to_response('project/dashboard.html',{},c)


@login_required
def trashcan(request,trash,can):

    c = context_instance=RequestContext(request)
    return render_to_response('project/dashboard.html',{},c)
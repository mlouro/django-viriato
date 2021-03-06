# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from core.decorators import permission_required_with_403

from projects import models

@login_required
def dashboard(request):

    messages = models.Message.objects.all().count()
    print messages

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
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def home(request):

    c = context_instance=RequestContext(request)
    return render_to_response('home.html',{},c)
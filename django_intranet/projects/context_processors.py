# -*- coding: utf-8 -*-
from projects.models.project import Project
def static_url(request,*args,**kwargs):

    return {'STATIC_URL' : 'hello'}


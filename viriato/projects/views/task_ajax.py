# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from projects.models.task import Task
from django.core import serializers

def add_task(request):
    pass
    #item = Item()

    #item.title        = request.GET['title']
    #item.todo         = Todo.objects.get(id=request.GET['todo'])
    #assigned_username = ''

    #if request.GET['assigned_to']:
        #user = User.objects.get(id=request.GET['assigned_to'])
        #item.assigned_to       = user
        #item.assigned_username = user.username
        #assigned_username      = '- ' + user.username

    #item.save()

    #data = '{ "id" : "' + str(item.id) + '", "title" : "' + item.title + '", "assigned_username" : "'+ assigned_username +'", "assigned_to" : "'+ request.GET['assigned_to'] +'" }';

    return HttpResponse(data, mimetype="application/javascript")

def remove_task(request):
    pass

    #item = Item.objects.get(id=request.POST['id'])
    #item.delete()

    return HttpResponse("{}", mimetype="application/javascript")


def complete_task(request, project_id, task_id):
    task = Task.objects.get(id=task_id)

    return HttpResponse('{ "complete" : "%s" }' % (task.set_complete()), mimetype="application/javascript")


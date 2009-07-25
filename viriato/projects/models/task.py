# -*- coding: utf-8 -*-
from django.db import models
from projects.models.project import Project
from projects.models.time import Time
from milestone import Milestone
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timesince import timesince, timeuntil
from django import utils
from django.utils.translation import ugettext as _
import re
from django.contrib.contenttypes import generic
from django.db.models import Sum


class Task(models.Model):
    name        = models.CharField(_("Name"), max_length=150)
    description = models.TextField(_("Description"), blank=True)
    parent      = models.ForeignKey("self", null=True, blank=True, related_name="children")
    project     = models.ForeignKey(Project)
    milestone   = models.ForeignKey(Milestone)

    owner       = models.ForeignKey(User, related_name="owner", blank=True, null=True)
    assignor    = models.ForeignKey(User, related_name="assignor")

    complete    = models.BooleanField(default=False)
    start_date  = models.DateField(null=True, blank=True)
    end_date    = models.DateField(null=True, blank=True)
    estimated_duration = models.FloatField(null=True, blank=True)

    times = generic.GenericRelation(Time)

    created     = models.DateTimeField(blank=False, auto_now_add=True)
    modified    = models.DateTimeField(blank=False, auto_now=True)


    class Meta:
        app_label = 'projects'
        permissions = (
            ("view_task", "Can view tasks"),
        )


    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('task_detail', (self.project.id, self.id))

    @models.permalink
    def get_delete_url(self):
        return ('task_delete', (self.project.id, self.id))

    @models.permalink
    def get_edit_url(self):
        return ('task_edit', (self.project.id, self.id))

    def get_create_subtask_url(self):
        return "/projects/%s/task/save/?parent=%s" % (self.project.id, self.id)


    def save(self, force_insert=False, force_update=False):

        # convert 10:30 to 10,5
        if self.estimated_duration:
            try:
                estimated_duration = float(self.estimated_duration)
            except ValueError:
                m = re.search("^(\d{0,}):(\d{0,})$",self.estimated_duration)
                if m:
                    hours   = float(m.group(1))
                    minutes = float(m.group(2)) / 60
                    self.estimated_duration = hours + round(minutes,2)
        else:
            self.estimated_duration = 0

        super(Task, self).save(force_insert, force_update)


    def get_estimated_duration(self):
        """
        Returns the estimated duration for the task, or it's children *worker tasks*.
        If tasks are not *worker tasks*, their estimated duration is not considered.
        """
        estimated_duration = 0
        children = self.children.all()

        if self.estimated_duration and not children:
            estimated_duration += self.estimated_duration

        if children:
            for child in children:
                estimated_duration += child.get_estimated_duration()

        return estimated_duration


    def get_current_time(self):
        """
        Returns the logged time for all subtasks
        """
        current_time = 0
        children = self.children.all()

        current_time += self.get_times()
        if children:
            for child in children:
                current_time += child.get_current_time()

        return current_time

    def get_times(self):
        time = 0
        time_sum = self.times.all().aggregate(Sum('time'))
        if time_sum['time__sum']:
            time = time_sum['time__sum']
        return time


    def get_lineage(self):
        current = self
        result = [current]
        while current.parent:
            current = current.parent
            result.append(current)

        return result


    def set_complete(self,completed = None):

        if completed == None:
            self.complete = False if self.complete else True
            if not self.complete:
                self.set_not_complete()
            else:
                for task in self.children.all():
                    task.set_complete(self.complete)
        elif completed == True:
            self.complete = completed
            for task in self.children.all():
                task.set_complete(self.complete)
        else:
            self.complete = completed
            self.set_not_complete()

        self.save()

        return self.complete


    def set_not_complete(self):
        current = self
        while current.parent:
            current.complete = False
            current.save()
            current = current.parent

        current.complete = False
        current.save()

        return None


    def get_children_html(self):

        html = ""
        complete = ""
        children = self.children.all()

        if self.parent is None:
            html = '<ul class="initial-node">'

        if self.complete:
            complete = "complete"

        if self.end_date:
            date_now = datetime.date(datetime.now())
            date_diff = (self.end_date - date_now)

        html += '<li class="task-li"><div class="task-row %s">' % (complete)
        html += '<label for="complete-%s"> ' % (self.id)
        html += '<input type="checkbox" class="task-complete %s" name="complete-%s" /> ' % (complete, self.id)
        if children:
            html += ' <em><a href="%s">%s</a></em></label> ' % (self.get_absolute_url(), self)
        else:
            html += ' <a href="%s">%s</a></label> ' % (self.get_absolute_url(), self)

        if self.end_date and (date_diff.days >= 0):
            html += '<span class="time time_until">%s days</span>' % (abs(date_diff.days))
        elif self.end_date:
            html += '<span class="time time_since">%s days late</span>' % (abs(date_diff.days))

        if self.owner:
            html += '<span class="owner"> @%s</span>' % (self.owner)

        html += '<div class="actions hidden">'
        html += '<a href="%s" class="edit">view</a>, ' % (self.get_absolute_url())
        html += '<a href="%s"' % (self.get_edit_url())
        html += 'class="edit">edit</a>, '
        html += '<a href="%s" class="delete">delete</a>, ' % (self.get_delete_url())
        html += '<a href="%s" class="create subtask">create subtask</a> ' % (self.get_create_subtask_url())
        html += '</div></div>'


        if children:
            html += "<ul>"
            for child in children:
                html += child.get_children_html()
            html += "</ul>"


        html += "</li>"

        if self.parent is None:
            html += "</ul>"

        return html



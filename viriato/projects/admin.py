# -*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from models.issue import IssueCategory, IssuePriority, IssueStatus, Issue
from models.message import Message
from models.task import Task
from models.time import Time
from models.project import Project, Membership, Role
from models.milestone import Milestone

# issues
class IssueCategoryAdmin(admin.ModelAdmin):
    pass

class IssuePriorityAdmin(admin.ModelAdmin):
    pass

class IssueStatusAdmin(admin.ModelAdmin):
    pass


class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'project')
    search_fields = ['title']

# messages
class MessageAdmin(admin.ModelAdmin):
    pass

# tasks
class TaskAdmin(admin.ModelAdmin):
    pass

class TaskInline(admin.TabularInline):
    model = Task

# milestones
class MilestoneAdmin(admin.ModelAdmin):
    inlines = [
        TaskInline,
    ]

class MilestoneInline(admin.TabularInline):
    model = Milestone

# time
class TimeAdmin(admin.ModelAdmin):
    pass

class RoleAdmin(admin.ModelAdmin):
    pass

class MembershipAdmin(admin.ModelAdmin):
    pass

class TimeInline(admin.TabularInline):
    model = Milestone


class MembershipInline(admin.TabularInline):
    model = Membership

# projects
class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
        MilestoneInline,
        TimeInline,
    ]

admin.site.register(Project, ProjectAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Time, TimeAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Milestone, MilestoneAdmin)
admin.site.register(IssueCategory, IssueCategoryAdmin)
admin.site.register(IssuePriority, IssuePriorityAdmin)
admin.site.register(IssueStatus, IssueStatusAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Message, MessageAdmin)


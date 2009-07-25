# -*- coding: utf-8 -*-

import os, sys

ROOT_PATH = os.path.dirname(os.path.realpath(os.path.dirname(__file__)))

PROJECT_PATH, PROJECT_DIR = os.path.split(ROOT_PATH)

sys.path.insert(0, ROOT_PATH)
sys.path.insert(1, PROJECT_PATH)

os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % PROJECT_DIR

from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from projects.models import Role

def setup_permissions():
    project_manager_group, project_manager_group_created = Group.objects.get_or_create(name="project_manager")
    internal_dev_group, internal_dev_created = Group.objects.get_or_create(name="internal_developer")

    if project_manager_group_created:
        project_manager_group.save()

    if internal_dev_created:
        internal_dev_group.save()


    manager_permissions = Permission.objects.filter(
        Q(codename__endswith="project") |
        Q(codename__endswith="time") |
        Q(codename__endswith="membership") |
        Q(codename__endswith="milestone") |
        Q(codename__endswith="role") |
        Q(codename__endswith="issue")
    )
    for permission in manager_permissions:
        project_manager_group.permissions.add(permission)

    project_manager_group.save()


    manager_permissions = Permission.objects.filter(
        Q(codename="view_project") |
        Q(codename__endswith="time") |
        Q(codename__endswith="issue")
    )
    for permission in manager_permissions:
        internal_dev_group.permissions.add(permission)

    internal_dev_group.save()

    role, created = Role.objects.get_or_create(name="Project Manager", group = project_manager_group)
    role.save()

    role, created = Role.objects.get_or_create(name="Internal Developer", group = internal_dev_group)
    role.save()

setup_permissions()
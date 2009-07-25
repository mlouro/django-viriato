# -*- coding: utf-8 -*-
from django.test import TestCase
from projects.models import Project, Membership, Role
from django.contrib.auth.models import User, Group
from projects.setup import setup_permissions
from django.test.client import Client

class ProjectTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester", password="pw",
                                         email="tester@test.com", first_name="Testa")
        self.user.save()
        self.project = Project.objects.create(id=1, name="project1")

        setup_permissions()

        p = Project.objects.get(name="project1")
        u = User.objects.get(username="tester")
        r = Role.objects.get(name="Internal Developer")

        m = Membership.objects.create(user=u, project=p, role=r)
        m.save()

        self.client = Client()
        self.client.login(username="tester", password="pw")

    def test_add_projects(self):
        response = self.client.get('/projects/add/')
        self.failUnlessEqual(response.status_code, 302)

    def test_manage_people(self):
        response = self.client.get('/projects/1/people/')
        self.failUnlessEqual(response.status_code, 302)

    def test_can_add_tasks(self):
        response = self.client.get('/projects/1/task/save/')
        self.failUnlessEqual(response.status_code, 302)

    def test_can_add_messages(self):
        response = self.client.get('/projects/1/message/save/')
        self.failUnlessEqual(response.status_code, 200)





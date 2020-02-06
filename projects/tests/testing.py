import datetime

from django.contrib.auth.models import User
from django.test import Client, TestCase
from projects.models import Project, Task

class TestingHelper(TestCase):
    def assert_valid_project(self, project):
        self.assertIn('kind', project)
        self.assertEquals(project['kind'], 'project')

        self.assertIn('id', project)
        self.assertIn('title', project)
        self.assertIn('description', project)
        self.assertIn('created', project)
        self.assertIn('updated', project)
        self.assertIn('deadline', project)
        self.assertIn('status', project)
        self.assertIn('tasks', project)
        self.assertIn('author', project)
        self.assertIn('public', project)
        self.assertIn('individual', project)

    def assert_valid_task(self, task):
        self.assertIn('kind', task)
        self.assertEquals(task['kind'], 'task')

        self.assertIn('id', task)
        self.assertIn('title', task)
        self.assertIn('description', task)
        self.assertIn('created', task)
        self.assertIn('updated', task)
        self.assertIn('deadline', task)
        self.assertIn('status', task)
        self.assertIn('project', task)
        self.assertIn('resources', task)

    def setUp(self):
        self.client = Client()
        self.username = 'test_username'
        self.password = 'test_strong_password'

        self.user = User.objects.create_user(
            username=self.username, 
            first_name='Gustavo',
            last_name='Martinez',
            email='dario@iteso.mx',
            password=self.password)

        self.user.set_password(self.password)
        self.user.save()

        self.project = Project(
            title='EXAMPLE',
            description='EXAMPLE',
            deadline=datetime.datetime.now(),
            author=self.user
        )

        self.project.save()

        self.task = Task(
            title='EXAMPLE',
            description='EXAMPLE',
            deadline=datetime.datetime.now(),
            project=self.project
        )

        self.task.save()

        self.client.login(username=self.username, password=self.password)


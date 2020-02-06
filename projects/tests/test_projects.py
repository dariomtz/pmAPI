import datetime

from django.contrib.auth.models import User
from django.test import Client, TestCase
from projects.models import Project, Task


class TestProjects(TestCase):

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
        self.client.login(username=self.username, password=self.password)
        
    def test_get_projects(self):
        response = self.client.get('/api/projects/')

        self.assertEquals(response.status_code, 200)
        
        all_projects = response.json()

        self.assertIn('projects', all_projects)
        self.assertIn('kind', all_projects)
        self.assertEquals(all_projects['kind'], 'projects')

        for project in all_projects['projects']:
            self.assert_valid_project(project)

    def test_post_project(self):
        new_project = {
            'title': 'Example project',
            'description': 'Example description',
            'deadline' : str(datetime.datetime.now())
        }

        response = self.client.post('/api/projects/', data=new_project, content_type='application/json')

        self.assertEquals(response.status_code, 201)
        self.assert_valid_project(response.json())

    def test_get_project(self):
        response = self.client.get('/api/projects/' + str(self.project.id) + '/')

        self.assertEquals(response.status_code, 200)
        self.assert_valid_project(response.json())

    def test_put_project(self):
        new_project = {
            'title': 'A changed salmple title.',
            'description': 'A changed sample description.', 
            'deadline': str(datetime.datetime.now()),
            'status': False
        }
        
        response = self.client.put('/api/projects/' + str(self.project.id),
                                    data= new_project,
                                    content_type='application/json')
        
        self.assertEquals(response.status_code, 200)
        self.assert_valid_project(response.json())

    def test_delete_project(self):
        response = self.client.delete('/api/projects/' + str(self.project.id) + '/')

        self.assertEquals(response.status_code, 204)

        response = self.client.get('/api/projects/' + str(self.project.id) + '/')

        self.assertEquals(response.status_code, 404)

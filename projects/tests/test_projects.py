import datetime

from .testing import TestingHelperAuth, TestingHelperNotAuth

class TestProjectsAuth(TestingHelperAuth):
     
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
        
        response = self.client.put('/api/projects/' + str(self.project.id) + '/',
                                    data= new_project,
                                    content_type='application/json')
        
        self.assertEquals(response.status_code, 200)
        self.assert_valid_project(response.json())

    def test_delete_project(self):
        response = self.client.delete('/api/projects/' + str(self.project.id) + '/')

        self.assertEquals(response.status_code, 204)

        response = self.client.get('/api/projects/' + str(self.project.id) + '/')

        self.assertEquals(response.status_code, 404)

class TestProjectsNotAuth(TestingHelperNotAuth):
    def test_get_projects(self):
        response = self.client.get('/api/projects/')

        self.assertEquals(response.status_code, 401)
        
        self.assert_valid_error(response.json())

    def test_post_project(self):
        new_project = {
            'title': 'Example project',
            'description': 'Example description',
            'deadline' : str(datetime.datetime.now())
        }

        response = self.client.post('/api/projects/', data=new_project, content_type='application/json')

        self.assertEquals(response.status_code, 401)
        self.assert_valid_error(response.json())

    def test_get_project(self):
        response = self.client.get('/api/projects/' + str(self.project.id) + '/')

        self.assertEquals(response.status_code, 401)
        self.assert_valid_error(response.json())

    def test_put_project(self):
        new_project = {
            'title': 'A changed salmple title.',
            'description': 'A changed sample description.', 
            'deadline': str(datetime.datetime.now()),
            'status': False
        }
        
        response = self.client.put('/api/projects/' + str(self.project.id) + '/',
                                    data= new_project,
                                    content_type='application/json')
        
        self.assertEquals(response.status_code, 401)
        self.assert_valid_error(response.json())

    def test_delete_project(self):
        response = self.client.delete('/api/projects/' + str(self.project.id) + '/')

        self.assertEquals(response.status_code, 401)

        self.assert_valid_error(response.json())

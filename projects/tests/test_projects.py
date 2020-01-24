import datetime, uuid
from .project_testing_helper import ProjectTestingHelper

class TestProjects(ProjectTestingHelper):
    def test_invalid_methods(self):
        self.assert_invalid_methods('/api/projects/', ['PUT', 'PATCH', 'DELETE', 'TRACE', 'HEAD', 'OPTIONS'])
        self.assert_invalid_methods('/api/projects/' +  self.valid_project_id() + '/', ['OPTIONS', 'HEAD', 'TRACE', 'PATCH'])

    def test_not_found_project(self):
        response = self.client.get('/api/projects/' + 9999 + '/')

        self.assertEquals(response.status_code, 404)

        self.assert_valid_error(response.json())

    def test_get_valid_projects(self):

        response = self.client.get('/api/projects/')

        self.assertEquals(response.status_code, 200)
        
        all_projects = response.json()

        self.assertIn('projects', all_projects)
        self.assertIn('kind', all_projects)
        self.assertEquals(all_projects['kind'], 'projects')

        for project in all_projects['projects']:
            self.assert_valid_project(project)
    
    def test_get_valid_project(self):
        response = self.client.get('/api/projects/' + self.valid_project_id() + '/')
        self.assertEquals(response.status_code, 200)
        self.assert_valid_project(response.json())

    def test_get_invalid_project(self):
        #try to access a project that does not belong to you
        return

    def test_post_valid_project(self):
        new_project = {
            'title':'This is a sample title.',
            'description': 'This is a sample description.',
            'deadline': str(datetime.datetime.today())
        }

        self.assert_post_valid_project(new_project) 

    def test_post_invalid_project_invalid_title(self): 
        new_project = {
            'title':'This is a sample title with more than 100 chars. This is a sample title with more than 100 chars. This is a sample title with more than 100 chars.',
            'description': 'This is a sample description.',
            'deadline': str(datetime.datetime.today())
        }

        self.assert_post_invalid_project(new_project)

    def test_post_invalid_project_missing_title(self):
        new_project = {
            'description': 'A valid description'
        }

        self.assert_post_invalid_project(new_project)

    def test_post_invalid_project_missing_description(self):
        new_project = {
            'title': 'Valid title'
        }

        self.assert_post_invalid_project(new_project)

    def test_post_invalid_project_deadline(self):
        new_project = {
            'title': 'Valid title',
            'description': 'Valid description',
            'deadline': 'Not a date'
        }
        
        self.assert_post_invalid_project(new_project)

    def test_put_valid_project(self):
        new_project = {
            'title': 'A changed salmple title.',
            'description': 'A changed sample description.', 
            'deadline': str(datetime.datetime.now()),
            'status': False
        }

        response = self.assert_put_valid_project(new_project)

        self.assertEquals(response['status'], False)

    def test_put_invalid_project_invalid_title(self):
        new_project = {
            'title': 'Very large invalid title. Very large invalid title. Very large invalid title. Very large invalid title.Very large invalid title. Very large invalid title. Very large invalid title. Very large invalid title. Very large invalid title.',
            'description': 'Valid description.',
            'deadline': str(datetime.datetime.now()),
            'status': False
        }

        self.assert_put_invalid_project(new_project)

    def test_put_invalid_project_invalid_date(self):
        new_project = {
            'title': 'A valid title',
            'description': 'A valid description',
            'deadline': 'Not a date lol',
            'status': False
        }

        self.assert_put_invalid_project(new_project)

    def test_put_invalid_project_missing_deadline(self):
        new_project = {
            'title': 'A valid title',
            'description': 'A valid description',
            'status': False
        }

        self.assert_put_invalid_project(new_project)

    def test_delete_valid_project(self):
        response = self.client.delete('/api/projects/' + self.valid_project_id() + '/')

        self.assertEquals(response.status_code, 204)
    
    def test_delete_invalid_project(self):
        #delete a project that does not belong to you
        return
    



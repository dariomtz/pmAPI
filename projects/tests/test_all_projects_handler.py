import datetime
from .testing_library import AssertHelper

class TestAllProjectsHandler(AssertHelper):
    def test_post_valid_project_complete(self):
        new_project = {
            'title':'This is a sample title.',
            'description': 'This is a sample description.',
            'deadline': str(datetime.datetime.today())
        }

        self.assert_post_valid_project(new_project)
    
    def test_post_valid_project_missing_deadline(self):
        new_project = {
            'title':'This is a sample title.',
            'description': 'This is a sample description.'
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

    def test_get_valid_projects(self):

        response = self.client.get('/api/projects/')

        self.assertEquals(response.status_code, 200)
        
        all_projects = response.json()

        self.assertIn('projects', all_projects)

        projects = all_projects['projects']
        for key in projects:
            project = projects[key]
            self.assert_valid_project(project)

    def test_get_invalid_projects(self):
        
        return
    
    def test_invalid_methods(self):
        self.assert_invalid_methods('/api/projects/', ['PUT', 'PATCH', 'DELETE', 'TRACE', 'HEAD', 'OPTIONS'])




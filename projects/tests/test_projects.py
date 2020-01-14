import datetime, uuid
from .project_testing_helper import ProjectTestingHelper

class TestProjects(ProjectTestingHelper):
    def test_invalid_methods(self):
        self.assert_invalid_methods('/api/projects/', ['PUT', 'PATCH', 'DELETE', 'TRACE', 'HEAD', 'OPTIONS'])
        self.assert_invalid_methods('/api/projects/' +  self.valid_project_id() + '/', ['OPTIONS', 'HEAD', 'TRACE'])

    def test_not_found_project(self):
        response = self.client.get('/api/projects/' + str(uuid.uuid4()) + '/')

        self.assertEquals(response.status_code, 404)

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
    
    def test_get_valid_project(self):
        all_projects_request = self.client.get('/api/projects/')
        all_projects_dict = all_projects_request.json()['projects']

        self.assertEquals(all_projects_request.status_code, 200)

        for key in all_projects_dict:
            response = self.client.get('/api/projects/' + key + '/')
            self.assertEquals(response.status_code, 200)
            self.assert_valid_project(response.json())

    def test_get_invalid_project(self):
        
        return

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

    def test_put_valid_project_status_true(self):
        new_project = {
            'title': 'A changed salmple title.',
            'description': 'A changed sample description.', 
            'deadline': str(datetime.datetime.now()),
            'status': True
        }

        response = self.assert_put_valid_project(new_project)

        self.assertEquals(response['status'], True)

    def test_put_valid_project_status_false(self):
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

    def test_put_invalid_project_invalid_status(self):
        new_project = {
            'title': 'A valid title',
            'description': 'A valid description',
            'deadline': str(datetime.datetime.now()),
            'status': 'Not a boolean lol'
        }

        response = self.assert_put_invalid_project(new_project)

        self.assertEquals(response['errors']['status'][0]['message'], 'Enter a valid boolean value.')
        self.assertEquals(response['errors']['status'][0]['code'], 'invalid')

    def test_put_invalid_project_missing_title(self):
        new_project = {
            'description': 'A changed sample description.', 
            'deadline': str(datetime.datetime.now()),
            'status': False
        }

        self.assert_put_invalid_project(new_project)

    def test_put_invalid_project_missing_description(self):
        new_project = {
            'title': 'A changed salmple title.',
            'deadline': str(datetime.datetime.now()),
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

    def test_put_invalid_project_missing_status(self):
        new_project = {
            'title': 'A valid title',
            'description': 'A valid description',
            'deadline': str(datetime.datetime.now()),
        }

        self.assert_put_invalid_project(new_project)

    def test_patch_valid_project_title(self):
        new_project = {
            'title': 'New title.',        
        }

        response = self.assert_patch_valid_project(new_project)

        self.assertEquals(response['title'], 'New title.')

    def test_patch_valid_project_description(self):
        new_project = {
            'description': 'A totally new description'
        }

        response = self.assert_patch_valid_project(new_project)

        self.assertEquals(response['description'], 'A totally new description')

    def test_patch_valid_project_deadline(self):
        date = str(datetime.datetime.now())

        new_project = {
            'deadline': date
        }

        response = self.assert_patch_valid_project(new_project)

        self.assertEquals(response['deadline'], date)

    def test_patch_valid_project_status(self):
        new_project = {
            'status': True
        }

        response = self.assert_patch_valid_project(new_project)

        self.assertTrue(response['status'])

    def test_patch_invalid_project(self):
        return

#     def test_delete_valid_project(self):
    
#     def test_delete_invalid_project(self):
    



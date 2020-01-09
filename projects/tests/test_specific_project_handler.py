import datetime, uuid
from .testing_library import AssertHelper

class TestSpecificProjectHandler(AssertHelper):
    def test_not_found_project(self):
        response = self.client.get('/api/projects/' + str(uuid.uuid4()) + '/')

        self.assertEquals(response.status_code, 404)

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

    def test_post_valid_task_complete(self):    
        new_task = {
            'title': 'This is a sample title for a task',
            'description': 'This is a sample description for a task',
            'resources': 'Sample resources',
            'deadline': str(datetime.datetime.now()),
            'startDate': str(datetime.datetime.today())
        }

        self.assert_post_valid_task(new_task)
    
    def test_post_valid_task_without_optional_params(self):
        new_task = {
            'title': 'This is a sample title for a task',
            'description': 'This is a sample description for a task'
        }

        self.assert_post_valid_task(new_task)

    def test_post_invalid_task(self):
        project_id = self.valid_project_id()
        
        #test case 1
        new_task = {
            'title': 'This is a sample title for a task long enough to cause an error. This is a sample title for a task long enough to cause an error. This is a sample title for a task long enough to cause an error.',
            'description': 'This is a sample description for a task',
            'resources': 'Sample resources',
            'deadline': 'Just not a date lol',
            'startDate': 'Just not a date lol'
        }

        response = self.client.post('/api/projects/' + project_id + '/', data=new_task, content_type='application/json')
        
        self.assertEquals(response.status_code, 400)

        error = response.json()

        self.assert_valid_error(error)

        #test case 2
        empty_task = {}

        error = self.client.post('/api/projects/' + project_id + '/', data=empty_task, content_type='application/json')
        
        self.assertEquals(error.status_code, 400)

        error = error.json()

        self.assert_valid_error(error)

    def test_put_valid_project(self):
        new_project = {
            'title': 'A changed salmple title.',
            'description': 'A changed sample description.', 
            'deadline': str(datetime.datetime.now()),
            'status': False
        }

        response = self.client.put('/api/projects/' + self.valid_project_id() + '/', data=new_project, content_type='application/json')
    
        self.assertEquals(response.status_code, 200)

        put_project = response.json()

        self.assert_valid_project(put_project)

    def test_put_invalid_project(self):
        #test case 1
        new_project = {
            'title': 'A changend invalid title. A changend invalid title. A changend invalid title. A changend invalid title. A changend invalid title. A changend invalid title. A changend invalid title. '
        }

        response = self.client.put('/api/projects/' + self.valid_project_id() + '/', data=new_project, content_type='application/json')

        self.assertEquals(response.status_code, 400)

        put_project = response.json()

        self.assert_valid_error(put_project)

    def test_patch_valid_project(self):
        new_project = {
            'title': 'New title.',
            'description': 'New description.',
            'status': True,            
        }

        response = self.client.patch('/api/projects/' + self.valid_project_id() + '/', data=new_project, content_type='application/json')

        patched_project = response.json()

        self.assert_valid_project(patched_project)

    def test_patch_invalid_project(self):
        return

#     def test_delete_valid_project(self):
    
#     def test_delete_invalid_project(self):
    
    def test_invalid_methods_2(self):

        self.assert_invalid_methods('/api/projects/' +  self.valid_project_id() + '/', ['OPTIONS', 'HEAD', 'TRACE'])
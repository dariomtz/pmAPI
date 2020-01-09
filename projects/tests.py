import json, datetime, uuid
from django.test import Client, TestCase

# Create your tests here.

class Tests(TestCase):
    def setUp(self):
        self.client =  Client()

    def valid_project_id(self):
        new_project = {
            'title': 'This is a sample title',
            'description' : 'This is a sample description'
        }

        response = self.client.post('/api/projects/', data=new_project, content_type='application/json')

        self.assertEquals(response.status_code, 200)

        project = response.json()

        self.assert_valid_project(project)

        return project['id']

    def valid_task_id(self):
        new_task = {
            'title': 'Sample task title.',
            'description': 'Sample task description'
        }

        response = self.client.post('/api/projects/' + self.valid_project_id() + '/', data=new_task, content_type='application/json')

        self.assertEquals(response.status_code, 200)

        task = response.json()

        self.assert_valid_task(task)

        return task['id']

    def assert_valid_task(self, task):
        self.assertTrue('kind' in task)
        self.assertEquals(task['kind'], 'task')

        self.assertTrue('id' in task)
        self.assertTrue('title' in task)
        self.assertTrue('description' in task)
        self.assertTrue('created' in task)
        self.assertTrue('updated' in task)
        self.assertTrue('inCharge' in task)
        self.assertTrue('deadline' in task)
        self.assertTrue('startDate' in task)
        self.assertTrue('resources' in task)
        self.assertTrue('status' in task)

    def assert_valid_project(self, project):
        self.assertTrue('kind' in project)
        self.assertEquals(project['kind'], 'project')

        self.assertTrue('id' in project)
        self.assertTrue('title' in project)
        self.assertTrue('description' in project)
        self.assertTrue('created' in project)
        self.assertTrue('updated' in project)
        self.assertTrue('canRead' in project)
        self.assertTrue('canEdit' in project)
        self.assertTrue('admins' in project)
        self.assertTrue('deadline' in project)
        self.assertTrue('status' in project)

        for k in project['tasks']:
            self.assert_valid_task(project['tasks'][k])
        
    def assert_valid_error(self, error):
        self.assertTrue('kind' in error)
        self.assertEquals(error['kind'], 'error')

        self.assertTrue('errors' in error)

        for key in error['errors']:
            e = error['errors'][key]
            for specific_error in e:
                self.assertTrue('message' in specific_error)
                self.assertTrue('code' in specific_error)

    def assert_invalid_methods(self, path, list_of_invalid_methods):
        list_of_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'TRACE', 'HEAD', 'OPTIONS']

        for method in list_of_invalid_methods:
            self.assertTrue(method in list_of_methods)

            if method == 'GET':
                response = self.client.get(path)
            elif method == 'POST':
                response = self.client.post(path)
            elif method == 'PUT':
                response = self.client.put(path)
            elif method == 'PATCH':
                response = self.client.patch(path)
            elif method == 'DELETE':
                response = self.client.delete(path)
            elif method == 'TRACE':
                response = self.client.trace(path)
            elif method == 'HEAD':
                response = self.client.head(path)
            elif method == 'OPTIONS':
                response = self.client.options(path)
            
            self.assertEquals(response.status_code, 405)
    
    #tests for '/api/projects/'
    def test_post_valid_project(self):
        #test case 1
        new_project = {
            'title':'This is a sample title.',
            'description': 'This is a sample description.',
            'deadline': str(datetime.datetime.today())
        }

        response = self.client.post('/api/projects/', data=new_project, content_type='application/json')        

        self.assertEquals(response.status_code, 200)

        project = response.json()
        self.assert_valid_project(project)

        #test case 2
        new_project = {
            'title':'This is a sample title.',
            'description': 'This is a sample description.'
        }

        response = self.client.post('/api/projects/', data=new_project, content_type='application/json')        

        self.assertEquals(response.status_code, 200)

        project = response.json()
        self.assert_valid_project(project)
        
    def test_post_invalid_project(self):
        #test case 1
        bad_title = {
            'title':'This is a sample title with more than 100 chars. This is a sample title with more than 100 chars. This is a sample title with more than 100 chars.',
            'description': 'This is a sample description.',
            'deadline': str(datetime.datetime.today())
        }

        response = self.client.post('/api/projects/', data=bad_title, content_type='application/json')        

        self.assertEquals(response.status_code, 400)

        error = response.json()
        self.assert_valid_error(error)

        #test case 2
        empty_dict = {}

        response = self.client.post('/api/projects/', data=empty_dict, content_type='application/json')        

        self.assertEquals(response.status_code, 400)

        error = response.json()
        self.assert_valid_error(error)
    
    def test_get_valid_projects(self):

        response = self.client.get('/api/projects/')

        self.assertEquals(response.status_code, 200)
        
        all_projects = response.json()

        self.assertTrue('projects' in all_projects)

        projects = all_projects['projects']
        for key in projects:
            project = projects[key]
            self.assert_valid_project(project)

    def test_get_invalid_projects(self):
        
        return
    
    def test_invalid_methods(self):
        self.assert_invalid_methods('/api/projects/', ['PUT', 'PATCH', 'DELETE', 'TRACE', 'HEAD', 'OPTIONS'])

    #tests for '/api/projects/uuid/'
    def test_all_methods_not_found_project(self):
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

    def test_post_valid_task(self):
        project_id = self.valid_project_id()
        #test case 1: With all the possible fields
        new_task = {
            'title': 'This is a sample title for a task',
            'description': 'This is a sample description for a task',
            'resources': 'Sample resources',
            'deadline': str(datetime.datetime.now()),
            'startDate': str(datetime.datetime.today())
        }

        response = self.client.post('/api/projects/' + project_id + '/', data=new_task, content_type='application/json')
        
        self.assertEquals(response.status_code, 200)

        task = response.json()

        self.assert_valid_task(task)

        #test case 2: Without the optional fields
        new_task = {
            'title': 'This is a sample title for a task',
            'description': 'This is a sample description for a task'
        }

        task = self.client.post('/api/projects/' + project_id + '/', data=new_task, content_type='application/json')
        
        self.assertEquals(task.status_code, 200)

        task = task.json()

        self.assert_valid_task(task)

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
            'status': 'o'
        }

        response = self.client.put('/api/projects/' + self.valid_project_id() + '/', data=new_project, content_type='application/json')
    
        self.assertEquals(response.status_code, 200)

        put_project = response.json()

        self.assert_valid_project(put_project)

    def test_put_invalid_project(self):
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
            'description': 'New description.'            
        }

        response = self.client.patch('/api/projects/' + self.valid_project_id() + '/', data=new_project, content_type='application/json')

        patched_project = response.json()

        self.assert_valid_project(patched_project)

#     def test_patch_invalid_project(self):

#     def test_delete_valid_project(self):
    
#     def test_delete_invalid_project(self):
    
    def test_invalid_methods_2(self):

        self.assert_invalid_methods('/api/projects/' +  self.valid_project_id() + '/', ['OPTIONS', 'HEAD', 'TRACE'])

# class TestSpecificTaskHandler(TestCase):

#     def setUp(self):
#         self.factory = RequestFactory()

#     def test_all_methods_not_found_task(self):

#     def test_get_valid_task(self):

#     def test_post_valid_task(self):

#     def test_post_invalid_task(self):

#     def test_put_valid_task(self):

#     def test_put_invalid_task(self):

#     def test_patch_valid_task(self):

#     def test_patch_invalid_task(self):

#     def test_delete_valid_task(self):

#     def test_delete_invalid_task(self):

#     def test_invalid_methods(self):


import json, datetime, uuid
from django.test import Client, TestCase

# Create your tests here.

def assert_valid_task(task):
    assert 'kind' in task
    assert task['kind'] == 'task'

    assert 'id' in task
    assert 'title' in task
    assert 'description' in task
    assert 'created' in task
    assert 'updated' in task
    assert 'inCharge' in task
    assert 'deadline' in task
    assert 'startDate' in task
    assert 'resources' in task
    assert 'status' in task

def assert_valid_project(project):
    assert 'kind' in project
    assert project['kind'] == 'project'

    assert 'id' in project
    assert 'title' in project
    assert 'description' in project
    assert 'created' in project
    assert 'updated' in project
    assert 'canRead' in project
    assert 'canEdit' in project
    assert 'admins' in project
    assert 'deadline' in project
    assert 'status' in project

    assert 'tasks' in project
    for k in project['tasks']:
        assert_valid_task(project['tasks'][k])
    
def assert_valid_error(error):
    assert 'kind' in error
    assert error['kind'] == 'error'
    assert 'errors' in error
    
    for key in error['errors']:
        for e in error['errors'][key]:
            assert 'message' in e
            assert 'code' in e

def assert_invalid_methods(path, list_of_methods):
    for method in list_of_methods:
        if method == 'GET':
            response = Client().get(path)
        elif method == 'POST':
            response = Client().post(path)
        elif method == 'PUT':
            response = Client().put(path)
        elif method == 'PATCH':
            response = Client().patch(path)
        elif method == 'DELETE':
            response = Client().delete(path)
        elif method == 'TRACE':
            response = Client().trace(path)
        elif method == 'HEAD':
            response = Client().head(path)
        elif method == 'OPTIONS':
            response = Client().options(path)
        else:
            assert method == 'INVALID'
        
        assert response.status_code == 405

class TestAllProjectsHandler(TestCase):

    def setUp(self):
        self.client =  Client()

    def test_post_valid_project(self):
        new_project = {
            'title':'This is a sample title.',
            'description': 'This is a sample description.',
            'deadline': str(datetime.datetime.today())
        }

        response = self.client.post('/api/projects/', data=new_project, content_type='application/json')        

        self.assertEquals(response.status_code, 200)

        response_dict = response.json()
        assert_valid_project(response_dict)
        
    def test_post_invalid_project(self):
        #test case 1
        bad_title = {
            'title':'This is a sample title with more than 100 chars. This is a sample title with more than 100 chars. This is a sample title with more than 100 chars.',
            'description': 'This is a sample description.',
            'deadline': str(datetime.datetime.today())
        }

        response = self.client.post('/api/projects/', data=bad_title, content_type='application/json')        

        self.assertEquals(response.status_code, 400)

        response_dict = response.json()
        assert_valid_error(response_dict)

        #test case 2
        empty_dict = {}

        response = self.client.post('/api/projects/', data=empty_dict, content_type='application/json')        

        self.assertEquals(response.status_code, 400)

        response_dict = json.loads(response.content, encoding='utf8')
        assert_valid_error(response_dict)
    
    def test_get_valid_projects(self):

        response = self.client.get('/api/projects/')

        self.assertEquals(response.status_code, 200)
        
        response_dict = response.json()

        assert 'projects' in response_dict

        projects = response_dict['projects']
        for key in projects:
            project = projects[key]
            assert_valid_project(project)

    def test_get_invalid_projects(self):
        #assert 401 if the user doesn't exists
        return
    
    def test_invalid_methods(self):
        assert_invalid_methods('/api/projects/', ['PUT', 'PATCH', 'DELETE', 'TRACE', 'HEAD', 'OPTIONS'])

class TestSpecificProjectHandler(TestCase):

    def setUp(self):
        self.client = Client()

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
            assert_valid_project(response.json())

    def test_get_invalid_project(self):
        #assert 401 if the user doesn't have access to the project
        return

    def test_post_valid_task(self):
        new_project = {
            'title':'This is a sample title.',
            'description': 'This is a sample description.',
            'deadline': str(datetime.datetime.today())
        }

        project = self.client.post('/api/projects/', data=new_project, content_type='application/json')

        self.assertEquals(project.status_code, 200)

        project = project.json()

        new_task = {
            'title': 'This is a sample title for a task',
            'description': 'This is a sample description for a task',
            'resources': 'Sample resources',
            'deadline': str(datetime.datetime.now()),
            'startDate': str(datetime.datetime.today())
        }

        task = self.client.post('/api/projects/' + project['id'] + '/', data=new_task, content_type='application/json')
        
        self.assertEquals(task.status_code, 200)

        task = task.json()

        assert_valid_task(task)

    def test_post_invalid_task(self):
        
        new_project = {
            'title':'This is a sample title.',
            'description': 'This is a sample description.',
            'deadline': str(datetime.datetime.today())
        }

        project = self.client.post('/api/projects/', data=new_project, content_type='application/json')

        self.assertEquals(project.status_code, 200)

        project = project.json()

        #test case 1
        new_task = {
            'title': 'This is a sample title for a task long enough to cause an error. This is a sample title for a task long enough to cause an error. This is a sample title for a task long enough to cause an error.',
            'description': 'This is a sample description for a task',
            'resources': 'Sample resources',
            'deadline': 'Just not a date lol',
            'startDate': 'Just not a date lol'
        }

        error = self.client.post('/api/projects/' + project['id'] + '/', data=new_task, content_type='application/json')
        
        self.assertEquals(error.status_code, 400)

        error = error.json()

        assert_valid_error(error)

        #test case 2
        empty_task = {
            'title': 'This is a sample title for a task long enough to cause an error. This is a sample title for a task long enough to cause an error. This is a sample title for a task long enough to cause an error.',
            'description': 'This is a sample description for a task',
            'resources': 'Sample resources',
            'deadline': 'Just not a date lol',
            'startDate': 'Just not a date lol'
        }

        error = self.client.post('/api/projects/' + project['id'] + '/', data=empty_task, content_type='application/json')
        
        self.assertEquals(error.status_code, 400)

        error = error.json()

        assert_valid_error(error)

    def test_put_valid_project(self):
        new_project = {
            'title': 'A salmple title.',
            'description': 'A sample description.'
        }
        project = self.client.post('/api/projects/', data= new_project, content_type='application/json')
        self.assertEquals(project.status_code, 200)

        project = project.json()

        new_project = {
            'title': 'A changed salmple title.',
            'description': 'A changed sample description.', 
            'status': 'o'
        }

        put_project = self.client.put('/api/projects/' + project['id'] + '/', data=new_project, content_type='application/json')
    
        self.assertEquals(put_project.status_code, 200)

        put_project = put_project.json()

        assert_valid_project(put_project)

        self.assertEquals(put_project['id'], project['id'])
        self.assertEquals(put_project['created'], project['created'])


#     def test_put_invalid_project(self):

#     def test_patch_valid_project(self):

#     def test_patch_invalid_project(self):

#     def test_delete_valid_project(self):
    
#     def test_delete_invalid_project(self):
    
#     def test_invalid_methods(self):

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


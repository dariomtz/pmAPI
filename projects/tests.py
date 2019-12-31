import json, datetime
from django.test import Client, TestCase
from .views import all_projects, specific_project

# Create your tests here.

def assert_valid_task(task, key):
    return

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
        assert_valid_task(project['tasks'][k], k)
    
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

    def test_invalid_methods(self):
        assert_invalid_methods('/api/projects/', ['PUT', 'PATCH', 'DELETE', 'TRACE', 'HEAD', 'OPTIONS'])

# class TestSpecificProjectHandler(TestCase):

#     def setUp(self):
#         self.factory = RequestFactory()

#     def test_all_methods_not_found_project(self):

#     def test_get_valid_project(self):

#     def test_get_invalid_project(self):

#     def test_post_valid_task(self):

#     def test_post_invalid_task(self):

#     def test_put_valid_project(self):

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


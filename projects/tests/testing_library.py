import datetime
from django.test import Client, TestCase

class AssertHelper(TestCase):
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
    
    def assert_valid_datetime(self, datetime_string):
        if datetime_string == None:
            return
        format_string =  '%Y-%m-%d %H:%M:%S.%f'
        try :
            datetime.datetime.strptime(datetime_string, format_string)
        except ValueError:
            raise AssertionError

    def assert_valid_task(self, task):
        self.assertIn('kind', task)
        self.assertEquals(task['kind'], 'task')

        self.assertIn('id', task)
        self.assertIn('title', task)
        self.assertIn('description', task)
        self.assertIn('created', task)
        self.assert_valid_datetime(task['created'])
        self.assertIn('updated', task)
        self.assert_valid_datetime(task['updated'])
        self.assertIn('inCharge', task)
        self.assertIn('deadline', task)
        self.assert_valid_datetime(task['deadline'])
        self.assertIn('startDate', task)
        self.assert_valid_datetime(task['startDate'])
        self.assertIn('resources', task)
        self.assertIn('status', task)

    def assert_valid_project(self, project):
        self.assertIn('kind', project)
        self.assertEquals(project['kind'], 'project')

        self.assertIn('id', project)
        self.assertIn('title', project)
        self.assertIn('description', project)
        self.assertIn('created', project)
        self.assert_valid_datetime(project['created'])
        self.assertIn('updated', project)
        self.assert_valid_datetime(project['updated'])
        self.assertIn('canRead', project)
        self.assertIn('canEdit', project)
        self.assertIn('admins', project)
        self.assertIn('deadline', project)
        self.assert_valid_datetime(project['deadline'])
        self.assertIn('status', project)

        for k in project['tasks']:
            self.assert_valid_task(project['tasks'][k])
        
    def assert_valid_error(self, error):
        self.assertIn('kind', error)
        self.assertEquals(error['kind'], 'error')

        self.assertIn('errors', error)

        for key in error['errors']:
            e = error['errors'][key]
            for specific_error in e:
                self.assertIn('message', specific_error)
                self.assertIn('code', specific_error)

    def assert_invalid_methods(self, path, list_of_invalid_methods):
        list_of_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'TRACE', 'HEAD', 'OPTIONS']

        for method in list_of_invalid_methods:
            self.assertIn(method, list_of_methods)

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
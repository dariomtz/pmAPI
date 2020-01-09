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
    
    def assert_post_invalid_project(self, new_project):
        response = self.client.post('/api/projects/', data=new_project, content_type='application/json')

        self.assertEquals(response.status_code, 400)

        error = response.json()
        self.assert_valid_error(error)   

    def assert_post_valid_project(self, new_project):
        response = self.client.post('/api/projects/', data=new_project, content_type='application/json')

        self.assertEquals(response.status_code, 200)

        project = response.json()
        self.assert_valid_project(project)  
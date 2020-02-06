import datetime, uuid
from .testing import TestingHelperAuth, TestingHelperNotAuth

class TestTasksAuth(TestingHelperAuth):

    def test_get_tasks(self):
        response = self.client.get('/api/projects/' + str(self.project.id) + '/tasks/')

        self.assertEquals(response.status_code, 200)

        task_list = response.json()
        self.assertIn('kind', task_list)
        self.assertEquals('task_list', task_list['kind'])
        self.assertIn('tasks', task_list)

        for task in task_list['tasks']:
            self.assert_valid_task(task)

    def test_post_tasks(self):
        new_task = {
            'title': 'Example.',
            'description': 'Example.',
            'deadline': str(datetime.datetime.now()),
            'status': True
        }

        response = self.client.post('/api/projects/' + str(self.project.id) + '/tasks/',
                                    data=new_task,
                                    content_type='application/json')

        self.assertEquals(response.status_code, 201)
        self.assert_valid_task(response.json())

    def test_get_task(self):
        response = self.client.get('/api/projects/' + str(self.project.id) + '/tasks/' + str(self.task.id) + '/')

        self.assertEquals(response.status_code, 200)
        self.assert_valid_task(response.json())

    def test_put_task(self):
        new_task = {
            'title': 'Example title.',
            'description': 'Example description.',
            'deadline': str(datetime.datetime.now()),
            'status' : True
        }

        response = self.client.put('/api/projects/' + str(self.project.id) + '/tasks/' + str(self.task.id) + '/',
                                    data=new_task,
                                    content_type='application/json')
        
        self.assertEquals(response.status_code, 200)
        self.assert_valid_task(response.json())

    def test_delete_task(self):
        response = self.client.delete('/api/projects/' + str(self.project.id) + '/tasks/' + str(self.task.id) + '/')

        self.assertEquals(response.status_code, 204)

        response = self.client.get('/api/projects/' + str(self.project.id) + '/tasks/' + str(self.task.id) + '/')

        self.assertEquals(response.status_code, 404)

class TestTasksNotAuth(TestingHelperNotAuth):

    def test_get_tasks(self):
        response = self.client.get('/api/projects/' + str(self.project.id) + '/tasks/')

        self.assertEquals(response.status_code, 401)

        self.assert_valid_error(response.json())

    def test_post_tasks(self):
        new_task = {
            'title': 'Example.',
            'description': 'Example.',
            'deadline': str(datetime.datetime.now()),
            'status': True
        }

        response = self.client.post('/api/projects/' + str(self.project.id) + '/tasks/',
                                    data=new_task,
                                    content_type='application/json')

        self.assertEquals(response.status_code, 401)
        self.assert_valid_error(response.json())

    def test_get_task(self):
        response = self.client.get('/api/projects/' + str(self.project.id) + '/tasks/' + str(self.task.id) + '/')

        self.assertEquals(response.status_code, 401)
        self.assert_valid_error(response.json())

    def test_put_task(self):
        new_task = {
            'title': 'Example title.',
            'description': 'Example description.',
            'deadline': str(datetime.datetime.now()),
            'status' : True
        }

        response = self.client.put('/api/projects/' + str(self.project.id) + '/tasks/' + str(self.task.id) + '/',
                                    data=new_task,
                                    content_type='application/json')
        
        self.assertEquals(response.status_code, 401)
        self.assert_valid_error(response.json())

    def test_delete_task(self):
        response = self.client.delete('/api/projects/' + str(self.project.id) + '/tasks/' + str(self.task.id) + '/')

        self.assertEquals(response.status_code, 401)
        self.assert_valid_error(response.json())

        

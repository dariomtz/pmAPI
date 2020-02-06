import datetime, uuid
from .testing import TestingHelper

class TestTasks(TestingHelper):

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

    """
        TODO:
        FINISH ADDING ALL THE TESTING FUNCTIONS

    def test_get_task(self):
    def test_put_task(self):
    def test_delete_task(self):

    """

import datetime, uuid
from .task_testing_helper import TaskTestingHelper

class TestTasks(TaskTestingHelper):
    def test_invalid_methods(self):
        ids = self.valid_task_id()
        self.assert_invalid_methods('/api/projects/' + ids['projectId'] + '/' + ids['taskId'] + '/',
        ['OPTIONS', 'HEAD', 'TRACE', 'PATCH', 'POST'])

    def test_get_not_found_task(self):
        response = self.client.get('/api/projects/' + self.valid_project_id() + '/' + str(uuid.uuid4()) + '/')
        
        self.assertEquals(response.status_code, 404)

        self.assert_valid_error(response.json())

        response = self.client.get('/api/projects/' + 999 + '/' + self.valid_task_id()['taskId']  + '/')

        self.assertEquals(response.status_code, 404)

        self.assert_valid_error(response.json())

    def test_get_valid_task(self):
        ids = self.valid_task_id()
        response = self.client.get('/api/projects/' + ids['projectId'] + '/' + ids['taskId'] + '/')

        self.assertEquals(response.status_code, 200)

        self.assert_valid_task(response.json())

    def test_get_invalid_task(self):
        #this is only invalid when the user does not have permisión tu read the task
        return

    def test_post_valid_task(self):    
        new_task = {
            'title': 'This is a sample title for a task',
            'description': 'This is a sample description for a task',
            'resources': 'Sample resources',
            'deadline': str(datetime.datetime.now()),
        }

        self.assert_post_valid_task(new_task)
    
    def test_post_invalid_task_bad_title(self):
        new_task = {
            'title': 'This is a sample title for a task long enough to cause an error. This is a sample title for a task long enough to cause an error. This is a sample title for a task long enough to cause an error.',
            'description': 'This is a sample description for a task',
        }

        self.assert_post_invalid_task(new_task)

    def test_post_invalid_task_bad_deadline(self):
        new_task = {
            'title': 'Valid title',
            'description': 'Valid description',
            'deadline': 'Not a date'
        }
        
        self.assert_post_invalid_task(new_task)

    def test_put_valid_task_status(self):
        task = {
            'title':'Valid title',
            'description': 'Valid description',
            'deadline': '2020-01-22 19:36:50',
            'resources': '',
            'status': True,
        }

        response = self.assert_put_valid_task(task)

        self.assertTrue(response['status'])

    def test_put_invalid_task_bad_title(self):
        task = {
            'title':'Very long invalid title. Very long invalid title. Very long invalid title. Very long invalid title. Very long invalid title. ',
            'description': 'Valid description',
            'deadline': '2020-01-22 19:36:50',
            'resources': '',
            'status': False,
        }

        self.assert_put_invalid_task(task)

    def test_put_invalid_task_bad_deadline(self):
        task = {
            'title':'Valid title',
            'description': 'Valid description',
            'deadline': 'Not a date',
            'resources': '',
            'status': False,
        }

        self.assert_put_invalid_task(task)

    def test_put_invalid_task_status(self):
        task = {
            'title':'Valid title',
            'description': 'Valid description',
            'deadline': '2020-01-22 19:36:50',
            'resources': '',
            'status': None,
        }

        self.assert_put_invalid_task(task)

    def test_put_invalid_task_missing_deadline(self):
        task = {
            'title':'Valid title',
            'description': 'Valid description',
            'resources': '',
            'status': False,
        }

        self.assert_put_invalid_task(task)

    def test_delete_valid_task(self):
        ids = self.valid_task_id()
        response = self.client.delete('/api/projects/' + ids['projectId'] + '/' + ids['taskId'] + '/')

        self.assertEquals(response.status_code, 204)
        
    def test_delete_invalid_task(self):
        return


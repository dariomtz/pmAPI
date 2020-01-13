import datetime, uuid
from .task_testing_helper import TaskTestingHelper

class TestTasks(TaskTestingHelper):

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

    def test_post_invalid_task_bad_title(self):
        new_task = {
            'title': 'This is a sample title for a task long enough to cause an error. This is a sample title for a task long enough to cause an error. This is a sample title for a task long enough to cause an error.',
            'description': 'This is a sample description for a task',
        }

        self.assert_post_invalid_task(new_task)

    def test_post_invalid_task_missing_title(self):
        new_task = {
            'description': 'This is a sample description for a task',
        }

        self.assert_post_invalid_task(new_task)

    def test_post_invalid_task_missing_description(self):
        new_task = {
            'title': 'Valid title'
        }

        self.assert_post_invalid_task(new_task)
    
    def test_post_invalid_task_bad_deadline(self):
        new_task = {
            'title': 'Valid title',
            'description': 'Valid description',
            'deadline': 'Not a date'
        }
        
        self.assert_post_invalid_task(new_task)

    def test_post_invalid_task_bad_startDate(self):
        new_task = {
            'title': 'Valid title',
            'description': 'Valid description',
            'startDate': 'Not a date'
        }

        self.assert_post_invalid_task(new_task)


        
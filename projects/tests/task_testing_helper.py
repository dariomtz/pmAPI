from .testing_library import AssertHelper

class TaskTestingHelper(AssertHelper):
    
    def assert_post_valid_task(self, new_task):
        response = self.client.post('/api/projects/' + self.valid_project_id() + '/', data=new_task, content_type='application/json')
        
        self.assertEquals(response.status_code, 200)

        task = response.json()

        self.assert_valid_task(task)

    def assert_post_invalid_task(self, new_task):
        response = self.client.post('/api/projects/' + self.valid_project_id() + '/', data=new_task, content_type='application/json')
        
        self.assertEquals(response.status_code, 400)

        error = response.json()

        self.assert_valid_error(error)


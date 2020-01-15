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

    def assert_put_valid_task(self, task):
        response = self.client.put('/api/projects/' + self.valid_project_id() + '/' + self.valid_task_id() + '/', data=task, content_type='application/json')
        
        self.assertEquals(response.status_code, 200)

        put_task = response.json()

        self.assert_valid_task(put_task)

        return put_task
    
    def assert_put_invalid_task(self, task):
        response = self.client.put('/api/projects/' + self.valid_project_id() + '/' + self.valid_task_id() + '/', data=task, content_type='application/json')
        
        self.assertEquals(response.status_code, 200)

        error = response.json()

        self.assert_valid_error(error)

        return error

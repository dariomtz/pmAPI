from .testing_library import AssertHelper

class ProjectTestingHelper(AssertHelper):

    def assert_post_valid_project(self, new_project):
        response = self.client.post('/api/projects/', data=new_project, content_type='application/json')

        self.assertEquals(response.status_code, 200)

        project = response.json()
        self.assert_valid_project(project)  
        
        return project

    def assert_post_invalid_project(self, new_project):
        response = self.client.post('/api/projects/', data=new_project, content_type='application/json')

        self.assertEquals(response.status_code, 400)

        error = response.json()
        self.assert_valid_error(error) 
        
        return error

    def assert_put_valid_project(self, project):
        response = self.client.put('/api/projects/' + self.valid_project_id() + '/', data=project, content_type='application/json')
    
        self.assertEquals(response.status_code, 200)

        put_project = response.json()

        self.assert_valid_project(put_project)

        return put_project

    def assert_put_invalid_project(self, project):
        response = self.client.put('/api/projects/' + self.valid_project_id() + '/', data=project, content_type='application/json')
    
        self.assertEquals(response.status_code, 400)

        error = response.json()

        self.assert_valid_error(error)

        return error

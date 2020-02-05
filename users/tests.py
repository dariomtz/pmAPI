from django.contrib.auth.models import User
from django.test import TestCase, Client


class TestUsers(TestCase):

    def assert_valid_user(self, user):
        self.assertIn('kind', user)
        self.assertEquals('user', user['kind'])
        
        self.assertIn('id', user)
        self.assertIn('username', user)
        self.assertIn('email', user)
        self.assertIn('first_name', user)
        self.assertIn('last_name', user)
        self.assertIn('created', user)

    def setUp(self):
        self.client = Client()
        self.username = 'dario'
        self.password = 'top_secret'
        self.user = User.objects.create_user(
            username=self.username, 
            first_name='Gustavo',
            last_name='Martinez',
            email='dario@iteso.mx',
            password=self.password)
        
        self.user.set_password(self.password)
        self.user.save()
        
    def test_get_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/api/users/')

        self.assertEquals(response.status_code, 200)
        self.assert_valid_user(response.json())

    def test_post_user(self):
        new_user = {
            'username': 'dariongo',
            'password': 'super_secure_password',
            'email': 'gusano@lol.com',
            'first_name': 'Dario',
            'last_name': 'Martinez'
        }

        response = self.client.post('/api/users/', data=new_user, content_type='application/json')

        self.assertEquals(response.status_code, 201)
        self.assert_valid_user(response.json())

    def test_put_user(self):
        self.client.login(username=self.username, password=self.password)

        new_user = {
            'username': 'dariongo',
            'email': 'gusano@lol.com',
            'first_name': 'Dario',
            'last_name': 'Martinez'
        }

        response = self.client.put('/api/users/', data=new_user, content_type='application/json')

        self.assertEquals(response.status_code, 200)
        self.assert_valid_user(response.json())

    def test_delete_user(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.delete('/api/users/')

        self.assertEquals(response.status_code, 204)

    def test_login(self):
        credentials = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post('/api/users/login/', data=credentials, content_type='application/json')

        self.assertEquals(response.status_code, 204)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get('/api/users/logout/')

        self.assertEquals(response.status_code, 204)
        self.assertNotIn('_auth_user_id', self.client.session)
    
    def test_put_password(self):
        new_password = 'newImprovedPW'

        self.client.login(username=self.username, password=self.password)

        credentials = {
            'username' : self.username,
            'old_password' : self.password,
            'password': new_password
        }

        response = self.client.put('/api/users/password/', data= credentials, content_type='application/json')

        self.assertEquals(response.status_code, 204)

        self.client.logout()

        self.client.login(username=self.username, password=new_password)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    

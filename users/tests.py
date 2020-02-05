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

    """ TODO: 
        Finish this test cases:

    
    def test_put_user(self):
    def test_delete_user(self):
    def test_login(self):
    def test_logout(self):
    def test_put_password(self):
        """
    

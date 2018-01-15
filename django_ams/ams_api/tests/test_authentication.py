from django.contrib.auth.models import User
from .base import BaseTestCase


class AuntenticationTestCase(BaseTestCase):

    def test_successful_signup(self):
        response = self.client.post('/users/', {
            'first_name': 'test',
            'last_name': 'test',
            'email': 'teste@test.com',
            'username': 'testtest',
            'password': 'password',
            'role': 'Student',
            'matric_number': '01057846',
            'faculty': 'test faculty',
            'department': 'test department'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(User.objects.count(), 2)
        self.assertIn('token', response.data)

    def test_email_already_exists(self):
        response = self.client.post('/users/', {
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@test.com',
            'username': 'test_user',
            'password': 'password',
            'role': 'Student',
            'matric_number': '01057846',
            'faculty': 'test faculty',
            'department': 'test department'
        })
        self.assertIn("A User with this email already exists", response.data['non_field_errors'])
        self.assertEqual(response.status_code, 400)

    def test_successful_login(self):
        response = self.client.post('/login/', {
            'username': 'test',
            'password': 'password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_nonexistent_user(self):
        response = self.client.post('/login/', {
            'username': 'random',
            'password': 'test',
        })
        self.assertEqual(response.status_code, 404)

    def test_successful_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 200)
            
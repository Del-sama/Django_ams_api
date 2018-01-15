import os

from django.test import override_settings
from django.conf import settings

from .base import BaseTestCase
from ..models import Assignment

class AssignmentTestCase(BaseTestCase):

    def test_create_assignment(self):
        self.first_file.seek(0)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post('/courses/{}/assignments/'.format(self.course.id), {
            'title':'Test',
            'due_date':'2018-12-12',
            'upload': self.first_file,
            'course_id': self.course.id,
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Assignment.objects.count(), 2)
    
    def test_get_assignments(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get('/assignments/')
        self.assertEqual(response.status_code, 200)
    
    def test_get_assignment_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get('/assignments/{}/'.format(self.assignment.id))
        self.assertEqual(response.status_code, 200)

    def test_update_assignment(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.put('/assignments/{}/'.format(self.assignment.id), {
            'title': 'updated assignment'
        })
        updated_assignment = Assignment.objects.get(id=self.assignment.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_assignment.title, "updated assignment")
    
    def test_delete_assignment(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete('/assignments/{}/'.format(self.assignment.id))
        self.assertEqual(response.status_code, 204)

    def test_assignment_submissions(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get('/assignments/{}/submissions/'.format(self.assignment.id))
        self.assertEqual(response.status_code, 200)
        
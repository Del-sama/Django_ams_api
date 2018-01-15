from .base import BaseTestCase
from ..models import Submission

class SubmissionsTestCase(BaseTestCase):
    
    def test_create_submission(self):
        self.first_file.seek(0)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post('/assignments/{}/submissions/'.format(self.assignment.id), {
            'upload': self.first_file,
            'assignment_id': self.assignment.id,
            'user_id': self.user.id
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Submission.objects.count(), 2)
    
    def test_get_submisions(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get('/submissions/')
        self.assertEqual(response.status_code, 200)
    
    def test_get_submission_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get('/submissions/{}/'.format(self.submission.id))
        self.assertEqual(response.status_code, 200)

    def test_update_submission(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.put('/submissions/{}/'.format(self.submission.id), {
            'grade': 50
        })
        updated_submission = Submission.objects.get(id=self.submission.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_submission.grade, '50')
    
    def test_delete_submission(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete('/submissions/{}/'.format(self.submission.id))
        self.assertEqual(response.status_code, 204)
        
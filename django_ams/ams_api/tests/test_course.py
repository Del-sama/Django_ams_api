from .base import BaseTestCase
from ..models import Course

class CourseTestCase(BaseTestCase):

    def test_successfully_create_course(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post('/courses/', {
            'course_title': 'testtest',
            'course_code': 'test 325',
            'units': 3
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Course.objects.count(), 2)
    
    def test_get_courses(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 200)
    
    def test_get_course_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get('/courses/{}/'.format(self.course.id))
        self.assertEqual(response.status_code, 200)

    def test_update_course(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.put('/courses/{}/'.format(self.course.id), {
            'course_title': 'updated test'
        })
        updated_course = Course.objects.get(id=self.course.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_course.course_title, "updated test")
    
    def test_delete_course(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete('/courses/{}/'.format(self.course.id))
        self.assertEqual(response.status_code, 204)

    def test_course_assignments(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get('/courses/{}/assignments/'.format(self.course.id))
        self.assertEqual(response.status_code, 200)
        
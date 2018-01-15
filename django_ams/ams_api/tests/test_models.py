from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Course, Profile, Assignment, Submission
from .base import BaseTestCase

class ModelTestCase(BaseTestCase):

    def tearDown(self):
        User.objects.all().delete()
        Course.objects.all().delete()
        Assignment.objects.all().delete()
        Submission.objects.all().delete()

    def test_user_is_created(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.email, "test@test.com")

    def test_profile_is_created_alongside_user(self):
        self.assertTrue(hasattr(self.user, 'profile'), True)
        self.user.profile.role = 'Lecturer'
        self.assertEqual(self.user.profile.role, 'Lecturer')

    def test_assignment_is_created(self):
        self.assertEqual(Assignment.objects.count(), 1)
        self.assertEqual(self.assignment.title, "Test")

    def test_submission_is_created(self):
        self.assertEqual(Submission.objects.count(), 1)

    def test_course_is_created(self):
        self.assertEqual(Course.objects.count(), 1)

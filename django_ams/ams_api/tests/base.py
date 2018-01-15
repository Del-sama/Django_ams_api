import os
import shutil

from django.test import override_settings
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from ..models import Course, Profile, Assignment, Submission

class BaseTestCase(TestCase):
    
    TEST_MEDIA_ROOT=os.path.join(settings.BASE_DIR, 'test_uploads')
    @override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
    def setUp(self):
        self.client = APIClient()

        self.first_file = SimpleUploadedFile("file.txt", b"file content")

        self.user = User.objects.create_user(
            first_name="test",
            last_name="test",
            username="test", 
            email="test@test.com",
            password="password"
        )


        self.login = self.client.post('/login/', {
            'username': 'test',
            'password': 'password',
        })

        self.token = "Bearer {}".format(self.login.data['token'])
        self.course = Course.objects.create(
            course_code="Test 111",
            course_title="Test course",
            units=3
            )

        self.assignment = Assignment.objects.create(
            title="Test",
            due_date="2018-12-12",
            upload=self.first_file,
            course_id=self.course.id,
            user_id=self.user.id
        )

        self.submission = Submission.objects.create(
            upload=self.first_file,
            user_id=self.user.id,
            assignment_id=self.assignment.id,
        )

    def tearDown(self):
        User.objects.all().delete()
        Course.objects.all().delete()
        Assignment.objects.all().delete()
        Submission.objects.all().delete()
        # delete test upload folder
        shutil.rmtree(self.TEST_MEDIA_ROOT)

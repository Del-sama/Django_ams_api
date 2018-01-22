import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Course(models.Model):
    course_code = models.CharField(max_length=100, unique=True)
    course_title = models.CharField(max_length=100, unique=True)
    units = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)


class Profile(models.Model):
    LECTURER = 'LR'
    STUDENT = 'ST'
    role_choice = ((LECTURER , 'Lecturer'), (STUDENT, 'Student'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=role_choice, default='Lecturer')
    faculty = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    matric_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    courses = models.ManyToManyField(Course,
        related_name='profiles',
        blank=True,
        null=True
        )

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    upload = models.FileField(upload_to='assignments/')
    due_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assignments'
    )


class Submission(models.Model):
    upload = models.FileField(upload_to='submissions/')
    submitted_at = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    assignment = models.ForeignKey(
        'Assignment',
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    grade = models.CharField(max_length=100, null=True, blank=True, default=0)
    feedback = models.CharField(max_length=255, null=True, blank=True, default="No feedback yet")

class Blacklist(models.Model):
    token = models.CharField(null=True, blank=True, max_length=255)
    
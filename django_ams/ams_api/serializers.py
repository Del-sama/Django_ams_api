from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Profile, Course, Assignment, Submission

class UserSerializer(serializers.ModelSerializer):

    def validate(self, data):
        email = data['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A User with this email already exists")
        return data

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name','username', 'email', 'password')
        write_only_field = ('password')


class LoginSerializer(serializers.Serializer):
    
    username = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length=100)

    
class CourseSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        
        instance.course_code = validated_data.get('course_code', instance.course_code)
        instance.course_title = validated_data.get('course_title', instance.course_title)
        instance.units = validated_data.get('units', instance.units)
        instance.save()
        return instance

    class Meta:
        model = Course
        fields = ('id', 'course_code', 'course_title','units')

class CourseAssignmentsSerializer(serializers.Serializer):
    
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    course_id = serializers.IntegerField()
    title = serializers.CharField(max_length=250)
    upload = serializers.FileField()
    due_date = serializers.DateField()
    created_at = serializers.DateField()
    last_updated = serializers.DateField()


class ProfileSerializer(serializers.ModelSerializer):
    
    courses = CourseSerializer(many=True, required=False)
    matric_number = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        role = data['role']

        if role == 'ST' and 'matric_number' not in data:
            raise serializers.ValidationError("Matric number is required")
        if role == 'LR' and 'matric_number'in data:
            raise serializers.ValidationError("Matric number not required")
        return data

    class Meta:
        model = Profile
        fields = ('id', 'user_id', 'role','faculty', 'department', 'matric_number', 'courses')


class AssignmentSerializer(serializers.ModelSerializer):
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.upload = validated_data.get('upload', instance.upload)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.save()
        return instance

    class Meta:
        model = Assignment
        fields = ('id', 'user_id', 'course_id', 'title', 'upload', 'due_date', 'created_at', 'last_updated')


class SubmissionSerializer(serializers.ModelSerializer):
    
    def update(self, instance, validated_data):
        instance.grade = validated_data.get('grade', instance.grade)
        instance.upload = validated_data.get('upload', instance.upload)
        instance.feedback = validated_data.get('feedback', instance.feedback)
        instance.save()
        return instance

    class Meta:
        model = Submission
        fields = ('id', 'user_id', 'upload', 'submitted_at', 'last_updated', 'assignment_id', 'grade', 'feedback')

class AssignmentSubmissionsSerializer(serializers.Serializer):
    
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    assignment_id = serializers.IntegerField()
    grade = serializers.IntegerField()
    feedback = serializers.CharField(max_length=250)
    upload = serializers.FileField()
    submitted_at = serializers.DateField()
    last_updated = serializers.DateField()

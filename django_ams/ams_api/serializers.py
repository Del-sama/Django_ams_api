from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Profile, Course, Assignment, Submission

class UserSerializer(serializers.ModelSerializer):

    def validate(self, data):
        email = data['email']
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A User with this email already exists")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                username=validated_data['username'], 
                email=validated_data['email'],
                password=validated_data['password']
                )
        return user

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name','username', 'email', 'password')
        write_only_field = ('password')


class LoginSerializer(serializers.Serializer):
    
    username = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length=100)

    
class CourseSerializer(serializers.ModelSerializer):
    
    def create(self, validated_data):
    
        return Course.objects.create(**validated_data)

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

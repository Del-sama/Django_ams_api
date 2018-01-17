from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ..serializers import CourseSerializer, CourseAssignmentsSerializer, AssignmentSerializer
from ..models import Course, Assignment
from .helpers import check_logout


class CourseView(APIView):
    permission_classes = (IsAuthenticated, )
    @check_logout
    def post(self, request):
        course_serializer=CourseSerializer(data=request.data)
        if course_serializer.is_valid():
            course = Course.objects.create(
                course_title=course_serializer.data['course_title'],
                course_code=course_serializer.data['course_code'],
                units=course_serializer.data['units']
            )
            return Response(course_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(course_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_logout
    def get(self, request):
        import pdb; pdb.set_trace()
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class CourseDetail(APIView):
    permission_classes = (IsAuthenticated, )
    @check_logout
    def get_object(self, id):
        try:
            return Course.objects.get(id=id)
        except Course.DoesNotExist:
            raise Http404

    @check_logout
    def get(self, request, id):
        course = self.get_object(id)
        serializer = CourseSerializer(course)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @check_logout
    def put(self, request, id):
        course = self.get_object(id)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_logout
    def delete(self, request, id):
        course = self.get_object(id)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseAssignments(APIView):
    permission_classes = (IsAuthenticated, )

    @check_logout
    def get_object(self, id):
        try:
            return Course.objects.get(id=id)
        except Course.DoesNotExist:
            raise Http404

    @check_logout
    def post(self, request, id):
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            Assignment.objects.create(
                title=serializer.data["title"],
                upload=serializer.data["upload"],
                due_date=serializer.data["due_date"],
                course_id=id,
                user_id=request.user.id
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @check_logout
    def get(self, request, id):
        course = self.get_object(id)
        assignments = course.assignments.all()

        serializer = CourseAssignmentsSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers import CourseSerializer, CourseAssignmentsSerializer
from ..models import Course


class CourseView(APIView):

    def post(self, request):
        course_serializer=CourseSerializer(data=request.data)
        if course_serializer.is_valid():
            course = course_serializer.save()
            import pdb; pdb.set_trace()
            return Response(course_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(course_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class CourseDetail(APIView):
    
    def get_object(self, id):
        try:
            return Course.objects.get(id=id)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, id):
        course = self.get_object(id)
        serializer = CourseSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        course = self.get_object(id)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        course = self.get_object(id)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseAssignments(APIView):

    def get_object(self, id):
        try:
            return Course.objects.get(id=id)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, id):
        course = self.get_object(id)
        assignments = course.assignments.all()

        serializer = CourseAssignmentsSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
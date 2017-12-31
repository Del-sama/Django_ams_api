from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers import AssignmentSerializer, AssignmentSubmissionsSerializer
from ..models import Assignment


class AssignmentView(APIView):

    def get(self, response):
        assignments = Assignment.objects.all()
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AssignmentDetail(APIView):
    
    def get_object(self, id):
        try:
            return Assignment.objects.get(id=id)
        except Assignment.DoesNotExist:
            raise Http404

    def get(self, request, id):
        assignment = self.get_object(id)
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        assignment = self.get_object(id)
        serializer = AssignmentSerializer(assignment, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        assignment = self.get_object(id)
        assignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AssignmentSubmissions(APIView):
    
    def get_object(self, id):
        try:
            return Assignment.objects.get(id=id)
        except Assignment.DoesNotExist:
            raise Http404

    def get(self, request, id):
        assignment = self.get_object(id)
        submissions = assignment.submissions.all()

        serializer = AssignmentSubmissionsSerializer(submissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
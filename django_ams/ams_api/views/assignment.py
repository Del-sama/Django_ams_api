from __future__ import unicode_literals

from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication

from ..serializers import AssignmentSerializer, AssignmentSubmissionsSerializer, SubmissionSerializer
from ..models import Assignment, Submission


class AssignmentView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
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

    def post(self, request, id):
        serializer = SubmissionSerializer(data=request.data)
        if serializer.is_valid():
            Submission.objects.create(
                upload=serializer.data["upload"],
                assignment_id=id,
                user_id=request.user.id
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id):
        assignment = self.get_object(id)
        submissions = assignment.submissions.all()

        serializer = AssignmentSubmissionsSerializer(submissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserAssignments(APIView):

    def get(self, request, id):
        assignments = Assignment.objects.filter(user_id=id)
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
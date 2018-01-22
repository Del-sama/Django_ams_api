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
from .helpers import check_logout


class AssignmentView(APIView):
    permission_classes = (IsAuthenticated, )

    @check_logout
    def get(self, request):
        assignments = Assignment.objects.all()
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AssignmentDetail(APIView):
    
    @check_logout
    def get_object(self, id):
        try:
            return Assignment.objects.get(id=id)
        except Assignment.DoesNotExist:
            raise Http404

    @check_logout
    def get(self, request, id):
        assignment = self.get_object(id)
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @check_logout
    def put(self, request, id):
        user_id = request.user.id
        assignment = self.get_object(id)

        if user_id == assignment.user_id:
            serializer = AssignmentSerializer(assignment, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'message': 'You are not authorized to carry out this operation'},
                status=status.HTTP_401_UNAUTHORIZED
                )

    @check_logout
    def delete(self, request, id):
        user_id = request.user.id
        assignment = self.get_object(id)
        if user_id == assignment.user_id:
            assignment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'message': 'You are not authorized to carry out this operation'},
                status=status.HTTP_401_UNAUTHORIZED
                )

class AssignmentSubmissions(APIView):
            
    @check_logout
    def get_object(self, id):
        try:
            return Assignment.objects.get(id=id)
        except Assignment.DoesNotExist:
            raise Http404

    @check_logout
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

    @check_logout
    def get(self, request, id):
        user_id = request.user.id
        assignment = self.get_object(id)
        submissions = assignment.submissions.all()

        if user_id == assignment.user_id:
            serializer = AssignmentSubmissionsSerializer(submissions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'message': 'You are not authorized to carry out this operation'},
                status=status.HTTP_401_UNAUTHORIZED
                )

class UserAssignments(APIView):

    @check_logout
    def get(self, request, id):
        assignments = Assignment.objects.filter(user_id=id)
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
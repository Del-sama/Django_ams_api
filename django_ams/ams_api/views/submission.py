from __future__ import unicode_literals

import datetime

from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers import SubmissionSerializer
from ..models import Submission
from .helpers import check_logout


class SubmissionView(APIView):

    @check_logout
    def get(self, response):
        submissions = Submission.objects.all()
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubmissionDetail(APIView):
    
    @check_logout
    def get_object(self, id):
        try:
            return Submission.objects.get(id=id)
        except Submission.DoesNotExist:
            raise Http404

    @check_logout
    def get(self, request, id):
        submission = self.get_object(id)
        serializer = SubmissionSerializer(submission)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @check_logout
    def put(self, request, id):
        user_id = request.user.id
        submission = self.get_object(id)
        assignment = submission.assignment
        if user_id == submission.user_id:
            serializer = SubmissionSerializer(submission, data=request.data, partial=True)
            
            if serializer.is_valid():
                if assignment.due_date >= datetime.date.today():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": "The due date for this assignment has passed"
                        }, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'message': 'You are not authorized to carry out this operation'},
                status=status.HTTP_401_UNAUTHORIZED
                )

    @check_logout
    def delete(self, request, id):
        user_id = request.user.id
        submission = self.get_object(id)
        if user_id == submission.user_id:
            submission.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'message': 'You are not authorized to carry out this operation'},
                status=status.HTTP_401_UNAUTHORIZED
                )

class UserSubmissions(APIView):
    
    @check_logout
    def get(self, request, id):
        submissions = Submission.objects.filter(user_id=id)
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

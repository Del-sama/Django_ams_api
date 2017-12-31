from __future__ import unicode_literals

import datetime

from django.shortcuts import render
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers import SubmissionSerializer
from ..models import Submission


class SubmissionView(APIView):

    def get(self, response):
        submissions = Submission.objects.all()
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubmissionDetail(APIView):
    
    def get_object(self, id):
        try:
            return Submission.objects.get(id=id)
        except Submission.DoesNotExist:
            raise Http404

    def get(self, request, id):
        submission = self.get_object(id)
        serializer = SubmissionSerializer(submission)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        submission = self.get_object(id)
        assignment = submission.assignment
        serializer = AssignmentSerializer(assignment, data=request.data, partial=True)
        
        if serializer.is_valid():
            if assignment.due_date >= datetime.date.today():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({
                    "message": "The due date for this assignment has passed"
                    }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        submission = self.get_object(id)
        submission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

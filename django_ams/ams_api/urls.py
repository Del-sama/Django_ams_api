from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from .views.authentication import RegisterUsers, LoginUsers, LogoutUsers
from .views.course import CourseView, CourseDetail, CourseAssignments
from .views.assignment import (
    AssignmentView, AssignmentDetail, AssignmentSubmissions, UserAssignments)
from .views.submission import SubmissionView, SubmissionDetail, UserSubmissions

urlpatterns = [
    url(r'^users/$', RegisterUsers.as_view(), name="register_user"),
    url(r'^login/$', LoginUsers.as_view(), name="login_user"),
    url(r'^logout/$', LogoutUsers.as_view(), name="logout"),
    url(r'^courses/$', CourseView.as_view()),
    url(r'^courses/(?P<id>[-\w]+)/$', CourseDetail.as_view()),
    url(r'^courses/(?P<id>[-\w]+)/assignments/$', CourseAssignments.as_view()),
    url(r'^assignments/$', AssignmentView.as_view()),
    url(r'^assignments/(?P<id>[-\w]+)/$', AssignmentDetail.as_view()),
    url(r'^assignments/(?P<id>[-\w]+)/submissions/$', AssignmentSubmissions.as_view()),
    url(r'^submissions/$', SubmissionView.as_view()),
    url(r'^submissions/(?P<id>[-\w]+)/$', SubmissionDetail.as_view()),
    url(r'^users/(?P<id>[-\w]+)/assignments/$', UserAssignments.as_view()),
    url(r'^users/(?P<id>[-\w]+)/submissions/$', UserSubmissions.as_view()),
]
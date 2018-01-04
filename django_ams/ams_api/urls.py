from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from .views.authentication import RegisterUsers, LoginUsers, LogoutUsers
from .views.course import CourseView, CourseDetail, CourseAssignments
from .views.assignment import (
    AssignmentView, AssignmentDetail, AssignmentSubmissions, UserAssignments)
from .views.submission import SubmissionView, SubmissionDetail, UserSubmissions

urlpatterns = [
    url(r'^users/$', csrf_exempt(RegisterUsers.as_view()), name="register_user"),
    url(r'^login/$', csrf_exempt(LoginUsers.as_view()), name="login_user"),
    url(r'^logout/$', csrf_exempt(LogoutUsers.as_view()), name="logout"),
    url(r'^courses/$', csrf_exempt(CourseView.as_view())),
    url(r'^courses/(?P<id>[-\w]+)/$', csrf_exempt(CourseDetail.as_view())),
    url(r'^courses/(?P<id>[-\w]+)/assignments/$', csrf_exempt(CourseAssignments.as_view())),
    url(r'^assignments/$', csrf_exempt(AssignmentView.as_view())),
    url(r'^assignments/(?P<id>[-\w]+)/$', csrf_exempt(AssignmentDetail.as_view())),
    url(r'^assignments/(?P<id>[-\w]+)/submissions/$', csrf_exempt(AssignmentSubmissions.as_view())),
    url(r'^submissions/$', csrf_exempt(SubmissionView.as_view())),
    url(r'^submissions/(?P<id>[-\w]+)/$', csrf_exempt(SubmissionDetail.as_view())),
    url(r'^users/(?P<id>[-\w]+)/assignments/$', csrf_exempt(UserAssignments.as_view())),
    url(r'^users/(?P<id>[-\w]+)/submissions/$', csrf_exempt(UserSubmissions.as_view())),
]
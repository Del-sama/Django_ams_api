from functools import wraps

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from ..models import Blacklist

def check_logout(f):
    @wraps(f)
    def decorated(request, *args, **kwargs):
        token = request.request.auth.decode()
        if len(Blacklist.objects.filter(token=token)) > 0:
           return Response({
                "message": "User is logged out"
            }, status=status.HTTP_400_BAD_REQUEST)
        return f(request, *args, **kwargs)
    return decorated
        
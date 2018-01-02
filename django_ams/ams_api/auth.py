from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication

def validate_token(request):
    return BaseJSONWebTokenAuthentication.authenticate(request)
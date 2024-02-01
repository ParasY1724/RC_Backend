from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.contrib.auth.models import User

class JWTAuthentication(BasePermission):
    def has_permission(self, request,*args, **kwargss):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Authentication credentials were not provided.")

        try:
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
            username = payload['username']
            user = User.objects.get(username=username)
            request.user = user
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")
        except User.DoesNotExist:
            raise AuthenticationFailed("User does not exist")

        return True
    
    


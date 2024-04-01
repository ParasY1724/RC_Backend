from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
import jwt
from .models import Team

class JWTAuthentication(BasePermission):
    def has_permission(self, request,*args, **kwargss):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Authentication credentials were not provided.")

        try:
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
            teamname = payload['teamname']
            team = Team.objects.get(teamname=teamname)
            request.team = team
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")
        except Team.DoesNotExist:
            raise AuthenticationFailed("Team does not exist")
        return True
    
    


from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
import jwt
from .models import Team

class JWTAuthentication(BasePermission):
    def has_permission(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            # raise AuthenticationFailed("Authentication credentials were not provided.")
            return False
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
    
    #Question.objects.create( question_id=i,question_text='1+1=?',correct_answer=2,responses={"1" : 10 , "5": 12 ,"3" : 3})

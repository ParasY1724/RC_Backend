from rest_framework import generics, status,views
from rest_framework.response import Response
from django.db.models import Q
from .models import Team, Progress,Question
from .serializers import TeamSerializer, UserSerializer, QuestionSerializer,ProgressSerializer
from django.contrib.auth.models import User
import jwt,datetime,random
from rest_framework.exceptions import AuthenticationFailed
from .permissions import JWTAuthentication
from django.shortcuts import  redirect,render



class CreateTeamView(generics.CreateAPIView):
    serializer_class = TeamSerializer

class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        team_name = request.data.get('team')
        team = None
        user = self.get_queryset().filter(username=username).first()
        try :
            team = Team.objects.get(teamname= team_name )
         
            if team.login_status :
                raise AuthenticationFailed('Another User is Logged-In !!')
            else :
                team.login_status = True
                team.save()
        except Team.DoesNotExist :
            raise AuthenticationFailed('No such Team found.')

        if user is None or not user.check_password(password):
            raise AuthenticationFailed('Invalid username or password')
        
        payload ={
            'username' : username ,
            'team' : team_name,
            'exp' : datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.utcnow(),
        }
        #Generating Token and storing in COOKIE
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}
        return response


class GetQuestionView(generics.ListCreateAPIView):
    queryset = Question.objects.none()
    permission_classes = [JWTAuthentication]
    serializer_class = QuestionSerializer

    def get(self, request): 
        try:
            team = Team.objects.get(Q(user1=request.user) | Q(user2=request.user))
        except Team.DoesNotExist:
            return Response({"error": "Team not found for the authenticated user"}, status=status.HTTP_404_NOT_FOUND)

        progress, created = Progress.objects.get_or_create(team=team)

        if  created or not progress.question_list :
            q_list = str(random.sample(range(1,6),5) + random.sample(range(6,11),5)).strip("[]")
            progress.question_list = q_list
            progress.save()
        if (progress.current_question == 10) :
            return Response({"message": "Questions are over"}, status=status.HTTP_404_NOT_FOUND)

        questions_data = (progress.question_list).split(',')
        que_id = questions_data[progress.current_question-1]
        question = Question.objects.get(question_id = que_id)
        
        context = {
            "Current_Question" : progress.current_question,
            "question" : question.question_text,
            "team" : progress.team,
            "attempts" : 2 - progress.isAttemptedFirst
        }
        return render(request, 'question.html', context)

    
    def post(self,request):
        answer = request.data.get("answer")
        team  = request.data.get("team")
        try:
            team = Team.objects.get(Q(user1=request.user) | Q(user2=request.user))
            progress = Progress.objects.get(team=team)
        except Team.DoesNotExist:
            return Response({"error": "Team not found for the authenticated user"}, status=status.HTTP_404_NOT_FOUND)
        except Progress.DoesNotExist :
            return Response({"error": "Team not found for the authenticated user"}, status=status.HTTP_404_NOT_FOUND)

        questions_data = (progress.question_list).split(',')
        que_id = questions_data[progress.current_question-1]
        question = Question.objects.get(question_id = que_id)

        if (int(answer) == question.correct_answer):
            progress.score +=1
            progress.current_question+=1
            progress.isAttemptedFirst = False
        else :
            if ( not progress.isAttemptedFirst):
                progress.isAttemptedFirst = True
            else:
                progress.isAttemptedFirst = False
                progress.current_question+=1
        progress.save()

        return redirect('get_question')
        

class LeaderboardView(generics.ListAPIView):
    queryset = Progress.objects.all().order_by('-score')
    serializer_class = ProgressSerializer
    permission_classes = [JWTAuthentication]


class LogoutView(views.APIView):
    def get(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Authentication credentials were not provided.")
        team = None
        try:
            payload = jwt.decode(token, 'secret', algorithms=["HS256"])
            team_name = payload['team']
            team = Team.objects.get(teamname= team_name)
            team.login_status = False
            team.save()
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")
        except Team.DoesNotExist:
            raise AuthenticationFailed("User does not exist")
        

        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message' : 'Logged Out!',
        }
        return response
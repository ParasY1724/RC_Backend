from rest_framework import generics, status,views
from rest_framework.response import Response
from .models import Team, Progress,Question
from .serializers import TeamSerializer, QuestionSerializer,ProgressSerializer,CreateTeamSerializer
import jwt,datetime,random
from rest_framework.exceptions import AuthenticationFailed
from .permissions import JWTAuthentication
from django.shortcuts import  redirect,render
from django.utils import timezone
from . import MarkingScheme,Timer,lifelines
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse




class CreateTeamView(generics.CreateAPIView):
    serializer_class = CreateTeamSerializer


class LoginView(generics.CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def post(self, request):
        teamname = request.data.get('teamname')
        password = request.data.get('password')
        try:
            team = Team.objects.get(teamname=teamname)
        except Team.DoesNotExist:
            raise AuthenticationFailed('Invalid teamname or password')
        
        if not check_password(password, team.password) :
            raise AuthenticationFailed('Invalid teamname or password')
        
        if team.login_status:
            raise AuthenticationFailed('Another user is logged in with this team')

        team.login_status = True
        team.save()

        payload = {
            'teamname': teamname,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {'jwt': token}
        return response
    
    def get(self,request):
        if(JWTAuthentication.has_permission(self,request)):
           return redirect('get_question')
        

class GetQuestionView(generics.ListCreateAPIView):
    queryset = Question.objects.none()
    permission_classes = [JWTAuthentication]
    serializer_class = QuestionSerializer

    def get(self, request):
        team = request.team
        progress, created = Progress.objects.get_or_create(team=team)

        if created or not progress.question_list:
            if team.category == 'JR':
                q_list = str(random.sample(range(1, 6), 5) + random.sample(range(6, 11), 5)).strip("[]")
            else:
                q_list = str(random.sample(range(11, 16), 5) + random.sample(range(16, 21), 5)).strip("[]")

            progress.question_list = q_list
            progress.start_time = timezone.now()
            progress.end_time = timezone.now() + timezone.timedelta(hours=2)
            progress.save()

        if progress.current_question == 10:
            return Response({"message": "Questions are over"}, status=status.HTTP_404_NOT_FOUND)

        questions_data = progress.question_list.split(',')
        que_id = questions_data[progress.current_question - 1]
        question = Question.objects.get(question_id=que_id)

        time_remaining = (progress.end_time - timezone.now())
        time_data = Timer.Timer(time_remaining)

        context = {
            "Current_Question" : progress.current_question,
            "question" : question.question_text,
            "attempts" : 2 - progress.isAttemptedFirst,
            "prev_ans" : progress.prev_answer,
            "score" : progress.score,
            "lifeline_flag" : progress.lifeline_flag,
            "lifeline1" : progress.lifeline1,
            "lifeline2" : progress.lifeline2,
            "lifeline3" : progress.lifeline3,
        }

        context.update(time_data)

        # return render(request, 'question.html', context)
        return Response(context)

    
    def post(self,request):
        answer = request.data.get("answer")
        answer = int(answer)
        team  = request.team
        try:
            progress = Progress.objects.get(team=team)
        except Progress.DoesNotExist :
            return Response({"error": "Team not found for the authenticated user"}, status=status.HTTP_404_NOT_FOUND)

        questions_data = (progress.question_list).split(',')
        que_id = questions_data[progress.current_question-1]
        question = Question.objects.get(question_id = que_id)

        if (answer == question.correct_answer):
            MarkingScheme.evaluate_postive(progress)
        else :
            MarkingScheme.evaluate_negative(progress,answer)
        lifelines.save_response(question,answer)
        lifelines.reset_lifelines(progress) 
        progress.save()
        return redirect('get_question')
        

class LeaderboardView(generics.ListAPIView):
    queryset = Progress.objects.all().order_by('-score')
    serializer_class = ProgressSerializer
    permission_classes = [JWTAuthentication]


class LogoutView(views.APIView):
    permission_classes = [JWTAuthentication]
    def get(self,request):
        team = request.team
        team.login_status = False
        team.save()
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message' : 'Logged Out!',
        }
        return response
    

class ResultView(generics.ListAPIView):
    permission_classes = [JWTAuthentication]
    def get(self,request):
        team = request.team
        try:
            progress = Progress.objects.get(team = team)
            return Response({"Score" : progress.score  })
        except Progress.DoesNotExist:
            raise AuthenticationFailed("Progress does not exist")
           
 

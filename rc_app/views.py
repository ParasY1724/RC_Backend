from rest_framework import generics, status,views
from rest_framework.response import Response
from .models import Team, Progress,Question
from .serializers import TeamSerializer, QuestionSerializer,ProgressSerializer,CreateTeamSerializer
import jwt,datetime,random
from rest_framework.exceptions import AuthenticationFailed
from .permissions import JWTAuthentication
from rest_framework.permissions import IsAdminUser
from django.shortcuts import  redirect,render
from django.utils import timezone
from . import MarkingScheme,Timer,lifelines
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from sys import maxsize
from django.contrib.auth.hashers import make_password
import requests

class CreateTeamView(generics.CreateAPIView):
    serializer_class = CreateTeamSerializer
    # permission_classes = [IsAdminUser]

# class LoginView(generics.CreateAPIView):
#     queryset = Team.objects.all()
#     serializer_class = TeamSerializer

#     def post(self, request):
#         teamname = request.data.get('teamname')
#         password = request.data.get('password')
#         try:
#             team = Team.objects.get(teamname=teamname)
#         except Team.DoesNotExist:
#             hashed_password = make_password(password)
#             team = Team.objects.create(teamname = teamname , password = hashed_password,user1 = request.data.get('user1'),user2 = request.data.get('user2'),category=request.data.get('category'))
            
        
#         if not check_password(password, team.password) :
#             raise AuthenticationFailed('Invalid teamname or password')
        
#         if team.login_status:
#             raise AuthenticationFailed('User is already logged in')

#         team.login_status = True
#         team.save()

#         payload = {
#             'teamname': teamname,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
#             'iat': datetime.datetime.utcnow(),
#         }

#         token = jwt.encode(payload, 'secret', algorithm='HS256')
#         return Response({'jwt': token}, status=status.HTTP_201_CREATED)


class LoginView(generics.CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def post(self, request):
        teamname = request.data.get('teamname')
        password = request.data.get('password')
        try:
            team = Team.objects.get(teamname=teamname)


            if not check_password(password, team.password) :
             raise AuthenticationFailed('Invalid teamname or password')
        
            if team.login_status:
                raise AuthenticationFailed('User is already logged in')
        except Team.DoesNotExist:
            url = 'https://admin.credenz.in/api/verify/user/'
            # url = "http://127.0.0.1:8001/api/verify/user/"
            headers= {'Content-Type':'application/json'}
            
            data={
                'username':teamname,
                'password':password,
                'event':"RC",
                'is_team':'false'
            }

            if request.data.get('is_team'):
                data['is_team'] = 'true'
            
            response =  requests.post(url,headers=headers,json=data)
            print(response)

            if response.status_code == 200:
                        response = response.json()
                        username_two = ''
                        if not (request.data.get('is_team')):
                            try:
                                isSenior = response['user']['senior']
                                if(isSenior):
                                    isSenior = "SR"
                                else:
                                    isSenior = "JR"
                                username_one = response['user']['username']
                            except Exception as e:
                                return Response({"message": "Bad Credentials"}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            isSenior = response['users'][0]['senior']
                            username_one = response['users'][0]['username']
                            username_two = response['users'][1]['username']
                        try:
                            serializer  = serializer = CreateTeamSerializer(data={
                                                            'teamname': teamname,
                                                            'password': password,
                                                            'category': isSenior,
                                                            'user1': username_one,
                                                            'user2': username_two
                                                        })
                            serializer.is_valid()
                            serializer.save()
                            team = serializer.instance
                        except Exception as e:
                            return Response({"message": "User not Found"}, status=status.HTTP_404_NOT_FOUND)
            else:  
                return Response({"message": "Bad Credentials"}, status=status.HTTP_404_NOT_FOUND)
    

        team.login_status = True
        team.save()

        payload = {
            'teamname': teamname,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return Response({'jwt': token}, status=status.HTTP_201_CREATED)


    
        

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

        if progress.current_question > 10:
            return Response({"message": "Questions are over"}, status=status.HTTP_204_NO_CONTENT)

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
        if(answer > maxsize or answer < (-1 * maxsize)-1):
            return Response({"error":"Integer Overflow"},status=status.HTTP_406_NOT_ACCEPTABLE)
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

    def get(self,request):
        if(JWTAuthentication.has_permission(self,request)):
            team_set = self.queryset.filter(team__category=request.team.category)
        else:
            category = request.query_params.get('category',default = "NONE")
            if category :
                team_set = self.queryset.filter(team__category=category)
            else :
                return Response({"message": "Invalid URL"}, status=status.HTTP_400_BAD_REQUEST)
            
        serialized_data = self.serializer_class(team_set, many=True).data
        return Response(serialized_data)

class LogoutView(views.APIView):
    permission_classes = [JWTAuthentication]
    def get(self,request):
        team = request.team
        team.login_status = False
        team.save()
        response = Response()
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
            rank = list(Progress.objects.all().order_by('-score').filter(team__category=team.category)).index(progress)


            return Response({"teamname" : team.teamname,
                             "score" : progress.score ,
                             "correct_submission" : progress.correct_count ,
                             "incorrect_submission" : progress.incorrect_count,
                             "question_attempted" : progress.current_question - 1,
                             "rank" : rank+1,
                             "lifelines_used" : progress.lifeline1 + progress.lifeline2 + progress.lifeline3,           
                              })
        except Progress.DoesNotExist:
            raise AuthenticationFailed("Progress does not exist")
        

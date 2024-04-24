from rest_framework import serializers
from .models import Question,Progress,Team
from django.contrib.auth.hashers import make_password


class QuestionSerializer(serializers.ModelSerializer):
    correct_answer = serializers.IntegerField(write_only = True)
    class Meta:
        model = Question
        fields = ['question_id', 'question_text', 'correct_answer'] 

class ProgressSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.teamname', read_only=True)
    start_time = serializers.DateTimeField(write_only = True)
    end_time = serializers.DateTimeField(write_only = True)
    question_list = serializers.CharField(write_only = True)
    prev_answer = serializers.IntegerField(write_only = True)
    isAttemptedFirst = serializers.BooleanField(write_only = True)
    class Meta:
        model = Progress
        fields = ["team_name", "score", "start_time", "end_time", "current_question", "question_list", "prev_answer" ,"isAttemptedFirst","incorrect_count","correct_count"]
    
class CreateTeamSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    login_status = serializers.BooleanField(read_only=True)
    
    class Meta: 
        model = Team
        fields = ['teamname', 'password', 'category','user1' ,'user2','login_status']
    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        team = Team.objects.create(password=hashed_password,**validated_data)
        return team
    
class TeamSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    login_status = serializers.BooleanField(read_only=True)
    category = serializers.CharField(read_only=True)

    class Meta: 
        model = Team
        fields = ['teamname', 'password', 'category', 'login_status']
   
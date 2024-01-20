from rest_framework import serializers
from .models import Question,Progress,Team
from django.contrib.auth.models import User




class QuestionSerializer(serializers.ModelSerializer):
    correct_answer = serializers.IntegerField(write_only = True)
    class Meta:
        model = Question
        fields = ['question_id', 'question_text', 'correct_answer', 'category', 'level']

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        fields = [ "team" , "score" , "start_time" , "end_time" , "current_questions" ,"isAttemptedFirst" ,"isAttemptedSecond" ]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

     

class TeamSerializer(serializers.ModelSerializer):
    user1 = UserSerializer()
    user2 = UserSerializer()

    class Meta: 
        model = Team
        fields = ['teamname', 'user1', 'user2','category']
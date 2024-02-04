from rest_framework import serializers
from .models import Question,Progress,Team
from django.contrib.auth.models import User


class QuestionSerializer(serializers.ModelSerializer):
    correct_answer = serializers.IntegerField(write_only = True)
    class Meta:
        model = Question
        fields = ['question_id', 'question_text', 'correct_answer', 'category']

class ProgressSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.teamname', read_only=True)
    start_time = serializers.DateTimeField(write_only = True)
    end_time = serializers.DateTimeField(write_only = True)
    current_question = serializers.IntegerField(write_only = True)
    question_list = serializers.CharField(write_only = True)
    prev_answer = serializers.IntegerField(write_only = True)
    isAttemptedFirst = serializers.BooleanField(write_only = True)
    class Meta:
        model = Progress
        fields = ["team_name", "score", "start_time", "end_time", "current_question", "question_list", "prev_answer" ,"isAttemptedFirst"]
    

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class TeamSerializer(serializers.ModelSerializer):
    user1 = UserSerializer()
    user2 = UserSerializer()
    login_status = serializers.BooleanField(write_only=True)
    class Meta: 
        model = Team
        fields = ['teamname', 'user1', 'user2', 'category','login_status']

    def create(self, validated_data):
        user1_data = validated_data.pop('user1')
        user2_data = validated_data.pop('user2')

        user1 = UserSerializer.create(UserSerializer(), validated_data=user1_data)
        user2 = UserSerializer.create(UserSerializer(), validated_data=user2_data)

        team = Team.objects.create(user1=user1, user2=user2, **validated_data)
        return team
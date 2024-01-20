from django.db import models
from django.contrib.auth.models import User
import random

class Question(models.Model):
    LEVEL_CHOICES = [("E", 'Easy'),("H", 'Hard'),]
    CATEGORY_CHOICES = [("JR", 'Junior'),("SR", 'Senior'),]
    question_id = models.IntegerField(primary_key=True)
    question_text = models.CharField(max_length=255)
    correct_answer = models.IntegerField()
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)

class Team(models.Model):
    user1 = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user2')
    category = models.CharField(max_length=2, choices=Question.CATEGORY_CHOICES)
    teamname = models.CharField(max_length=255)

    def __str__(self):
        return self.teamname
    
    def get_questions_for_team(self):
        #Suppose 10 Questions are to Given then 5 Easy 5 Hard
        easy_questions = list(Question.objects.filter(level='E', category=self.category))
        hard_questions = list(Question.objects.filter(level='H', category=self.category))
        questions = random.sample(easy_questions, 5)
        questions += random.sample(hard_questions, 5)
        return questions
    
class Progress(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='progress')  
    score = models.IntegerField(default = 0)
    start_time = models.DateTimeField(auto_now_add=True, blank=True)
    end_time = models.DateTimeField(auto_now_add=True, blank=True) 
    current_questions = models.TextField()
    isAttemptedFirst = models.BooleanField(default=False)
    isAttemptedSecond = models.BooleanField(default=False)

    

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Question(models.Model):
    CATEGORY_CHOICES = [("JR", 'Junior'),("SR", 'Senior'),]  
    question_id = models.IntegerField(primary_key=True)
    question_text = models.CharField(max_length=255)
    correct_answer = models.IntegerField()
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    responses = models.CharField(max_length= 255 , null = True )

class Team(models.Model):
    user1 = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user2')
    category = models.CharField(max_length=2, choices=Question.CATEGORY_CHOICES)
    teamname = models.CharField(max_length=255,unique = True)
    login_status = models.BooleanField(default=False)

    def __str__(self):
        return self.teamname
    
class Progress(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='progress')  
    score = models.IntegerField(default = 0)
    start_time = models.DateTimeField(blank =True)
    end_time = models.DateTimeField(blank =True ) 
    current_question = models.IntegerField(default=1)
    question_list = models.CharField(max_length = 256)
    prev_answer = models.IntegerField(default = 0)
    isAttemptedFirst = models.BooleanField(default=False)
    lifeline1=models.BooleanField(default=False)
    lifeline2=models.BooleanField(default=False)
    lifeline3=models.BooleanField(default=False)
    lifeline_flag = models.SmallIntegerField(default = 1)

    def __str__(self):
            return (self.team.teamname)
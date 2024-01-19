#models.py
from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    user1 = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user2')
    teamname = models.CharField(max_length=255)

    def __str__(self):
        return self.teamname

class Question(models.Model):
    question_id = models.IntegerField(primary_key=True)
    question_text = models.CharField()
    correct_answer = models.IntegerField()


class Progress(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='progress')  
    score = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField() 
    current_question = models.ForeignKey(Question, on_delete=models.PROTECT)
    isAttemptedFirst = models.BooleanField(default=False)
    isAttemptedSecond = models.BooleanField(default=False)

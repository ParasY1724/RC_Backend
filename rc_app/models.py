from django.db import models
from datetime import datetime, timedelta

# Create your models here.
class UserTable(models.Model) :
    user_id =models.IntegerField(primary_key = True)
    username = models.CharField(max_length = 255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length = 255)

class Question(models.Model):
    question_id = models.IntegerField(primary_key=True)
    question_text = models.TextField()
    correct_answer = models.IntegerField()


class TeamTable(models.Model) :
    team_id = models.IntegerField(primary_key = True)
    team_name = models.CharField(max_length = 255 , unique = True)
    score = models.IntegerField()
    start_time = models.DateTimeField(default=datetime.now())
    end_time = models.DateTimeField(default=datetime.now() + timedelta(hours=2)) 
    current_question_id = models.ForeignKey(Question, on_delete=models.PROTECT)
    attempts = models.IntegerField(default=2)



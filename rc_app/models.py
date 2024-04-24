from django.db import models

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    question_id = models.IntegerField(unique=True)
    question_text = models.TextField()
    correct_answer = models.IntegerField()
    responses = models.CharField(max_length=255, null=True)

class Team(models.Model):
    CATEGORY_CHOICES = [("JR", 'Junior'),("SR", 'Senior'),]
    user1 = models.CharField(max_length=255)
    user2 = models.CharField(max_length=255,blank=True,null=True)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    teamname = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    login_status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.teamname

    
class Progress(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='progress')  
    score = models.IntegerField(default = 0)
    start_time = models.DateTimeField(null =True)
    end_time = models.DateTimeField(null =True ) 
    current_question = models.IntegerField(default=1)
    question_list = models.CharField(max_length = 256)
    prev_answer = models.IntegerField(default = 0)
    correct_count = models.SmallIntegerField(default=0)
    incorrect_count = models.SmallIntegerField(default=0)
    isAttemptedFirst = models.BooleanField(default=False)
    lifeline1=models.BooleanField(default=False)
    lifeline2=models.BooleanField(default=False)
    lifeline3=models.BooleanField(default=False)
    lifeline_flag = models.SmallIntegerField(default = 1)

    def __str__(self):
            return (self.team.teamname)
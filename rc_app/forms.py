from django import forms
from .models import UserTable, Question, TeamTable

class UserForm(forms.ModelForm):
    class Meta:
        model = UserTable
        fields = ['username', 'email', 'password']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'correct_answer']

class TeamForm(forms.ModelForm):
    class Meta:
        model = TeamTable
        fields = ['team_name', 'score', 'current_question_id', 'attempts']

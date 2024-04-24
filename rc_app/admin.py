# admin.py
from django.contrib import admin
from .models import Question, Team, Progress
from import_export.admin import ImportExportModelAdmin
from import_export import resources,fields

class QuestionResource(resources.ModelResource):
    id = fields.Field(attribute='id', column_name='id')

    class Meta:
        model = Question
        exclude = ('id',)
        fields = ('question_id', 'question_text', 'correct_answer', 'responses')

class TeamResource(resources.ModelResource):
    class Meta:
        model = Team

class ProgressResource(resources.ModelResource):
    class Meta:
        model = Progress

@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource

@admin.register(Team)
class TeamAdmin(ImportExportModelAdmin):
    resource_class = TeamResource

@admin.register(Progress)
class ProgressAdmin(ImportExportModelAdmin):
    resource_class = ProgressResource

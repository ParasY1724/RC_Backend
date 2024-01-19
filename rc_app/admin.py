# admin.py
from django.contrib import admin
from .models import Question, Team, Progress

# Register your models with admin.site.register
admin.site.register(Question)
admin.site.register(Team)
admin.site.register(Progress)

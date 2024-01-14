from django.contrib import admin
from .models import UserTable,Question,TeamTable
# Register your models here.

admin.site.register(UserTable)
admin.site.register(Question)
admin.site.register(TeamTable)


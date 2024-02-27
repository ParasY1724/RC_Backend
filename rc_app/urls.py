#urls.py
from django.urls import path
from .views import CreateTeamView,LeaderboardView,GetQuestionView,LoginView,LogoutView,ResultView
from .lifelines import GetLifeline1
urlpatterns = [
    path('create_team', CreateTeamView.as_view(), name='create_team'),
    path('login',LoginView.as_view(),name="login"),
    path('leaderboard', LeaderboardView.as_view(), name='leaderboard'),
    path('get_question', GetQuestionView.as_view(), name='get_question'),
    path('logout',LogoutView.as_view(),name="logout"),
    path('result',ResultView.as_view(),name="result"),
    path('lifeline',GetLifeline1.as_view(),name="life_line"),
]

#urls.py
from django.urls import path
from .views import create_team,leaderboard
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('create_team/', create_team, name='create_team'),
    path('token/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='obtain_token'),
    path('leaderboard/', leaderboard, name='leaderboard'),

]

#views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .models import Team
from .serializers import TeamSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def create_team(request):
    if request.method == 'POST':
        team_serializer = TeamSerializer(data=request.data)
        user1_serializer = UserSerializer(data=request.data.get('user1'))
        user2_serializer = UserSerializer(data=request.data.get('user2'))

        if team_serializer.is_valid() and user1_serializer.is_valid() and user2_serializer.is_valid():
        
            user1 = user1_serializer.save()
            user2 = user2_serializer.save()

            user1.set_password(request.data.get('user1')['password'])   #Hashing 
            user2.set_password(request.data.get('user2')['password'])

            user1.save()
            user2.save()

            team = team_serializer.save(user1=user1, user2=user2)
            return Response(TeamSerializer(team).data, status=status.HTTP_201_CREATED)

        return Response(team_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leaderboard(request):
    teams = Team.objects.all().order_by('-progress__score')
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)

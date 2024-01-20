from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .models import Team,Progress
from .serializers import TeamSerializer, UserSerializer,QuestionSerializer
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

from django.db.models import Q  # For Logical Operations
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_question(request):
    try:
        team = Team.objects.get(Q(user1=request.user) | Q(user2=request.user))
    except Team.DoesNotExist:
        return Response({"error": "Team not found for the authenticated user"}, status=status.HTTP_404_NOT_FOUND)

    progress, created = Progress.objects.get_or_create(team=team)          #get_or_create tuple return karta he

    if created:
        questions = team.get_questions_for_team()
        progress.current_questions = str(questions)
        progress.save()
    else:
        questions = progress.get_saved_questions()

    question_serializer = QuestionSerializer(questions, many=True)
    return Response(question_serializer.data, status=status.HTTP_200_OK)

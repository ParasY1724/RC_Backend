from . import MarkingScheme
from rest_framework import generics,status
from .permissions import JWTAuthentication
from .serializers import QuestionSerializer
from .models import Question,Team,Progress
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import redirect   


#lifeline 1
def Amplifier(progress):
    if (progress.lifeline1 == False and progress.isAttemptedFirst == False):
        progress.lifeline_flag = 2
        progress.isAttemptedFirst = True
        progress.lifeline1 = True
        progress.save()
    else :
        return Response({"error": "Lifeline is already used or can't use right now"}, status=status.HTTP_406_NOT_ACCEPTABLE)

class GetLifeline1(generics.ListAPIView):
    queryset = Question.objects.none()
    permission_classes = [JWTAuthentication]
    serializer_class = QuestionSerializer

    def get(self, request):
        try:
            team = Team.objects.get(Q(user1=request.user) | Q(user2=request.user))
            progress = Progress.objects.get(team = team)
        except Team.DoesNotExist:
            return Response({"error": "Team not found for the authenticated user"}, status=status.HTTP_404_NOT_FOUND)
        except Progress.DoesNotExist:
            return Response({"error": "Team not found for the authenticated user"}, status=status.HTTP_404_NOT_FOUND)
        Amplifier(progress)
        return redirect('get_question')
        
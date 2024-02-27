from . import MarkingScheme
from rest_framework import generics,status
from .permissions import JWTAuthentication
from .serializers import QuestionSerializer
from .models import Question,Team,Progress
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import redirect   
from django.http import JsonResponse

#lifeline 1
def Amplifier(progress):
    if (progress.lifeline1 == False and progress.isAttemptedFirst == False):
        progress.lifeline_flag = 2
        progress.isAttemptedFirst = True
        progress.lifeline1 = True
        progress.save()
    else :
        return Response({"error": "Lifeline is already used or can't use right now"}, status=status.HTTP_406_NOT_ACCEPTABLE)

def Freezer(progress):
    if not progress.lifeline2:
        progress.lifeline2 = True
        progress.lifeline_flag = 3
        progress.start_time = timezone.now()
        progress.save()
    elif progress.lifeline_flag == 3:

        time_delta = ((timezone.now() - progress.start_time).total_seconds())//10
        if (time_delta >= 6):
            progress.lifeline_flag = 1
            progress.end_time += timezone.timedelta(seconds=54)
            progress.save()
            return JsonResponse(
                {
                'hours': -1,
                'minutes': -1,
                'seconds': -1
            }
            )
     
        time_remaining = progress.end_time - progress.start_time - timezone.timedelta(seconds=time_delta)
        time_data = MarkingScheme.Timer(time_remaining)

        return JsonResponse(time_data)


class GetLifeline1(generics.ListAPIView):
    queryset = Question.objects.none()
    permission_classes = [JWTAuthentication]
    serializer_class = QuestionSerializer

    def get(self, request):
        lifeline_no = request.query_params.get('lifeline',default = "NONE")
        try:
            team = Team.objects.get(Q(user1=request.user) | Q(user2=request.user))
            progress = Progress.objects.get(team = team)
        except Team.DoesNotExist:
            return Response({"error": "Team not found for the authenticated user"}, status=status.HTTP_404_NOT_FOUND)
        except Progress.DoesNotExist:
            return Response({"error": "Team not found for the authenticated user"}, status=status.HTTP_404_NOT_FOUND)
        if (lifeline_no == "aqua_point"):
            Amplifier(progress)
        elif (lifeline_no == "time_freeze"):
            context = Freezer(progress)
            if (context):
                return context
        return redirect('get_question')
        
from django.utils import timezone

POSTIVE_MARKING = 4
NEGATIVE_MARKING = -2

#marking scheme
def evaluate_postive(progress):
    if (progress.isAttemptedFirst):
        score = POSTIVE_MARKING/2 
    else :
        score = POSTIVE_MARKING
    progress.current_question+=1
    progress.isAttemptedFirst = False

    if (progress.lifeline_flag == 2) :
         progress.score += score * 4
    else :
         progress.score += score 

def evaluate_negative(progress,answer) :
    progress.prev_answer = answer
    if (progress.isAttemptedFirst):
        score = NEGATIVE_MARKING/2
        progress.isAttemptedFirst = False
        progress.current_question+=1
    else :
        score = NEGATIVE_MARKING
        progress.isAttemptedFirst = True
    if (progress.lifeline_flag == 2):
            progress.end_time -= timezone.timedelta(minutes=5)
            progress.score += score * 4
    else:
        progress.score += score * 1 
         

        
        
    


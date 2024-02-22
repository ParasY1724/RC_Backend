
POSTIVE_MARKING = 4
NEGATIVE_MARKING = -2



def evaluate_postive(progress):
    progress.score += POSTIVE_MARKING * progress.lifeline_flag
    progress.current_question+=1
    progress.isAttemptedFirst = False

def evaluate_negative(progress,answer) :
    progress.prev_answer = answer
    progress.score += NEGATIVE_MARKING * progress.mark
    if ( not progress.isAttemptedFirst):
        progress.isAttemptedFirst = True
    else:
        progress.isAttemptedFirst = False
        progress.current_question+=1
    


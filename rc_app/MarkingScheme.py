POSTIVE_MARKING = 4
NEGATIVE_MARKING = -1

"""
Marking Scheme =>
1st Attempt +4 -1
2nd Attempt +3 -1
if (lifeline_flag == 2) +8 -4
"""

def evaluate_postive(progress):
    if (progress.lifeline_flag == 2) :
         progress.score += POSTIVE_MARKING * 2
    else:
        progress.score += POSTIVE_MARKING - (progress.isAttemptedFirst) 

    progress.current_question+=1
    progress.correct_count +=1
    progress.isAttemptedFirst = False



def evaluate_negative(progress,answer) :
    progress.prev_answer = answer
    progress.incorrect_count += 1
    if (progress.isAttemptedFirst):
        progress.isAttemptedFirst = False
        progress.current_question+=1
    else :
        progress.isAttemptedFirst = True
    if (progress.lifeline_flag == 2):
            progress.score += NEGATIVE_MARKING * 4
    else:
        progress.score += NEGATIVE_MARKING


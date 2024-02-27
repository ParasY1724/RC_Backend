POSTIVE_MARKING = 4
NEGATIVE_MARKING = -2



def evaluate_postive(progress):
    progress.score += POSTIVE_MARKING * progress.lifeline_flag
    progress.current_question+=1
    progress.isAttemptedFirst = False

def evaluate_negative(progress,answer) :
    progress.prev_answer = answer
    progress.score += NEGATIVE_MARKING * progress.lifeline_flag
    if ( not progress.isAttemptedFirst):
        progress.isAttemptedFirst = True
    else:
        progress.isAttemptedFirst = False
        progress.current_question+=1
    

def Timer(time_remaining):
    if time_remaining.total_seconds() > 0:
            
            hours = time_remaining.seconds // 3600
            minutes = (time_remaining.seconds % 3600) // 60
            seconds = time_remaining.seconds % 60

            
            time_data = {
                'hours': hours,
                'minutes': minutes,
                'seconds': seconds
            }
    else:
        time_data = {
            'hours': 0,
            'minutes': 0,
            'seconds': 0
        }
    return time_data
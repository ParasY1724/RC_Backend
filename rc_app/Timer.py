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
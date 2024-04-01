
### README

This Django application serves as a quiz platform where teams can participate in quizzes, answer questions, and view their scores on a leaderboard.

#### Schema
Here's an overview of our database schema:

![Database Schema](https://github.com/ParasY1724/RC_Backend/blob/main/DB_Schema.png?raw=true)

#### Endpoints

| Endpoint           | Method | Description                        |
|--------------------|--------|------------------------------------|
| `/api/create_team` | POST   | Create a new team                  |
| `/api/login`       | POST   | Login and generate JWT token       |
| `/api/leaderboard` | GET    | Retrieve the leaderboard           |
| `/api/get_question`|GET/POST| Fetch and answer questions         |
| `/api/logout`      | GET    | Logout and deletes the token from cookies|
| `/api/result`      | GET    | Obtain the team's score            |
| `/api/lifeline`    | GET    | Utilize lifelines during the quiz  |

#### Usage

1. **Team Creation**: 
   - Endpoint: `/api/create_team`
   - Method: POST
   - Request Body: `{"teamname": "Team123","password": "pass123","category": "JR"}`

2. **Login**:
   - Endpoint: `/api/login`
   - Method: POST
   - Request Body: `{"teamname": "Team123","password": "pass123"}`

3. **Get Question**:
   - Endpoint: `/api/get_question`
   - Method: GET
   - Response Body: `{
                      "Current_Question": 5,
                      "question": "100-99",
                      "attempts": 2,
                      "prev_ans": 0,
                      "score": 20,
                      "lifeline_flag": 1,
                      "lifeline1": false,
                      "lifeline2": false,
                      "lifeline3": false,
                      "hours": 1,
                      "minutes": 27,
                      "seconds": 12
                    }`

   - Method: POST (to submit answer)
   - Request Body: `{"answer" : "2"}`

4. **Lifeline Usage**: 

| Endpoint         | Method | Lifeline     | Conditions                                         | Response        |
|------------------|--------|--------------|----------------------------------------------------|-----------------|
| `/api/lifeline?lifeline=aqua_point`  | GET    | Amplifier    | `lifeline1 == False && attempts == 2`             | -----           |
| `/api/lifeline?lifeline=time_freeze`  | GET    | Time Freeze  | `lifeline1 == True && lifeline2 == False && (time for activation < 5 sec from get question)` | ----           |
| `/api/lifeline?lifeline=poll`  | GET    | Audience Poll| `lifeline1,2 == True && lifeline3 == False`       | Responses for answer of that question: `{"2": 14, "3": 9, "0": 1}` |

Activate the appropriate lifeline based on the conditions mentioned in the table. Enjoy the benefits of lifelines during the quiz!


5. **Leaderboard**: 
   - Endpoint: `/api/leaderboard`
   - Method: GET

6. **Result**
   - Endpoint: `/api/result`
   - Method: GET

7. **Logout**:
   - Endpoint: `/api/logout`
   - Method: GET

#### Dependencies
- Django
- Django Rest Framework
- django-cors-headers

#### Setup
1. Clone this repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Migrate the database using `python manage.py migrate`.
4. Start the Django development server with `python manage.py runserver`.

Feel free to explore and enjoy your quiz experience with us!
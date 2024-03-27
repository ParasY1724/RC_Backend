
### README

This Django application serves as a quiz platform where teams can participate in quizzes, answer questions, and view their scores on a leaderboard.

#### SCHEMA
![alt text](https://github.com/ParasY1724/RC_Backend/blob/main/DB_Schema.png?raw=true)


#### Endpoints

| Endpoint             | Method | Description                   |
|----------------------|--------|-------------------------------|
| `api/create_team`    | POST   | Create a new team             |
| `api/login`          | POST   | Login and generate JWT token  |
| `api/leaderboard`    | GET    | Get the leaderboard           |
| `api/get_question`   | GET/   | Get a question for the team & |
|                      | POST   | Post answer response          |
| `api/logout`         | GET    | Logout and invalidate token   |
| `api/result`         | GET    | Get the team's score          |
| `api/lifeline`       | GET    | Use lifeline                  |



### Usage

1. **Team Creation**: Use the `api/create_team` endpoint to create a new team by providing user details and team information.

2. **Login**: Authenticate users and generate a JWT token using the `api/login` endpoint. This token is used for subsequent requests.

3. **Question Retrieval**: Access questions for the team using the `api/get_question` endpoint. Questions are randomly selected based on the team's category.

4. **Lifeline Usage**: Teams can use lifelines during quizzes. Available lifelines include "Amplifier" , "Time Freeze" and "Audience Poll". Use the `api/lifeline` endpoint to activate lifelines.

    -`api/lifeline?lifeline=time_freeze` => "Time Freeze"
    
    -`api/lifeline?lifeline=aqua_point` => "Amplifier"
    
    -`api/lifeline?lifeline=poll` => "Audience Poll"


5. **Answer Submission**: Submit answers to questions using the `api/get_question` endpoint with a POST request.

6. **Leaderboard**: View the leaderboard to see scores of all participating teams. Access this information through the `api/leaderboard` endpoint.

7. **Logout**: Log out and invalidate the JWT token using the `api/logout` endpoint.

### Dependencies

- Django
- Django Rest Framework

### Setup

1. Clone this repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Migrate the database using `python manage.py migrate`.
4. Start the Django development server with `python manage.py runserver`.

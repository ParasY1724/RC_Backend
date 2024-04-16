# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth.models import User
# from .models import Team, Progress, Question
# from rest_framework import status
# from rest_framework.test import APIClient
# from http.cookies import SimpleCookie
# import json

# token = None

# class TestRCAppViews(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user1 = User.objects.create_user(username='TestUser1', password='password')
#         self.team = Team.objects.create(user1=self.user1,category='JR', teamname='TestTeam')
#         Question.objects.create(question_id=1, question_text='Test Question', correct_answer=1, category='JR')




#     def test_a_create_team(self):
#         url = reverse('create_team')
#         data = {
#             "teamname": "TestTeam2",
#             "user1": {
#                 "username": "TestUser01",
#                 "email": "user@rc.com",
#                 "password" : "password"
#             },
#             "user2": {
#                 "username": "TestUser02",
#                 "email": "user2@rc.com",
#                 "password" : "password"
#             },
#             "category": "JR",
#             "login_status": False
#         }        
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

#     def test_b_login(self):
#         url = reverse('login')
#         data = {'username': 'TestUser1', 'team': 'TestTeam', 'password': 'password'}
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue('jwt' in response.data)
#         global token
#         token = response.data['jwt']

#     def test_get_question(self):
#         global token
#         self.client.cookies = SimpleCookie({'jwt': token})
#         url = reverse('get_question')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     # def test_post_answer_correct(self):
#     #     global token
#     #     self.client.cookies = SimpleCookie({'jwt': token})
#     #     url = reverse('get_question')
#     #     data = {'answer': 1, 'team': 'TestTeam'}
#     #     self.client.force_login(self.user1)
#     #     response = self.client.post(url, data, format='json')
#     #     # Redirects to get_question
#     #     print(response.data)
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)


from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .test_helpers import create_superuser, create_user, PASSWORD

class UserAccountTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('auth_register')
        self.login_url = reverse('token_obtain_pair')
        self.refresh_url = reverse('token_refresh')

        self.super_user = create_superuser(username="superuser")
        self.user = create_user(username="maintestuser")

    def test_user_registration(self):
        data = {
            "username": "testuser",
            "password": PASSWORD,
            "password2": PASSWORD
        }

        response = self.client.post(self.register_url, data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_and_refresh(self):
        login_data = { 'username': self.user.username, 'password': PASSWORD }
        
        login_response = self.client.post(self.login_url, login_data, format='json', secure=True)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', login_response.data)

        refresh_token = login_response.data['refresh']
        refresh_response = self.client.post(self.refresh_url, { 'refresh': refresh_token }, format='json', secure=True)
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)

    def test_registration_duplicate_user(self):
        data = {
            "username": "maintestuser",
            "password": PASSWORD,
            "password2": PASSWORD
        }

        response = self.client.post(self.register_url, data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_login(self):
        login_data = { 'username': self.user.username, 'password': "wrongpassword" }
        
        login_response = self.client.post(self.login_url, login_data, format='json', secure=True)
        self.assertEqual(login_response.status_code, status.HTTP_401_UNAUTHORIZED)
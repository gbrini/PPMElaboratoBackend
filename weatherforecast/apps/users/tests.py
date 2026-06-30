from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

class UserAccountTest(APITestCase):
    def test_user_registration(self):
        url = reverse('auth_register')
        data = {
            "username": "testuser",
            "password": "PasswordTest123!",
            "password2": "PasswordTest123!"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().username, "testuser")
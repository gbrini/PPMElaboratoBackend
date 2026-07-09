from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .test_helpers import create_user, PASSWORD

class UserEditTest(APITestCase):
    def setUp(self):
        self.user = create_user(username='user')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('change_password')

    def test_change_password_success(self):
        new_password = "Password!67"
        data = {
            "old_password": PASSWORD,
            "new_password": new_password,
            "confirm_new_password": new_password
        }

        response = self.client.post(self.url, data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(new_password))

    def test_change_password_fail(self):
        new_password = "Password!67"
        data = {
            "old_password": PASSWORD,
            "new_password": new_password,
            "confirm_new_password": new_password + 'a'
        }

        response = self.client.post(self.url, data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
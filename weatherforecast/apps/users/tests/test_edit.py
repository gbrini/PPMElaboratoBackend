from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from .test_helpers import create_user, create_superuser

class UserEditTest(APITestCase):
    def setUp(self):
        self.admin = create_superuser(username='admin_user')
        self.standard_user = create_user(username='std_user')

        self.list_url = reverse('list_users')

    def test_list_users_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.list_url, secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users_as_standard_user_fails(self):
        self.client.force_authenticate(user=self.standard_user)
        response = self.client.get(self.list_url, secure=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_user_role_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = f'/api/users/{self.standard_user.id}/'
        data = {'role': 'premium'}
        response = self.client.put(url, data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.standard_user.refresh_from_db()
        self.assertEqual(self.standard_user.role, 'premium')

    def test_delete_user(self):
        self.client.force_authenticate(user=self.admin)
        rm_user = create_user(username='rm_user')
        url = f'/api/users/{rm_user.id}/'
        response = self.client.delete(url, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
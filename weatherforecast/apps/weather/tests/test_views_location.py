from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import WeatherLocation
from django.contrib.auth import get_user_model

User = get_user_model()

class WeatherLocationViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.admin = User.objects.create_superuser(username='admin', password='password')
        self.admin.role = 'admin'
        self.admin.save()
        self.list_url = reverse('weather_location') 

    def test_get_locations_allow_any(self):
        """Anyone should be able to view the list of locations."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_location_requires_admin(self):
        """Standard users should NOT be able to create locations."""
        self.client.force_authenticate(user=self.user)
        data = {"name": "Rome", "country": "IT", "latitude": 41.9, "longitude": 12.5}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_location_success_as_admin(self):
        """Admin should be able to create new locations."""
        self.client.force_authenticate(user=self.admin)
        data = {"name": "Milan", "country": "IT", "latitude": 45.4, "longitude": 9.1}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WeatherLocation.objects.count(), 1)
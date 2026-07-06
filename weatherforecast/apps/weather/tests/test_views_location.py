from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import WeatherLocation
from .test_helpers import create_superuser, create_user

class WeatherLocationViewTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.admin = create_superuser()
        self.list_url = reverse('weather_location')

    def test_get_locations_allow_any(self):
        response = self.client.get(self.list_url, secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_location_requires_admin(self):
        self.client.force_authenticate(user=self.user)
        data = {"name": "Rome", "country": "IT", "latitude": 41.9, "longitude": 12.5}
        response = self.client.post(self.list_url, data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_location_success_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {"name": "Milan", "country": "IT", "latitude": 45.4, "longitude": 9.1}
        response = self.client.post(self.list_url, data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WeatherLocation.objects.count(), 1)
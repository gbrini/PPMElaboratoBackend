from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .test_helpers import create_user, create_superuser
from ..models import WeatherLocation, WeatherQuery, WeatherData

class WeatherForecastViewTests(APITestCase):
    def setUp(self):
        # Create an admin user for POST requests
        self.admin = create_superuser(username='admin')
        self.location = WeatherLocation.objects.create(name="Rome", country="IT", user=self.admin)
        self.url = reverse('weather_forecast')

    def test_get_weather_forecast_list(self):
        """Anyone can access the list of forecasts."""
        response = self.client.get(f"{self.url}?location={self.location.name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_weather_forecast_as_admin(self):
        """Admin can create a new forecast."""
        self.client.force_authenticate(user=self.admin)
        data = {
            "location_id": self.location.id,
            "forecast_date": "2026-07-06",
            "forecast_hour": 10,
            "weather_info": {"temperature": 22.5, "condition": "Sunny", "humidity": 45, "uv_index": 3}
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WeatherQuery.objects.count(), 1)

    def test_post_weather_forecast_non_admin_fails(self):
        """Standard users should NOT be able to create a new forecast."""
        # Create a non-admin user
        standard_user = create_user(
            username='standard_user',
            role='standard'
        )
        self.client.force_authenticate(user=standard_user)
        
        data = {
            "location_id": self.location.id,
            "forecast_date": "2026-07-06",
            "forecast_hour": 10,
            "weather_info": {"temperature": 22.5, "condition": "Sunny", "humidity": 45, "uv_index": 3}
        }
        
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(WeatherQuery.objects.count(), 0)

    
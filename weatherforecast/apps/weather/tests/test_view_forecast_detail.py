from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .test_helpers import create_user, create_superuser
from ..models import WeatherLocation, WeatherQuery, WeatherData

class WeatherForecastDetailViewTests(APITestCase):
    def setUp(self):
        self.admin = create_superuser(username='admin')
        self.location = WeatherLocation.objects.create(name="Rome", country="IT", user=self.admin)
        self.weather_info = WeatherData.objects.create(temperature=20.0, condition="Cloudy")
        self.forecast = WeatherQuery.objects.create(
            user=self.admin, location=self.location, weather_info=self.weather_info, forecast_date='2028-06-15', forecast_hour=10
        )
        self.detail_url = reverse('weather_forecast_detail', kwargs={'pk': self.forecast.pk})

    def test_put_update_forecast(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            "location_id": self.location.id,
            "forecast_date": "2032-07-06",
            "forecast_hour": 15,
            "weather_info": {"temperature": 35.0, "condition": "Hot", "humidity": 30, "uv_index": 9}
        }
        
        response = self.client.put(self.detail_url, data, format='json', secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.forecast.refresh_from_db()
        self.assertEqual(self.forecast.forecast_hour, 15)
        self.assertEqual(self.forecast.weather_info.temperature, 35.0)

    def test_delete_forecast_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.detail_url, secure=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WeatherQuery.objects.count(), 0)

    def test_delete_forecast_as_unauthorized(self):
        user = create_user(username='std', role='standard')
        self.client.force_authenticate(user=user)
        response = self.client.delete(self.detail_url, secure=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from ..models import WeatherLocation, WeatherData, WeatherQuery
from .test_helpers import create_superuser, create_user

class WeatherLocationDetailViewTests(APITestCase):
    def setUp(self):
        self.user = create_user()
        self.admin = create_superuser()
        self.general_url = reverse('weather_location')

    def test_delete_location_requires_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse('weather_location_detail', kwargs={ 'pk': 1 }), secure=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_location(self):
        self.client.force_authenticate(user=self.admin)
        data = {"name": "Malmo", "country": "SE", "latitude": 12.4, "longitude": 67.1}
        response = self.client.post(self.general_url, data, format='json', secure=True)

        new_id = response.data['id']

        response_patch = self.client.delete(reverse('weather_location_detail', kwargs={ 'pk': new_id }), secure=True)

        self.assertEqual(response_patch.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(WeatherLocation.objects.filter(id = new_id)), 0)

    def test_put_location_success_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {"name": "Milan", "country": "IT", "latitude": 45.4, "longitude": 9.1}
        response = self.client.post(self.general_url, data, format='json', secure=True)

        new_id = response.data['id']

        data['latitude'] = 56
        response_patch = self.client.put(reverse('weather_location_detail', kwargs={ 'pk': new_id }), data, format='json', secure=True)

        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        self.assertAlmostEqual(WeatherLocation.objects.filter(id = new_id).get().latitude, 56)

    def test_delete_forecast_location(self):
        self.client.force_authenticate(user=self.admin)
        
        location = WeatherLocation.objects.create(name="Rome", country="IT", user=self.admin)
        weather_info = WeatherData.objects.create(temperature=20.0, condition="Cloudy")
        forecast = WeatherQuery.objects.create(
            user=self.admin, location=location, weather_info=weather_info, forecast_date='2032-06-15', forecast_hour=10
        )

        self.assertEqual(len(WeatherQuery.objects.filter(location = location.id)), 1)
        response_patch = self.client.delete(reverse('weather_location_detail', kwargs={ 'pk': location.id }), secure=True)
        self.assertEqual(len(WeatherQuery.objects.filter(location = location.id)), 0)
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .test_helpers import create_user, create_search_history

User = get_user_model()

class WeatherForecastQueryHistoryDetailViewTests(APITestCase):
    def setUp(self):
        self.user = create_user(username='premium_user', role='premium')
        self.client.force_authenticate(user=self.user)
        self.list_url = reverse('weather_forecast_query_history') 

    def test_history_ordering(self):
        old = create_search_history(self.user, hours_ago=10)
        new = create_search_history(self.user, hours_ago=1)
        
        response = self.client.get(self.list_url, secure=True)
        
        self.assertEqual(response.data['results'][0]['id'], new.id)
        self.assertEqual(response.data['results'][1]['id'], old.id)

    def test_permission_denied_for_standard_user(self):
        standard_user = create_user(username='std', role='standard')
        self.client.force_authenticate(user=standard_user)
        
        response = self.client.get(self.list_url, secure=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .test_helpers import create_user, create_search_history

User = get_user_model()

class WeatherForecastRequestTrackingViewTests(APITestCase):
    def setUp(self):
        self.user = create_user(username='premium_user', role='premium')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('weather_forecast_tracking')

    def test_tracking_aggregation(self):
        """Test that searches are grouped by day and counted correctly."""
        create_search_history(self.user, days_ago=0, count=1)
        create_search_history(self.user, days_ago=0, count=1)
        
        response = self.client.get(self.url, secure=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should have 1 object in the list for 'today' with count 2
        self.assertEqual(response.data[0]['count'], 2)

    def test_tracking_includes_throttle_rate_today(self):
        """Verify the custom throttle_rate field is added for today's requests."""
        create_search_history(self.user, days_ago=0)
        
        response = self.client.get(f"{self.url}?today=true", secure=True)
        self.assertIn('throttle_rate', response.data[0])

    
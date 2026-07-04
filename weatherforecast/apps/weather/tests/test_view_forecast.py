from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError as ValidationErrorDjangoCore
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import timedelta
from .test_helpers import create_user, create_superuser
from ..models import WeatherLocation, WeatherQuery, WeatherData
from ..serializers import WeatherQueryCreateSerializer
from ..filters import WeatherQueryFilter

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
            "forecast_date": "2028-07-06",
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

    def test_cannot_create_past_forecast(self):
        """Ensure serializer raises error for past dates."""
        past_date = timezone.now().date() - timedelta(days=1)
        data = {
            "location_id": self.location.id,
            "forecast_date": past_date,
            "forecast_hour": 10,
            "weather_info": {"temperature": 20.0}
        }
        serializer = WeatherQueryCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('forecast_date', serializer.errors)

    def test_filter_requires_location(self):
        """Test that the filter raises ValidationError if location is missing."""
        filter_set = WeatherQueryFilter(data={})
        self.assertFalse(filter_set.is_valid())
        self.assertIn('location', filter_set.errors)

    def test_filter_hour_range_validation(self):
        """Test hour_min > hour_max error logic."""
        data = {
            "location": "Rome",
            "hour_min": 15,
            "hour_max": 10
        }
        filter_set = WeatherQueryFilter(data=data)
        # This will trigger the ValidationError in the .qs property
        with self.assertRaises(ValidationError) as cm:
            _ = filter_set.qs

        self.assertEqual(cm.exception.detail['hour_min'], "Hour min cannot be greater than hour max.")

    def test_model_clean_enforces_admin_role(self):
        """Test that the model clean() method prevents saving by non-admin users."""
        standard_user = create_user(
            username='std',
            role='standard'
        )

        query = WeatherQuery(
            user=standard_user, 
            location=self.location, 
            forecast_hour=10
        )
        
        with self.assertRaises(ValidationErrorDjangoCore) as cm:
            query.clean()
        
        self.assertEqual(cm.exception.messages[0], "Only admins can post/put weather forecasts.")
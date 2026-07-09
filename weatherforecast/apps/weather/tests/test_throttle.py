from django.core.cache import cache
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase
from .test_helpers import create_superuser, create_user, PASSWORD

class UserEditTest(APITestCase):
    def setUp(self):
        cache.clear()
        self.me_url = reverse("me")
        self.weather_url = reverse("weather_forecast")

    def tearDown(self):
        cache.clear()

    def call_endpoint(self, role):
        if role == "admin":
            user = create_superuser(username="test_throttle_admin")
            self.client.force_authenticate(user=user)
            n = 200
        elif role in ["premium", "standard"]:
            user = create_user(username=f"test_throttle_{role}", role=role)
            n = settings.MY_PROJECT_SETTINGS['THROTTLE_RATE']['premium'] if role == "premium" else settings.MY_PROJECT_SETTINGS['THROTTLE_RATE']['standard']
            self.client.force_authenticate(user=user)
        else:
            n = settings.MY_PROJECT_SETTINGS['THROTTLE_RATE']['anon']
        
        for i in range(n):
            response = self.client.get(
                f"{self.weather_url}?location=tokyo", secure=True
            )
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            f"{self.weather_url}?location=tokyo", secure=True
        )
        self.assertEqual(
            response.status_code, status.HTTP_429_TOO_MANY_REQUESTS
        )

    def test_anon(self):
        self.call_endpoint("anon")

    def test_standard(self):
        self.call_endpoint("standard")

    def test_premium(self):
        self.call_endpoint("premium")
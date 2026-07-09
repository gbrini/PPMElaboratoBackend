from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.weather.models import WeatherQuery, WeatherLocation, WeatherData
from django.utils import timezone

from datetime import timedelta
import datetime
import random

user_model = get_user_model()

class Command(BaseCommand):
    help = 'Loads fake weather data for testing'

    def handle(self, *args, **kwargs):
        admin = user_model.objects.filter(role='admin').get()

        if not admin:
            self.stdout.write("No admin user found.")
            return
        
        cities = [
            ("Rome", "IT", 41.9028, 12.4964),
            ("Milan", "IT", 45.4642, 9.1900),
            ("Florence", "IT", 43.7696, 11.2558),
            ("Paris", "FR", 48.8566, 2.3522),
            ("London", "GB", 51.5074, -0.1278),
            ("New York", "US", 40.7128, -74.0060),
            ("Tokyo", "JP", 35.6762, 139.6503),
            ("Berlin", "DE", 52.5200, 13.4050),
        ]

        conditions = [
            "Sunny",
            "Cloudy",
            "Rain",
            "Storm",
            "Snow",
            "Fog",
            "Windy",
            "Partly Cloudy",
        ]

        today = datetime.date.today()

        for city_name, country, lat, lon in cities:
            location = WeatherLocation.objects.create(
                user=admin,
                name=city_name,
                country=country,
                latitude=float(lat),
                longitude=float(lon),
            )

            for add_day in range(8):
                for hour in range(24):
                    weather = WeatherData.objects.create(
                        temperature=round(random.uniform(-5, 38), 1),
                        condition=random.choice(conditions),
                        humidity=random.randint(20, 100),
                        uv_index=random.randint(0, 11),
                    )

                    WeatherQuery.objects.create(
                        user=admin,
                        location=location,
                        weather_info=weather,
                        forecast_date=today + timedelta(days=add_day),
                        forecast_hour=hour,
                    )

        print("Mock weather data created successfully!")
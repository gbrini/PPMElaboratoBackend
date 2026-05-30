from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.weather.models import WeatherQuery
from django.utils import timezone

from datetime import timedelta
import random

user_model = get_user_model()

class Command(BaseCommand):
    help = 'Loads fake weather data for testing'

    def handle(self, *args, **kwargs):
        user = user_model.objects.first()

        if not user:
            self.stdout.write("No users found.")
            return
        
        cities = [ 'Seoul', 'Kyoto', 'Tokyo' ]
        conditions = [ 'Sunny', 'Cloudy', 'Rainy' ]

        for _ in range(20):
            WeatherQuery.objects.create(
                user=user,
                location=random.choice(cities),
                temperature=round(random.uniform(-5.0, 35.0), 1),
                condition=random.choice(conditions),
                forecast_date=timezone.now() + timedelta(days=random.randint(0, 7))
            )
        
        self.stdout.write(self.style.SUCCESS("Data inserted correctly!"))
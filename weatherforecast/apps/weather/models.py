from django.db import models
from django.conf import settings

class WeatherQuery(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='weather_queries'
    )
    location = models.CharField(max_length=50)
    temperature = models.FloatField(null=True, blank=True)
    condition = models.CharField(max_length=100, null=True, blank=True)
    forecast_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
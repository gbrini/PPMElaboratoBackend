from django.db import models
from django.conf import settings
from .constants import LOCATION_MAX_LENGTH, CONDITION_MAX_LENGTH

class WeatherLocation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='locations'
    )
    name = models.CharField(max_length=LOCATION_MAX_LENGTH)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Weather Location'
        verbose_name_plural = 'Weather locations'

class WeatherQuery(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='weather_queries'
    )
    location = models.ForeignKey(WeatherLocation, on_delete=models.CASCADE)
    temperature = models.FloatField(null=True, blank=True)
    condition = models.CharField(max_length=CONDITION_MAX_LENGTH, null=True, blank=True)
    forecast_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Weather Forecast'
        verbose_name_plural = 'Weather Forecasts'

class UserSearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='history_queries'
    )
    search_params = models.JSONField(help_text='Stores filters used')
    timestamp = models.DateTimeField(auto_now_add=True)
    result_count = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} searched at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Search Log'
        verbose_name_plural = 'Search Logs'
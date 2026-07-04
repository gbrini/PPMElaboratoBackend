from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import datetime
from .constants import LOCATION_MAX_LENGTH, CONDITION_MAX_LENGTH

class WeatherLocation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='locations'
    )
    name = models.CharField(max_length=LOCATION_MAX_LENGTH)
    country = models.CharField(max_length=2, help_text="ISO Country Code (e.g., IT, US, FR)")
    latitude = models.FloatField(null=True, blank=True, validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)])
    longitude = models.FloatField(null=True, blank=True, validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Weather Location'
        verbose_name_plural = 'Weather Locations'

class WeatherData(models.Model):
    temperature = models.FloatField(null=True, blank=True)
    condition = models.CharField(max_length=CONDITION_MAX_LENGTH, null=True, blank=True)
    humidity = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    uv_index = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = 'Detailed Weather Info'
        verbose_name_plural = 'Detailed Weather Info'

class WeatherQuery(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='weather_queries'
    )
    location = models.ForeignKey(WeatherLocation, on_delete=models.CASCADE)
    weather_info = models.OneToOneField(
        'WeatherData', 
        null=False, 
        blank=False, 
        on_delete=models.CASCADE, 
        related_name='query'
    )
    forecast_date = models.DateField(default=datetime.date.today)
    forecast_hour = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(23)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.user.role != 'admin':
            raise ValidationError("Only admins can post/put weather forecasts.")

    class Meta:
        verbose_name = 'Weather Forecast'
        verbose_name_plural = 'Weather Forecasts'
        
        unique_together = ( 'location', 'forecast_date', 'forecast_hour' )

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
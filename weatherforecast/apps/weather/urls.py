from django.urls import path
from .views import WeatherForecastView, WeatherForecastDetailView, WeatherForecastQueryHistoryView, WeatherForecastRequestTrackingView

urlpatterns = [
    path('forecast/', WeatherForecastView.as_view(), name='weather_forecast'),
    path('forecast/<int:pk>', WeatherForecastDetailView.as_view(), name='weather_forecast_detail'),
    path('forecast/history', WeatherForecastQueryHistoryView.as_view(), name='weather_forecast_history'),
    path('forecast/tracking', WeatherForecastRequestTrackingView.as_view(), name='weather_forecast_tracking')
]
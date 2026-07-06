from django.urls import path
from .views import WeatherForecastView, WeatherForecastDetailView, WeatherForecastQueryHistoryView, WeatherForecastRequestTrackingView, WeatherForecastQueryHistoryDetailView, WeatherLocationView, WeatherLocationDetailView

urlpatterns = [
    path('forecast/', WeatherForecastView.as_view(), name='weather_forecast'),
    path('forecast/<int:pk>', WeatherForecastDetailView.as_view(), name='weather_forecast_detail'),
    path('forecast/history', WeatherForecastQueryHistoryView.as_view(), name='weather_forecast_query_history'),
    path('forecast/history/<int:pk>', WeatherForecastQueryHistoryDetailView.as_view(), name='weather_forecast_query_history_detail'),
    path('forecast/tracking', WeatherForecastRequestTrackingView.as_view(), name='weather_forecast_tracking'),
    path('location/', WeatherLocationView.as_view(), name='weather_location'),
    path('location/<int:pk>', WeatherLocationDetailView.as_view(), name='weather_location_detail')
]
from django.urls import path
from .views import WeatherForecastView, WeatherForecastDetailView

urlpatterns = [
    path('forecast/', WeatherForecastView.as_view(), name='weather_forecast'),
    path('forecast/<int:pk>', WeatherForecastDetailView.as_view(), name='weather_forecast_detail')
]
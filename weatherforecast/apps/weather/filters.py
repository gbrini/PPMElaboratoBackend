from django_filters import rest_framework as filters
from .models import WeatherQuery

class WeatherQueryFilter(filters.FilterSet):
    date = filters.DateFilter(field_name="forecast_date", lookup_expr='date')
    date_range = filters.DateFromToRangeFilter(field_name="forecast_date")
    time = filters.TimeFilter(field_name="forecast_date", lookup_expr="time")
    location = filters.CharFilter(field_name="location", lookup_expr="icontains")

    class Meta:
        model = WeatherQuery
        fields = [ 'location', 'date', 'date_range', 'time' ]
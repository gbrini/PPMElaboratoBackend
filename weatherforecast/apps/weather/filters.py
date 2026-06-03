from django_filters import rest_framework as filters
from django.utils import timezone
from .models import WeatherQuery

class WeatherQueryFilter(filters.FilterSet):
    date = filters.DateFilter(field_name="forecast_date", lookup_expr='date')
    date_range = filters.DateFromToRangeFilter(field_name="forecast_date")
    time = filters.TimeFilter(field_name="forecast_date", lookup_expr="time")
    location = filters.CharFilter(field_name="location", lookup_expr="icontains", required=True)

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()

            has_date = 'date' in data
            has_range = 'date_range_before' in data or 'date_range_after' in data

            if has_range and has_date:
                data.pop('date')
            elif not has_date and not has_range:
                now = timezone.now()
                now_local = timezone.localtime(now)

                data['date'] = now_local.date().isoformat()
                data['time'] = now_local.replace(minute=0, second=0, microsecond=0).time().isoformat()

        super().__init__(data, *args, **kwargs)

    class Meta:
        model = WeatherQuery
        fields = [ 'location', 'date', 'date_range', 'time' ]
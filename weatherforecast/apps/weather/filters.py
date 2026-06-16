from django_filters import rest_framework as filters
from django.utils import timezone
from .models import WeatherQuery

class WeatherQueryFilter(filters.FilterSet):
    date = filters.DateFilter(field_name="forecast_date", lookup_expr='date')
    date_range = filters.DateFromToRangeFilter(field_name="forecast_date")
    #hour = filters.NumericRangeFilter(field_name="forecast_date", lookup_expr="hour")
    hour_min = filters.NumberFilter(field_name="forecast_date", lookup_expr="hour__gte")
    hour_max = filters.NumberFilter(field_name="forecast_date", lookup_expr="hour__lte")
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
                data['hour_min'] = now_local.hour
                data['hour_max'] = now_local.hour

        super().__init__(data, *args, **kwargs)

    @property
    def qs(self):
        parent = super().qs

        has_hour = self.data.get('hour_min') or self.data.get('hour_max')
        has_date = self.data.get('date') or self.data.get('date_range_before') or self.data.get('date_range_after')

        if has_hour and not has_date:
            raise ValidationError({
                "error": "Hour range can be set only if a specific date, or date range is provided."
            })

        return parent

    class Meta:
        model = WeatherQuery
        fields = [ 'location', 'date', 'date_range', 'hour_min', 'hour_max' ]
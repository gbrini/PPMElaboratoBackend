from django_filters import rest_framework as filters
from django.utils import timezone
from django.utils.dateparse import parse_date
from rest_framework.exceptions import ValidationError
from .models import WeatherQuery, WeatherLocation
from datetime import timedelta
from .constants import WEATHER_UNITS, MAX_DAYS_RETRIEVE

class WeatherQueryFilter(filters.FilterSet):
    date = filters.DateFilter(field_name="forecast_date")
    date_range = filters.DateFromToRangeFilter(field_name="forecast_date")
    hour_min = filters.NumberFilter(field_name="forecast_hour", lookup_expr="gte")
    hour_max = filters.NumberFilter(field_name="forecast_hour", lookup_expr="lte")
    location = filters.CharFilter(field_name="location__name", lookup_expr="iexact", required=True)
    unit = filters.ChoiceFilter(choices=WEATHER_UNITS, method='filter_by_unit')

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()

            has_date = 'date' in data
            has_range = 'date_range_before' in data or 'date_range_after' in data

            now = timezone.now()
            now_local = timezone.localtime(now)

            if has_range and has_date:
                data.pop('date')
            elif not has_date and not has_range:
                data['date'] = now_local.date().isoformat()

                if 'hour_min' not in data:
                    data['hour_min'] = now_local.hour

            if 'date_range_before' in data and 'date_range_after' not in data:
                data['date_range_after'] = now_local.date().isoformat()

            if 'date_range_after' in data and 'date_range_before' not in data:
                data['date_range_before'] = (parse_date(data['date_range_after']) + timedelta(days=MAX_DAYS_RETRIEVE)).isoformat()

        super().__init__(data, *args, **kwargs)

    @property
    def qs(self):
        data = self.data

        has_hour = 'hour_min' in data or 'hour_max' in data
        has_date = 'date' in data or 'date_range_before' in data or 'date_range_after' in data

        if has_hour and not has_date:
            raise ValidationError({
                "error": "Hour range can be set only if a specific date, or date range is provided."
            })

        hour_min = data.get('hour_min')
        hour_max = data.get('hour_max')

        if hour_min is not None and not ( 0 <= int(hour_min) <= 23 ):
            raise ValidationError({
                "hour_min": "Hour min must be between 0 and 23."
            })

        if hour_max is not None and not ( 0 <= int(hour_max) <= 23 ):
            raise ValidationError({
                "hour_max": "Hour max must be between 0 and 23."
            })

        if hour_min is not None and hour_max is not None and int(hour_min) > int(hour_max):
            raise ValidationError({
                "hour_min": "Hour min cannot be greater than hour max."
            })

        return super().qs

    def filter_by_unit(self, queryset, name, value):
        return queryset

    class Meta:
        model = WeatherQuery
        fields = [ 'location', 'date', 'date_range', 'hour_min', 'hour_max' ]

class WeatherLocationFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains", required=False)

    class Meta:
        model = WeatherLocation
        fields = [ 'name' ]
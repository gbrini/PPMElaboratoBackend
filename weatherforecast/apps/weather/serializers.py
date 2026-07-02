from rest_framework import serializers
from django.utils import timezone
from .models import WeatherQuery, UserSearchHistory, WeatherLocation
from .constants import LOCATION_MAX_LENGTH, CONDITION_MAX_LENGTH

class WeatherQueryOutputSerializer(serializers.ModelSerializer):
    temperature = serializers.SerializerMethodField()

    def get_temperature(self, obj):
        request = self.context.get('request')
        unit = request.query_params.get('unit', 'C').upper() if request else 'C'

        temp_c = obj.temperature

        if temp_c is None:
            return None

        if unit == 'F':
            return round((temp_c * 1.8) + 32, 1)
        elif unit == 'C':
            return temp_c
        else:
            return temp_c

    class Meta:
        model = WeatherQuery
        fields = [ 'id', 'location', 'temperature', 'condition', 'forecast_date', 'forecast_hour' ]

class WeatherQueryCreateSerializer(serializers.ModelSerializer):
    location_id = serializers.PrimaryKeyRelatedField(
        queryset = WeatherLocation.objects.all(),
        source = 'location',
        label="Location"
    )
    temperature = serializers.FloatField(required=True)
    condition = serializers.CharField(max_length=CONDITION_MAX_LENGTH, required=True)
    forecast_date = serializers.DateField(required=True)
    forecast_hour = serializers.IntegerField(min_value=0, max_value=23)

    class Meta:
        model = WeatherQuery
        fields = [ 'location_id', 'forecast_date', 'forecast_hour', 'temperature', 'condition' ]
    
    def validate(self, data):
        now = timezone.localtime(timezone.now())
        current_date = now.date()
        current_hour = now.hour

        input_date = data.get('forecast_date')
        input_hour = data.get('forecast_hour')

        if input_date < current_date:
            raise serializers.ValidationError({ "forecast_date": "Cannot set a forecast in the past." })

        if current_hour > input_hour and input_date == current_date:
            raise serializers.ValidationError({ "hour": "Cannot set a forecast hour that has already passed." })
            
        return data

class UserSearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSearchHistory
        fields = '__all__'

class WeatherLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherLocation
        fields = ['id', 'name', 'latitude', 'longitude']

        def validate_name(self, value):
            return value.strip().lower()
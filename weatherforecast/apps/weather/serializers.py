from rest_framework import serializers
from django.utils import timezone
from .models import WeatherQuery, UserSearchHistory, WeatherLocation, WeatherData

class WeatherLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherLocation
        fields = ['id', 'name', 'country', 'latitude', 'longitude']

        def validate_name(self, value):
            return value.strip().lower()

class WeatherDataOutputSerializer(serializers.ModelSerializer):
    temperature = serializers.SerializerMethodField(read_only=True)
    temperature_unit = serializers.SerializerMethodField()

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

    def get_temperature_unit(self, obj):
        request = self.context.get('request')
        return request.query_params.get('unit', 'C').upper() if request else 'C'

    class Meta:
        model = WeatherData
        fields = [ 'temperature', 'temperature_unit', 'condition', 'humidity', 'uv_index' ]

class WeatherDataCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = [ 'temperature', 'condition', 'humidity', 'uv_index' ]

class WeatherQueryOutputSerializer(serializers.ModelSerializer):
    weather_info = WeatherDataOutputSerializer(read_only=True)
    location = WeatherLocationSerializer(read_only=True)

    class Meta:
        model = WeatherQuery
        fields = [ 'id', 'location', 'weather_info', 'forecast_date', 'forecast_hour' ]

class WeatherQueryCreateSerializer(serializers.ModelSerializer):
    location_id = serializers.PrimaryKeyRelatedField(
        queryset = WeatherLocation.objects.all(),
        source = 'location',
        label="Location"
    )
    weather_info = WeatherDataCreateSerializer(required=True)
    forecast_date = serializers.DateField(required=True)
    forecast_hour = serializers.IntegerField(min_value=0, max_value=23)

    class Meta:
        model = WeatherQuery
        fields = [ 'location_id', 'forecast_date', 'forecast_hour', 'weather_info' ]
    
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

    def create(self, validated_data):
        weather_info_data = validated_data.pop('weather_info')
        weather_info = WeatherData.objects.create(**weather_info_data)

        return WeatherQuery.objects.create(weather_info=weather_info, **validated_data)

    def update(self, instance, validated_data):
        weather_info_data = validated_data.pop('weather_info', None)

        instance.location = validated_data.get('location', instance.location)
        instance.forecast_date = validated_data.get('forecast_date', instance.forecast_date)
        instance.forecast_hour = validated_data.get('forecast_hour', instance.forecast_hour)
        instance.save()

        if weather_info_data:
            weather_info = instance.weather_info

            for attr, value in weather_info_data.items():
                setattr(weather_info, attr, value)
            weather_info.save()

        return instance

class UserSearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSearchHistory
        fields = '__all__'
from rest_framework import serializers
from .models import WeatherQuery

class WeatherQueryInputSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=50, required=True)
    date = serializers.DateField(required=False)
    time = serializers.TimeField(required=False)

class WeatherQueryOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherQuery
        fields = [ 'id', 'location', 'temperature', 'condition', 'forecast_date' ]

class WeatherQueryCreateSerializer(serializers.ModelSerializer):
    location = serializers.CharField(max_length=50)
    temperature = serializers.FloatField(required=True)
    condition = serializers.CharField(max_length=100, required=True)
    forecast_date = serializers.DateTimeField(required=True)

    class Meta:
        model = WeatherQuery
        fields = [ 'location', 'forecast_date', 'temperature', 'condition' ]
    
    def validate_forecast_date(self, value):
        return value.replace(second = 0, microsecond = 0)
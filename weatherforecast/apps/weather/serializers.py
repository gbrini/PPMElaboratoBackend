from rest_framework import serializers
from .models import WeatherQuery, UserSearchHistory

class WeatherQueryInputSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=50, required=True)
    date = serializers.DateField(required=False)
    time = serializers.TimeField(required=False)

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

class UserSearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSearchHistory
        fields = '__all__'
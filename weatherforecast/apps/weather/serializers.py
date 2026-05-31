from rest_framework import serializers
from .models import WeatherQuery

class WeatherQueryInputSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=50, required=True)
    date = serializers.DateField(required=False)
    time = serializers.TimeField(required=False)

class WeatherQueryOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherQuery
        # fields = '__all__'
        exclude = [ 'user' ]
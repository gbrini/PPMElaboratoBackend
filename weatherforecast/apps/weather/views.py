from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import WeatherQueryInputSerializer, WeatherQueryOutputSerializer
from .models import WeatherQuery

class WeatherForecastView(APIView):
    permission_classes = [ AllowAny ]

    #def get_throttles(self)

    def get(self, request):
        input_serializer = WeatherQueryInputSerializer(data=request.query_params)

        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=400)

        location = input_serializer.validated_data['location']

        weather_data = WeatherQuery.objects.filter(location=location)

        output_serializer = WeatherQueryOutputSerializer(weather_data, many=True)

        return Response(output_serializer.data)
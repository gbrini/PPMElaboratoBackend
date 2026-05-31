from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import WeatherQueryInputSerializer, WeatherQueryOutputSerializer, WeatherQueryCreateSerializer
from .models import WeatherQuery
from ..users.permissions import IsAdminUser

from datetime import timedelta, datetime

class WeatherForecastView(APIView):
    permission_classes = [ AllowAny ]

    #def get_throttles(self)

    def get_permissions(self):
        if self.request.method in [ 'POST', 'DELETE' ]:
            return [ IsAdminUser() ]

        return super().get_permissions()

    def get(self, request):
        input_serializer = WeatherQueryInputSerializer(data=request.query_params)

        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = input_serializer.validated_data

        location = data['location']

        weather_data = WeatherQuery.objects.filter(location=location)

        if data.get('date'):
            weather_data = weather_data.filter(forecast_date__date = data['date'])

        if data.get('time'):
            time = data['time']

            weather_data = weather_data.filter(forecast_date__hour = time.hour)

        output_serializer = WeatherQueryOutputSerializer(weather_data, many=True)

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WeatherQueryCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.save(user=request.user)
        
        output_serializer = WeatherQueryOutputSerializer(instance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        return Response()
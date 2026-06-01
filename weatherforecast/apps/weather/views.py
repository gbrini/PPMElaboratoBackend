from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import WeatherQueryInputSerializer, WeatherQueryOutputSerializer, WeatherQueryCreateSerializer
from .models import WeatherQuery, UserSearchHistory
from ..users.permissions import IsAdminUser

from datetime import timedelta, datetime

class WeatherForecastView(APIView):
    permission_classes = [ AllowAny ]

    #def get_throttles(self)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [ IsAdminUser() ]

        return super().get_permissions()

    def get(self, request):
        input_serializer = WeatherQueryInputSerializer(data=request.query_params)

        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.user.role == 'premium':
            UserSearchHistory.objects.create(
                role=request.user,
                search_fields=request.query_params
            )

        data = input_serializer.validated_data

        location = data['location']

        weather_data = WeatherQuery.objects.filter(location=location)

        if data.get('date'):
            weather_data = weather_data.filter(forecast_date__date = data['date'])

        if data.get('time'):
            time = data['time']

            weather_data = weather_data.filter(forecast_date__hour = time.hour)

            if time.minute != 0:
                weather_data = weather_data.filter(forecast_date__minute = time.minute)

        output_serializer = WeatherQueryOutputSerializer(weather_data, many=True)

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WeatherQueryCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.save(user=request.user)
        
        output_serializer = WeatherQueryOutputSerializer(instance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

class WeatherForecastDetailView(APIView):
    permission_classes = [ AllowAny ]

    #def get_throttles(self)

    def get_permissions(self):
        if self.request.method in [ 'DELETE', 'PUT' ]:
            return [ IsAdminUser() ]

        return super().get_permissions()

    def delete(self, request, pk):
        forecast = get_object_or_404(WeatherQuery, pk=pk)

        forecast.delete()

        return Response({ "message": "Forecast deleted successfully!" }, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        forecast = get_object_or_404(WeatherQuery, pk=pk)

        serializer = WeatherQueryCreateSerializer(forecast, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.save()

        output_serializer = WeatherQueryOutputSerializer(instance)

        return Response(output_serializer.data, status=status.HTTP_200_OK)
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import WeatherQueryInputSerializer

class WeatherForecastView(APIView):
    permission_classes = [ AllowAny ]

    def get(self, request):
        input_serializer = WeatherQueryInputSerializer(data=request.query_params)

        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=400)

        location = request.query_params.get('location')

        return Response({
            "message": f"You searched for {location}"
        })
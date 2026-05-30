from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class WeatherForecastView(APIView):
    permission_classes = [ AllowAny ]

    def get(self, request):
        location = request.query_params.get('location')

        return Response({
            "message": f"You searched for {location}"
        })
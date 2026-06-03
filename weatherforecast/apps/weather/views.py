from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDate

from .serializers import WeatherQueryInputSerializer, WeatherQueryOutputSerializer, WeatherQueryCreateSerializer, UserSearchHistorySerializer
from .models import WeatherQuery, UserSearchHistory
from .filters import WeatherQueryFilter
from ..users.permissions import IsAdminUser, IsPremiumUser

from datetime import timedelta, datetime

class WeatherForecastView(APIView):
    permission_classes = [ AllowAny ]

    #def get_throttles(self)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [ IsAdminUser() ]

        return super().get_permissions()

    def get(self, request):
        filter_backend = WeatherQueryFilter(request.query_params, queryset=WeatherQuery.objects.all())
        filtered_queryset = filter_backend.qs

        paginator = PageNumberPagination()
        paginator.page_size = 25

        result_page = paginator.paginate_queryset(filtered_queryset, request)

        if request.user.is_authenticated and request.user.role in [ 'premium', 'admin' ]:
            UserSearchHistory.objects.create(
                user=request.user,
                search_params=request.query_params
            )

        output_serializer = WeatherQueryOutputSerializer(result_page, many=True)

        return paginator.get_paginated_response(output_serializer.data)

    def post(self, request):
        serializer = WeatherQueryCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.save(user=request.user)
        
        output_serializer = WeatherQueryOutputSerializer(instance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

class WeatherForecastDetailView(APIView):
    permission_classes = [ IsAdminUser ]

    #def get_throttles(self)

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

class WeatherForecastQueryHistoryView(APIView):
    permission_classes = [ IsAdminUser | IsPremiumUser ]

    def get(self, request):
        data = UserSearchHistory.objects.filter(user=request.user).order_by("-timestamp")

        paginator = PageNumberPagination()
        paginator.page_size = 25

        result_page = paginator.paginate_queryset(data, request)

        output_serializer = UserSearchHistorySerializer(result_page, many=True)

        return paginator.get_paginated_response(output_serializer.data)

class WeatherForecastQueryHistoryDetailView(APIView):
    permission_classes = [ IsAdminUser | IsPremiumUser ]

    def get(self, request, pk):
        data = get_object_or_404(UserSearchHistory, pk=pk, user=request.user)

        output_serializer = UserSearchHistorySerializer(data)

        return Response(output_serializer.data, status=status.HTTP_200_OK)

class WeatherForecastRequestTrackingView(APIView):
    permission_classes = [ IsAdminUser | IsPremiumUser ]

    def get(self, request):
        days_number = 30

        if request.query_params.get("today", "false").lower() == "true":
            days_number = 1

        days = timezone.now() - timedelta(days=days_number)

        daily_count = (
            UserSearchHistory.objects.filter(user=request.user, timestamp__gte=days)
            .annotate(date=TruncDate('timestamp'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('-date')
        )

        return Response(daily_count)
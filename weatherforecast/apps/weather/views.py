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

from .serializers import WeatherQueryOutputSerializer, WeatherQueryCreateSerializer, UserSearchHistorySerializer, WeatherLocationSerializer
from .models import WeatherQuery, UserSearchHistory, WeatherLocation
from .filters import WeatherQueryFilter, WeatherLocationFilter
from ..users.permissions import IsAdminUser, IsPremiumUser
from .constants import PAGE_SIZE, MAX_PAGE_SIZE, TRACKING_DAYS

from datetime import timedelta, datetime

class StandardResultsSetPagination(PageNumberPagination):
    page_size = PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = MAX_PAGE_SIZE

class WeatherForecastView(APIView):
    permission_classes = [ AllowAny ]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [ IsAdminUser() ]

        return super().get_permissions()

    def get(self, request):
        filter_backend = WeatherQueryFilter(request.query_params, queryset=WeatherQuery.objects.all().order_by("forecast_date", "forecast_hour"))
        
        if not filter_backend.is_valid():
            return Response(filter_backend.errors, status=status.HTTP_400_BAD_REQUEST)
        
        filtered_queryset = filter_backend.qs

        paginator = StandardResultsSetPagination()

        result_page = paginator.paginate_queryset(filtered_queryset, request)

        json_serialized_params = {}

        for k, v in filter_backend.form.cleaned_data.items():
            if v is None:
                json_serialized_params[k] = None
            elif hasattr(v, 'isoformat'):
                json_serialized_params[k] = v.isoformat()
            elif isinstance(v, slice):
                json_serialized_params[k] = { 
                    "start": v.start.isoformat() if v.start is not None else None, 
                    "stop": v.stop.isoformat() if v.stop is not None else None 
                }
            elif isinstance(v, (str, int, float, bool)):
                json_serialized_params[k] = v
            else:
                json_serialized_params[k] = str(v)
        
        if request.user.is_authenticated and request.user.role in [ 'premium', 'admin' ]:
            UserSearchHistory.objects.create(
                user=request.user,
                search_params=json_serialized_params,
                result_count=paginator.page.paginator.count
            )

        output_serializer = WeatherQueryOutputSerializer(result_page, many=True, context = { "request": request })

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

        paginator = StandardResultsSetPagination()

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
        days_number = TRACKING_DAYS

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

        for obj in daily_count:
            if obj['date'] == datetime.today().date():
                obj['throttle_rate'] = request.user.getMaximumRequestsNumber()
                break

        return Response(daily_count)

class WeatherLocationView(APIView):
    permission_classes = [ AllowAny ]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [ IsAdminUser() ]

        return super().get_permissions()

    def get(self, request):
        filter_backend = WeatherLocationFilter(request.query_params, queryset=WeatherLocation.objects.all().order_by("-name"))
        
        if not filter_backend.is_valid():
            return Response(filter_backend.errors, status=status.HTTP_400_BAD_REQUEST)
        
        filtered_queryset = filter_backend.qs

        paginator = StandardResultsSetPagination()

        result_page = paginator.paginate_queryset(filtered_queryset, request)

        output_serializer = WeatherLocationSerializer(result_page, many=True, context = { "request": request })

        return paginator.get_paginated_response(output_serializer.data)

    def post(self, request):
        serializer = WeatherLocationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.save(user=request.user)
        
        output_serializer = WeatherLocationSerializer(instance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
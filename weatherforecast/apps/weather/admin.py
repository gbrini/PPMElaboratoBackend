from django.contrib import admin

from .models import WeatherQuery

@admin.register(WeatherQuery)
class WeatherQueryAdmin(admin.ModelAdmin):
    list_display = ( 'location', 'forecast_date', 'temperature', 'condition', 'created_at', 'user', )

    list_display_links = ( 'location', )

    list_filter = ( 'user', 'forecast_date', )

    search_fields = ( 'location', 'user__username', )
from django.contrib import admin

from .models import WeatherQuery, UserSearchHistory, WeatherLocation

@admin.register(WeatherQuery)
class WeatherQueryAdmin(admin.ModelAdmin):
    list_display = ( 'location', 'forecast_date', 'temperature', 'condition', 'created_at', 'user', )

    list_display_links = ( 'location', )

    list_filter = ( 'user', 'forecast_date', )

    search_fields = ( 'location', 'user__username', )

@admin.register(UserSearchHistory)
class UserSearchHistoryAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

    list_display = ( 'user', 'result_count', 'search_params', 'timestamp', )

    readony_fields = ( 'user', 'result_count', 'search_params', 'timestamp', )

    list_display_links = ( 'user', )

    list_filter = ( 'user', 'timestamp', )

    search_fields = ( 'user__username', )


@admin.register(WeatherLocation)
class LocationAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'latitude', 'longitude' )

    list_display_links = ( 'name', )

    list_filter = ( 'name', )

    search_fields = ( 'name', )
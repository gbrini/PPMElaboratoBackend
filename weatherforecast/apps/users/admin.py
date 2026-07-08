from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ( 'id', 'username', 'role', 'date_joined', 'last_login', 'created_at', 'updated_at' )

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', { 'fields': ('role',) }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', { 'fields': ('role',) }),
    )
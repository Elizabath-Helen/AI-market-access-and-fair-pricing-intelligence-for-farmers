"""
Admin configuration for core app.
"""

from django.contrib import admin
from .models import FarmerQuery


@admin.register(FarmerQuery)
class FarmerQueryAdmin(admin.ModelAdmin):
    list_display = ['crop_type', 'location', 'quantity', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['crop_type', 'location', 'session_id']
    readonly_fields = ['id', 'created_at']

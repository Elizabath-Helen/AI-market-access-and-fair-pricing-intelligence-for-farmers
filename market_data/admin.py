"""
Admin configuration for market_data app.
"""

from django.contrib import admin
from .models import Market, MarketPrice, TransportCost


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'mandi_code', 'active']
    list_filter = ['active', 'region']
    search_fields = ['name', 'mandi_code', 'region']


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ['crop_type', 'market', 'date', 'modal_price', 'min_price', 'max_price']
    list_filter = ['date', 'crop_type']
    search_fields = ['crop_type', 'market__name']
    date_hierarchy = 'date'


@admin.register(TransportCost)
class TransportCostAdmin(admin.ModelAdmin):
    list_display = ['from_location', 'to_market', 'distance_km', 'cost_per_kg', 'last_updated']
    search_fields = ['from_location', 'to_market__name']

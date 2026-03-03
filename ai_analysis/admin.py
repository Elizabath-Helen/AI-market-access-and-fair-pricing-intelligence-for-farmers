"""
Admin configuration for ai_analysis app.
"""

from django.contrib import admin
from .models import PriceAnalysis, MarketRecommendation


@admin.register(PriceAnalysis)
class PriceAnalysisAdmin(admin.ModelAdmin):
    list_display = ['query', 'fair_price_min', 'fair_price_max', 'confidence_score', 'created_at']
    search_fields = ['query__crop_type', 'query__location']
    readonly_fields = ['id', 'created_at']


@admin.register(MarketRecommendation)
class MarketRecommendationAdmin(admin.ModelAdmin):
    list_display = ['query', 'market', 'rank', 'expected_price', 'net_profit', 'created_at']
    list_filter = ['rank']
    search_fields = ['query__crop_type', 'market__name']
    readonly_fields = ['id', 'created_at']

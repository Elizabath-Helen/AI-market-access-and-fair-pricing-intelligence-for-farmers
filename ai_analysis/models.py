"""
AI analysis models for Farmer Market Advisor.
"""

from django.db import models
import uuid
from core.models import FarmerQuery
from market_data.models import Market


class PriceAnalysis(models.Model):
    """
    Represents AI-generated price analysis for a farmer query.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query = models.OneToOneField(FarmerQuery, on_delete=models.CASCADE, related_name='price_analysis')
    fair_price_min = models.DecimalField(max_digits=10, decimal_places=2)
    fair_price_max = models.DecimalField(max_digits=10, decimal_places=2)
    confidence_score = models.FloatField(help_text="Confidence score between 0 and 1")
    factors_considered = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'price_analyses'
        verbose_name_plural = 'Price analyses'

    def __str__(self):
        return f"Price Analysis for {self.query.crop_type}: ₹{self.fair_price_min}-{self.fair_price_max}"


class MarketRecommendation(models.Model):
    """
    Represents a market recommendation for a farmer query.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    query = models.ForeignKey(FarmerQuery, on_delete=models.CASCADE, related_name='recommendations')
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    expected_price = models.DecimalField(max_digits=10, decimal_places=2)
    transport_cost = models.DecimalField(max_digits=10, decimal_places=2)
    net_profit = models.DecimalField(max_digits=10, decimal_places=2)
    rank = models.IntegerField()
    reasoning = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'market_recommendations'
        ordering = ['query', 'rank']
        indexes = [
            models.Index(fields=['query', 'rank']),
        ]

    def __str__(self):
        return f"Rank {self.rank}: {self.market.name} - Net Profit: ₹{self.net_profit}"

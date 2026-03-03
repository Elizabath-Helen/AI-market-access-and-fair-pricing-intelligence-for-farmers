"""
Market data models for Farmer Market Advisor.
"""

from django.db import models
import uuid


class Market(models.Model):
    """
    Represents a market (mandi) where produce is traded.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, help_text="Latitude, longitude")
    mandi_code = models.CharField(max_length=50, unique=True)
    region = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'markets'
        indexes = [
            models.Index(fields=['mandi_code']),
            models.Index(fields=['region']),
        ]

    def __str__(self):
        return f"{self.name} ({self.region})"


class MarketPrice(models.Model):
    """
    Represents price data for a specific crop at a market.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='prices')
    crop_type = models.CharField(max_length=100)
    date = models.DateField()
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    modal_price = models.DecimalField(max_digits=10, decimal_places=2)
    arrivals = models.IntegerField(help_text="Quantity arrived at market")
    source = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'market_prices'
        ordering = ['-date']
        indexes = [
            models.Index(fields=['crop_type', '-date']),
            models.Index(fields=['market', 'crop_type']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(min_price__lte=models.F('modal_price')) & 
                      models.Q(modal_price__lte=models.F('max_price')),
                name='price_range_constraint'
            ),
        ]

    def __str__(self):
        return f"{self.crop_type} at {self.market.name} on {self.date}"


class TransportCost(models.Model):
    """
    Represents transport cost from a location to a market.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_location = models.CharField(max_length=255)
    to_market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='transport_costs')
    distance_km = models.DecimalField(max_digits=10, decimal_places=2)
    cost_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transport_costs'
        unique_together = ['from_location', 'to_market']
        constraints = [
            models.CheckConstraint(
                check=models.Q(distance_km__gte=0),
                name='distance_non_negative'
            ),
            models.CheckConstraint(
                check=models.Q(cost_per_kg__gte=0),
                name='cost_non_negative'
            ),
        ]

    def __str__(self):
        return f"{self.from_location} to {self.to_market.name}: ₹{self.cost_per_kg}/kg"

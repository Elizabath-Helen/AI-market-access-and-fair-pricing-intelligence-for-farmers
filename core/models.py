"""
Core app models for Farmer Market Advisor.
"""

from django.db import models
import uuid


class FarmerQuery(models.Model):
    """
    Represents a farmer's query for market recommendations.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    crop_type = models.CharField(max_length=100)
    location = models.CharField(max_length=255, help_text="Latitude, longitude or place name")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantity in kg or quintals")
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        db_table = 'farmer_queries'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['session_id', '-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.crop_type} - {self.location} ({self.status})"


class CropRecommendation(models.Model):
    """
    Represents a crop recommendation based on land analysis.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    land_image = models.ImageField(upload_to='land_images/', null=True, blank=True)
    location = models.CharField(max_length=255, help_text="Location for weather data")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Weather data
    temperature = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    humidity = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    rainfall = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    soil_type = models.CharField(max_length=100, null=True, blank=True)
    
    # Analysis results
    recommended_crops = models.JSONField(default=list)
    analysis_data = models.JSONField(default=dict)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='completed')
    
    class Meta:
        db_table = 'crop_recommendations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['session_id', '-created_at']),
        ]
    
    def __str__(self):
        return f"Crop Recommendation for {self.location} - {self.created_at.strftime('%Y-%m-%d')}"


class ProfitAnalysis(models.Model):
    """
    Represents a profit maximization analysis for a farmer.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Farmer inputs
    crop_type = models.CharField(max_length=100)
    land_area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Land area in acres")
    total_yield = models.DecimalField(max_digits=12, decimal_places=2, help_text="Total yield in kg")
    
    # Cost breakdown
    seed_cost = models.DecimalField(max_digits=10, decimal_places=2)
    fertilizer_cost = models.DecimalField(max_digits=10, decimal_places=2)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2)
    irrigation_cost = models.DecimalField(max_digits=10, decimal_places=2)
    other_costs = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Market info
    current_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Current market price per kg")
    storage_capacity = models.CharField(max_length=100)
    immediate_need = models.CharField(max_length=100)
    processing_interest = models.CharField(max_length=100)
    
    # Analysis results
    current_situation = models.JSONField(default=dict)
    strategies = models.JSONField(default=list)
    summary = models.JSONField(default=dict)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20, default='completed')
    
    class Meta:
        db_table = 'profit_analyses'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['session_id', '-created_at']),
            models.Index(fields=['crop_type']),
        ]
    
    def __str__(self):
        return f"Profit Analysis for {self.crop_type} - {self.created_at.strftime('%Y-%m-%d')}"

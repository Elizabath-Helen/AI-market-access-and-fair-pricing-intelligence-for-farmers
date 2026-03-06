"""
Forms for the core app.
"""

from django import forms
from .models import FarmerQuery, CropRecommendation, ProfitAnalysis, NegotiationAnalysis


class FarmerQueryForm(forms.ModelForm):
    """Form for farmer to input crop query."""
    
    CROP_CHOICES = [
        ('', 'Select your crop...'),
        ('Wheat', 'Wheat'),
        ('Rice', 'Rice'),
        ('Tomato', 'Tomato'),
        ('Potato', 'Potato'),
        ('Onion', 'Onion'),
        ('Cotton', 'Cotton'),
        ('Sugarcane', 'Sugarcane'),
        ('Maize', 'Maize'),
        ('Soybean', 'Soybean'),
        ('Groundnut', 'Groundnut'),
    ]
    
    crop_type = forms.ChoiceField(
        choices=CROP_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'crop_type'
        }),
        required=True
    )
    
    location = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'location',
            'placeholder': 'e.g., Delhi, Mumbai, or coordinates'
        }),
        help_text='Enter your city name or coordinates (latitude, longitude)',
        required=True
    )
    
    quantity = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'quantity',
            'placeholder': 'e.g., 100',
            'step': '0.01',
            'min': '0.01'
        }),
        help_text='Enter the quantity you want to sell (in kg)',
        required=True
    )
    
    class Meta:
        model = FarmerQuery
        fields = ['crop_type', 'location', 'quantity']


class CropRecommendationForm(forms.ModelForm):
    """Form for crop recommendation based on land analysis."""
    
    SOIL_TYPE_CHOICES = [
        ('', 'Select soil type...'),
        ('Alluvial', 'Alluvial Soil'),
        ('Black', 'Black Soil (Regur)'),
        ('Red', 'Red Soil'),
        ('Laterite', 'Laterite Soil'),
        ('Desert', 'Desert/Arid Soil'),
        ('Mountain', 'Mountain Soil'),
        ('Clay', 'Clay Soil'),
        ('Sandy', 'Sandy Soil'),
        ('Loamy', 'Loamy Soil'),
    ]
    
    land_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'id': 'land_image',
            'accept': 'image/*'
        }),
        help_text='Upload an image of your land (optional)'
    )
    
    location = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'location_crop',
            'placeholder': 'e.g., Delhi, Mumbai'
        }),
        help_text='Enter your location for weather data',
        required=True
    )
    
    soil_type = forms.ChoiceField(
        choices=SOIL_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'soil_type'
        }),
        required=False,
        help_text='Select your soil type if known'
    )
    
    class Meta:
        model = CropRecommendation
        fields = ['land_image', 'location', 'soil_type']



class ProfitAnalysisForm(forms.ModelForm):
    """Form for profit analysis questionnaire."""
    
    CROP_CHOICES = [
        ('', 'Select your crop...'),
        ('Wheat', 'Wheat'),
        ('Rice', 'Rice'),
        ('Cotton', 'Cotton'),
        ('Sugarcane', 'Sugarcane'),
        ('Maize', 'Maize'),
        ('Soybean', 'Soybean'),
        ('Groundnut', 'Groundnut'),
        ('Potato', 'Potato'),
        ('Tomato', 'Tomato'),
        ('Onion', 'Onion'),
        ('Other', 'Other'),
    ]
    
    STORAGE_CHOICES = [
        ('Yes, good storage', 'Yes, good storage'),
        ('Yes, limited storage', 'Yes, limited storage'),
        ('No storage', 'No storage'),
    ]
    
    NEED_CHOICES = [
        ('Yes, urgently', 'Yes, urgently'),
        ('Within 1-2 months', 'Within 1-2 months'),
        ('No, can wait', 'No, can wait'),
    ]
    
    PROCESSING_CHOICES = [
        ('Yes, very interested', 'Yes, very interested'),
        ('Maybe, need more info', 'Maybe, need more info'),
        ('No, prefer raw sale', 'No, prefer raw sale'),
    ]
    
    crop_type = forms.ChoiceField(
        choices=CROP_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="What crop did you cultivate this season?",
        required=True
    )
    
    land_area = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
        label="How much land do you have (in acres)?",
        required=True
    )
    
    total_yield = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        label="What was your total yield this year (in kg)?",
        required=True
    )
    
    seed_cost = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        label="How much did you spend on seeds (₹)?",
        required=True
    )
    
    fertilizer_cost = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        label="How much did you spend on fertilizers and pesticides (₹)?",
        required=True
    )
    
    labor_cost = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        label="How much did you spend on labor (₹)?",
        required=True
    )
    
    irrigation_cost = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        label="How much did you spend on irrigation/water (₹)?",
        required=True
    )
    
    other_costs = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        label="Any other expenses like transport, equipment rental (₹)?",
        required=False,
        initial=0
    )
    
    current_price = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        label="What is the current market price for your crop (₹/kg)?",
        required=True
    )
    
    storage_capacity = forms.ChoiceField(
        choices=STORAGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Do you have storage facilities?",
        required=True
    )
    
    immediate_need = forms.ChoiceField(
        choices=NEED_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Do you need money immediately?",
        required=True
    )
    
    processing_interest = forms.ChoiceField(
        choices=PROCESSING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Are you interested in value-added processing?",
        required=True
    )
    
    class Meta:
        model = ProfitAnalysis
        fields = [
            'crop_type', 'land_area', 'total_yield',
            'seed_cost', 'fertilizer_cost', 'labor_cost', 'irrigation_cost', 'other_costs',
            'current_price', 'storage_capacity', 'immediate_need', 'processing_interest'
        ]


class NegotiationAnalysisForm(forms.ModelForm):
    """Form for negotiation analysis input."""
    
    CROP_CHOICES = [
        ('', 'Select your crop...'),
        ('Wheat', 'Wheat'),
        ('Rice', 'Rice'),
        ('Cotton', 'Cotton'),
        ('Sugarcane', 'Sugarcane'),
        ('Maize', 'Maize'),
        ('Soybean', 'Soybean'),
        ('Groundnut', 'Groundnut'),
        ('Potato', 'Potato'),
        ('Tomato', 'Tomato'),
        ('Onion', 'Onion'),
        ('Other', 'Other'),
    ]
    
    crop_type = forms.ChoiceField(
        choices=CROP_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="What crop are you selling?",
        required=True
    )
    
    farmer_location = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Amritsar, Punjab'
        }),
        label="Your location (City, State)",
        required=True
    )
    
    quantity = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0.1',
            'placeholder': 'e.g., 50'
        }),
        label="Quantity you want to sell (in quintals)",
        help_text="1 quintal = 100 kg",
        required=True
    )
    
    offered_price = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0',
            'placeholder': 'e.g., 2300'
        }),
        label="Price offered by buyer (₹ per quintal)",
        required=True
    )
    
    nearby_market_prices_text = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 2400, 2350, 2380'
        }),
        label="Nearby mandi prices (₹ per quintal, comma separated)",
        help_text="Enter recent prices from nearby mandis, separated by commas",
        required=False
    )
    
    class Meta:
        model = NegotiationAnalysis
        fields = ['crop_type', 'farmer_location', 'quantity', 'offered_price']
    
    def clean_nearby_market_prices_text(self):
        """Convert comma-separated prices to list of floats."""
        prices_text = self.cleaned_data.get('nearby_market_prices_text', '')
        
        if not prices_text.strip():
            return []
        
        try:
            prices = [float(price.strip()) for price in prices_text.split(',') if price.strip()]
            
            # Validate prices are reasonable
            for price in prices:
                if price <= 0 or price > 100000:
                    raise forms.ValidationError("Please enter reasonable price values (between ₹1 and ₹100,000)")
            
            return prices
        except ValueError:
            raise forms.ValidationError("Please enter valid numbers separated by commas (e.g., 2400, 2350, 2380)")
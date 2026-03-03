"""
Crop recommendation service based on climatic conditions and land analysis.
"""

import requests
from decimal import Decimal
from typing import Dict, List, Tuple
import random


class CropAdvisorService:
    """Service for analyzing land and recommending crops."""
    
    # Crop database with requirements and profitability
    CROP_DATABASE = {
        'Rice': {
            'temp_range': (20, 35),
            'rainfall_min': 1000,
            'humidity_min': 60,
            'soil_types': ['Alluvial', 'Clay', 'Loamy'],
            'yield_per_hectare': 3500,  # kg
            'price_per_kg': 30,
            'season': 'Kharif (Monsoon)',
            'growth_period': '120-150 days'
        },
        'Wheat': {
            'temp_range': (10, 25),
            'rainfall_min': 500,
            'humidity_min': 50,
            'soil_types': ['Alluvial', 'Loamy', 'Clay'],
            'yield_per_hectare': 3000,
            'price_per_kg': 25,
            'season': 'Rabi (Winter)',
            'growth_period': '120-140 days'
        },
        'Cotton': {
            'temp_range': (21, 30),
            'rainfall_min': 600,
            'humidity_min': 60,
            'soil_types': ['Black', 'Alluvial', 'Red'],
            'yield_per_hectare': 2000,
            'price_per_kg': 50,
            'season': 'Kharif (Monsoon)',
            'growth_period': '180-200 days'
        },
        'Sugarcane': {
            'temp_range': (20, 35),
            'rainfall_min': 1000,
            'humidity_min': 70,
            'soil_types': ['Alluvial', 'Loamy', 'Clay'],
            'yield_per_hectare': 70000,
            'price_per_kg': 28,
            'season': 'Year-round',
            'growth_period': '12-18 months'
        },
        'Maize': {
            'temp_range': (18, 27),
            'rainfall_min': 600,
            'humidity_min': 55,
            'soil_types': ['Alluvial', 'Loamy', 'Red'],
            'yield_per_hectare': 2500,
            'price_per_kg': 22,
            'season': 'Kharif & Rabi',
            'growth_period': '90-120 days'
        },
        'Soybean': {
            'temp_range': (20, 30),
            'rainfall_min': 500,
            'humidity_min': 60,
            'soil_types': ['Black', 'Alluvial', 'Red'],
            'yield_per_hectare': 1500,
            'price_per_kg': 45,
            'season': 'Kharif (Monsoon)',
            'growth_period': '90-120 days'
        },
        'Groundnut': {
            'temp_range': (20, 30),
            'rainfall_min': 500,
            'humidity_min': 55,
            'soil_types': ['Sandy', 'Loamy', 'Red'],
            'yield_per_hectare': 1800,
            'price_per_kg': 55,
            'season': 'Kharif & Rabi',
            'growth_period': '100-150 days'
        },
        'Potato': {
            'temp_range': (15, 25),
            'rainfall_min': 500,
            'humidity_min': 60,
            'soil_types': ['Loamy', 'Sandy', 'Alluvial'],
            'yield_per_hectare': 25000,
            'price_per_kg': 15,
            'season': 'Rabi (Winter)',
            'growth_period': '90-120 days'
        },
        'Tomato': {
            'temp_range': (18, 27),
            'rainfall_min': 400,
            'humidity_min': 60,
            'soil_types': ['Loamy', 'Sandy', 'Red'],
            'yield_per_hectare': 30000,
            'price_per_kg': 20,
            'season': 'Year-round',
            'growth_period': '90-120 days'
        },
        'Onion': {
            'temp_range': (15, 25),
            'rainfall_min': 400,
            'humidity_min': 55,
            'soil_types': ['Loamy', 'Sandy', 'Alluvial'],
            'yield_per_hectare': 20000,
            'price_per_kg': 18,
            'season': 'Rabi (Winter)',
            'growth_period': '120-150 days'
        },
    }
    
    def get_weather_data(self, location: str) -> Dict:
        """
        Fetch weather data for a location.
        Uses OpenWeatherMap API (free tier).
        """
        # For demo purposes, return mock data
        # In production, use: api.openweathermap.org/data/2.5/weather
        
        # Mock weather data based on location
        mock_weather = {
            'Delhi': {'temp': 28, 'humidity': 65, 'rainfall': 800},
            'Mumbai': {'temp': 30, 'humidity': 75, 'rainfall': 2400},
            'Bangalore': {'temp': 24, 'humidity': 70, 'rainfall': 900},
            'Kolkata': {'temp': 29, 'humidity': 80, 'rainfall': 1600},
            'Chennai': {'temp': 31, 'humidity': 78, 'rainfall': 1400},
            'Hyderabad': {'temp': 27, 'humidity': 68, 'rainfall': 800},
            'Pune': {'temp': 26, 'humidity': 65, 'rainfall': 700},
            'Jaipur': {'temp': 29, 'humidity': 55, 'rainfall': 600},
        }
        
        # Try to match location
        for city, data in mock_weather.items():
            if city.lower() in location.lower():
                return data
        
        # Default weather data
        return {
            'temp': random.randint(20, 32),
            'humidity': random.randint(55, 80),
            'rainfall': random.randint(500, 1500)
        }
    
    def analyze_land_image(self, image_path: str) -> Dict:
        """
        Analyze land image to determine soil characteristics.
        In production, this would use computer vision/ML models.
        """
        # Mock analysis for demo
        return {
            'soil_color': 'brown',
            'vegetation_cover': random.randint(10, 80),
            'moisture_level': random.choice(['low', 'medium', 'high']),
            'terrain': random.choice(['flat', 'slightly_sloped', 'hilly']),
            'estimated_soil_type': random.choice(['Loamy', 'Clay', 'Sandy', 'Alluvial'])
        }
    
    def calculate_suitability_score(
        self, 
        crop_name: str, 
        crop_data: Dict, 
        weather: Dict, 
        soil_type: str = None
    ) -> Tuple[float, List[str]]:
        """
        Calculate how suitable a crop is for given conditions.
        Returns (score, reasons).
        """
        score = 100.0
        reasons = []
        
        # Temperature suitability
        temp = weather['temp']
        temp_min, temp_max = crop_data['temp_range']
        if temp_min <= temp <= temp_max:
            reasons.append(f"✓ Temperature ({temp}°C) is ideal")
        elif temp < temp_min:
            penalty = (temp_min - temp) * 5
            score -= penalty
            reasons.append(f"⚠ Temperature is {temp_min - temp}°C below optimal")
        else:
            penalty = (temp - temp_max) * 5
            score -= penalty
            reasons.append(f"⚠ Temperature is {temp - temp_max}°C above optimal")
        
        # Rainfall suitability
        rainfall = weather['rainfall']
        if rainfall >= crop_data['rainfall_min']:
            reasons.append(f"✓ Rainfall ({rainfall}mm) is sufficient")
        else:
            deficit = crop_data['rainfall_min'] - rainfall
            penalty = (deficit / crop_data['rainfall_min']) * 30
            score -= penalty
            reasons.append(f"⚠ Rainfall is {deficit}mm below requirement")
        
        # Humidity suitability
        humidity = weather['humidity']
        if humidity >= crop_data['humidity_min']:
            reasons.append(f"✓ Humidity ({humidity}%) is adequate")
        else:
            deficit = crop_data['humidity_min'] - humidity
            penalty = deficit * 0.5
            score -= penalty
            reasons.append(f"⚠ Humidity is {deficit}% below optimal")
        
        # Soil type suitability
        if soil_type and soil_type in crop_data['soil_types']:
            reasons.append(f"✓ {soil_type} soil is suitable")
        elif soil_type:
            score -= 15
            reasons.append(f"⚠ {soil_type} soil is not ideal (prefer: {', '.join(crop_data['soil_types'])})")
        
        return max(0, min(100, score)), reasons
    
    def calculate_profitability(self, crop_data: Dict, land_area_hectares: float = 1.0) -> Dict:
        """Calculate expected profitability for a crop."""
        yield_kg = crop_data['yield_per_hectare'] * land_area_hectares
        revenue = yield_kg * crop_data['price_per_kg']
        
        # Estimate costs (simplified)
        seed_cost = revenue * 0.10
        fertilizer_cost = revenue * 0.15
        labor_cost = revenue * 0.20
        irrigation_cost = revenue * 0.10
        misc_cost = revenue * 0.05
        
        total_cost = seed_cost + fertilizer_cost + labor_cost + irrigation_cost + misc_cost
        net_profit = revenue - total_cost
        profit_margin = (net_profit / revenue) * 100 if revenue > 0 else 0
        
        return {
            'yield_kg': round(yield_kg, 2),
            'revenue': round(revenue, 2),
            'total_cost': round(total_cost, 2),
            'net_profit': round(net_profit, 2),
            'profit_margin': round(profit_margin, 2),
            'roi': round((net_profit / total_cost) * 100, 2) if total_cost > 0 else 0
        }
    
    def recommend_crops(
        self, 
        location: str, 
        soil_type: str = None, 
        land_image_path: str = None,
        land_area_hectares: float = 1.0
    ) -> Dict:
        """
        Main method to recommend crops based on all factors.
        """
        # Get weather data
        weather = self.get_weather_data(location)
        
        # Analyze land image if provided
        land_analysis = None
        if land_image_path:
            land_analysis = self.analyze_land_image(land_image_path)
            if not soil_type and land_analysis:
                soil_type = land_analysis.get('estimated_soil_type')
        
        # Evaluate all crops
        recommendations = []
        for crop_name, crop_data in self.CROP_DATABASE.items():
            suitability_score, reasons = self.calculate_suitability_score(
                crop_name, crop_data, weather, soil_type
            )
            
            profitability = self.calculate_profitability(crop_data, land_area_hectares)
            
            # Combined score (70% suitability, 30% profitability)
            combined_score = (suitability_score * 0.7) + (profitability['roi'] * 0.003)
            
            recommendations.append({
                'crop_name': crop_name,
                'suitability_score': round(suitability_score, 1),
                'combined_score': round(combined_score, 1),
                'reasons': reasons,
                'season': crop_data['season'],
                'growth_period': crop_data['growth_period'],
                'profitability': profitability,
                'price_per_kg': crop_data['price_per_kg']
            })
        
        # Sort by combined score
        recommendations.sort(key=lambda x: x['combined_score'], reverse=True)
        
        return {
            'location': location,
            'weather': weather,
            'soil_type': soil_type,
            'land_analysis': land_analysis,
            'recommendations': recommendations[:5],  # Top 5
            'all_crops': recommendations
        }

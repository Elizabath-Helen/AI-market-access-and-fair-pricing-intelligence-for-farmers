"""
Views for the core app.
"""

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from decimal import Decimal
import random

from .forms import FarmerQueryForm, CropRecommendationForm, ProfitAnalysisForm
from .models import FarmerQuery, CropRecommendation, ProfitAnalysis
from .crop_advisor import CropAdvisorService
from .profit_advisor import ProfitAdvisorService


class LandingView(View):
    """Landing page for visitors."""
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        return render(request, 'core/landing.html')


class RegisterView(View):
    """User registration view."""
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        form = UserCreationForm()
        return render(request, 'core/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Farmer Market Advisor.')
            return redirect('core:dashboard')
        return render(request, 'core/register.html', {'form': form})


class LoginView(View):
    """User login view."""
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        form = AuthenticationForm()
        return render(request, 'core/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('core:dashboard')
        messages.error(request, 'Invalid username or password.')
        return render(request, 'core/login.html', {'form': form})


class LogoutView(View):
    """User logout view."""
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('core:landing')


class DashboardView(LoginRequiredMixin, View):
    """
    Main dashboard for authenticated farmers.
    """
    login_url = '/login/'
    
    def get(self, request):
        """Display the dashboard with input form."""
        form = FarmerQueryForm()
        
        # Get recent queries for this user's session
        recent_queries = FarmerQuery.objects.filter(
            session_id=request.session.session_key
        )[:5] if request.session.session_key else []
        
        context = {
            'form': form,
            'recent_queries': recent_queries
        }
        return render(request, 'core/dashboard.html', context)

    def post(self, request):
        """Handle form submission and generate recommendations."""
        form = FarmerQueryForm(request.POST)
        
        if form.is_valid():
            # Save the query
            query = form.save(commit=False)
            
            # Ensure session exists
            if not request.session.session_key:
                request.session.create()
            
            query.session_id = request.session.session_key
            query.status = 'completed'  # For now, mark as completed immediately
            query.save()
            
            # Generate mock recommendations (placeholder for AI analysis)
            recommendations = self._generate_mock_recommendations(
                query.crop_type,
                query.location,
                query.quantity
            )
            
            # Get recent queries
            recent_queries = FarmerQuery.objects.filter(
                session_id=request.session.session_key
            )[:5]
            
            context = {
                'form': FarmerQueryForm(),  # Fresh form
                'query': query,
                'recommendations': recommendations,
                'recent_queries': recent_queries,
                'show_results': True
            }
            
            messages.success(request, 'Recommendations generated successfully!')
            return render(request, 'core/dashboard.html', context)
        
        # Form is invalid
        context = {
            'form': form,
            'recent_queries': []
        }
        return render(request, 'core/dashboard.html', context)
    
    def _generate_mock_recommendations(self, crop_type, location, quantity):
        """
        Generate mock market recommendations.
        This is a placeholder until the AI analysis is implemented.
        """
        # Mock market data
        markets = [
            {'name': 'Delhi Azadpur Mandi', 'region': 'Delhi'},
            {'name': 'Mumbai APMC', 'region': 'Maharashtra'},
            {'name': 'Bangalore KR Market', 'region': 'Karnataka'},
            {'name': 'Kolkata Posta Bazar', 'region': 'West Bengal'},
            {'name': 'Chennai Koyambedu', 'region': 'Tamil Nadu'},
        ]
        
        # Base price varies by crop
        base_prices = {
            'Wheat': 25,
            'Rice': 30,
            'Tomato': 20,
            'Potato': 15,
            'Onion': 18,
            'Cotton': 50,
            'Sugarcane': 28,
            'Maize': 22,
            'Soybean': 45,
            'Groundnut': 55,
        }
        
        base_price = base_prices.get(crop_type, 25)
        
        # Generate fair price range
        fair_price_min = Decimal(base_price * 0.9)
        fair_price_max = Decimal(base_price * 1.1)
        
        # Generate market recommendations
        recommendations_list = []
        for i, market in enumerate(markets[:3]):  # Top 3 markets
            # Random variations for demo
            price_variation = random.uniform(0.85, 1.15)
            expected_price = Decimal(base_price * price_variation)
            
            # Transport cost based on distance (mock)
            distance = random.randint(50, 300)
            transport_cost_per_kg = Decimal(distance * 0.05)  # ₹0.05 per km per kg
            total_transport = transport_cost_per_kg * quantity
            
            # Calculate net profit
            revenue = expected_price * quantity
            net_profit = revenue - total_transport
            
            recommendations_list.append({
                'rank': i + 1,
                'market_name': market['name'],
                'region': market['region'],
                'expected_price': round(expected_price, 2),
                'distance_km': distance,
                'transport_cost': round(transport_cost_per_kg, 2),
                'total_transport': round(total_transport, 2),
                'revenue': round(revenue, 2),
                'net_profit': round(net_profit, 2),
                'reasoning': self._generate_reasoning(market['name'], expected_price, distance)
            })
        
        # Sort by net profit
        recommendations_list.sort(key=lambda x: x['net_profit'], reverse=True)
        
        # Update ranks
        for i, rec in enumerate(recommendations_list):
            rec['rank'] = i + 1
        
        return {
            'fair_price_min': round(fair_price_min, 2),
            'fair_price_max': round(fair_price_max, 2),
            'confidence': random.randint(75, 95),
            'markets': recommendations_list,
            'factors': [
                'Historical price trends in your region',
                'Current market demand for ' + crop_type,
                'Seasonal factors and weather conditions',
                'Transport costs and accessibility'
            ]
        }
    
    def _generate_reasoning(self, market_name, price, distance):
        """Generate reasoning for recommendation."""
        reasons = [
            f"High demand at {market_name} with competitive prices",
            f"Reasonable transport distance ({distance} km)",
            f"Current market price of ₹{price}/kg is favorable",
            "Good market infrastructure and facilities"
        ]
        return "; ".join(reasons[:2])



class CropRecommendationView(LoginRequiredMixin, View):
    """
    View for AI-powered crop recommendations based on land and climate.
    """
    login_url = '/login/'
    
    def get(self, request):
        """Display the crop recommendation form."""
        form = CropRecommendationForm()
        
        # Get recent recommendations
        recent_recommendations = CropRecommendation.objects.filter(
            session_id=request.session.session_key
        )[:5] if request.session.session_key else []
        
        context = {
            'form': form,
            'recent_recommendations': recent_recommendations
        }
        return render(request, 'core/crop_recommendation.html', context)
    
    def post(self, request):
        """Handle form submission and generate crop recommendations."""
        form = CropRecommendationForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Save the recommendation request
            recommendation = form.save(commit=False)
            
            # Ensure session exists
            if not request.session.session_key:
                request.session.create()
            
            recommendation.session_id = request.session.session_key
            
            # Get form data
            location = form.cleaned_data['location']
            soil_type = form.cleaned_data.get('soil_type')
            land_image = form.cleaned_data.get('land_image')
            
            # Save the model first to get the image path
            recommendation.save()
            
            # Use crop advisor service
            advisor = CropAdvisorService()
            
            # Get image path if uploaded
            image_path = recommendation.land_image.path if recommendation.land_image else None
            
            # Generate recommendations
            analysis_result = advisor.recommend_crops(
                location=location,
                soil_type=soil_type,
                land_image_path=image_path,
                land_area_hectares=1.0  # Default 1 hectare
            )
            
            # Update recommendation with results
            recommendation.temperature = Decimal(str(analysis_result['weather']['temp']))
            recommendation.humidity = Decimal(str(analysis_result['weather']['humidity']))
            recommendation.rainfall = Decimal(str(analysis_result['weather']['rainfall']))
            recommendation.soil_type = analysis_result['soil_type'] or soil_type
            recommendation.recommended_crops = analysis_result['recommendations']
            recommendation.analysis_data = analysis_result
            recommendation.save()
            
            # Get recent recommendations
            recent_recommendations = CropRecommendation.objects.filter(
                session_id=request.session.session_key
            )[:5]
            
            context = {
                'form': CropRecommendationForm(),  # Fresh form
                'recommendation': recommendation,
                'analysis': analysis_result,
                'recent_recommendations': recent_recommendations,
                'show_results': True
            }
            
            messages.success(request, 'Crop recommendations generated successfully!')
            return render(request, 'core/crop_recommendation.html', context)
        
        # Form is invalid
        context = {
            'form': form,
            'recent_recommendations': []
        }
        return render(request, 'core/crop_recommendation.html', context)



class ProfitAdvisorView(LoginRequiredMixin, View):
    """
    View for AI-powered profit maximization advisor.
    """
    login_url = '/login/'
    
    def get(self, request):
        """Display the profit advisor questionnaire."""
        form = ProfitAnalysisForm()
        
        # Get recent analyses
        recent_analyses = ProfitAnalysis.objects.filter(
            session_id=request.session.session_key
        )[:5] if request.session.session_key else []
        
        context = {
            'form': form,
            'recent_analyses': recent_analyses
        }
        return render(request, 'core/profit_advisor.html', context)
    
    def post(self, request):
        """Handle form submission and generate profit strategies."""
        form = ProfitAnalysisForm(request.POST)
        
        if form.is_valid():
            # Save the analysis request
            analysis = form.save(commit=False)
            
            # Ensure session exists
            if not request.session.session_key:
                request.session.create()
            
            analysis.session_id = request.session.session_key
            
            # Prepare responses for advisor
            responses = {
                'crop_type': form.cleaned_data['crop_type'],
                'land_area': float(form.cleaned_data['land_area']),
                'total_yield': float(form.cleaned_data['total_yield']),
                'seed_cost': float(form.cleaned_data['seed_cost']),
                'fertilizer_cost': float(form.cleaned_data['fertilizer_cost']),
                'labor_cost': float(form.cleaned_data['labor_cost']),
                'irrigation_cost': float(form.cleaned_data['irrigation_cost']),
                'other_costs': float(form.cleaned_data.get('other_costs', 0)),
                'current_price': float(form.cleaned_data['current_price']),
                'storage_capacity': form.cleaned_data['storage_capacity'],
                'immediate_need': form.cleaned_data['immediate_need'],
                'processing_interest': form.cleaned_data['processing_interest'],
            }
            
            # Use profit advisor service
            advisor = ProfitAdvisorService()
            result = advisor.analyze_responses(responses)
            
            # Update analysis with results
            analysis.current_situation = result['current_situation']
            analysis.strategies = result['strategies']
            analysis.summary = result['summary']
            analysis.save()
            
            # Get recent analyses
            recent_analyses = ProfitAnalysis.objects.filter(
                session_id=request.session.session_key
            )[:5]
            
            context = {
                'form': ProfitAnalysisForm(),  # Fresh form
                'analysis': analysis,
                'result': result,
                'recent_analyses': recent_analyses,
                'show_results': True
            }
            
            messages.success(request, 'Profit analysis completed successfully!')
            return render(request, 'core/profit_advisor.html', context)
        
        # Form is invalid
        context = {
            'form': form,
            'recent_analyses': []
        }
        return render(request, 'core/profit_advisor.html', context)

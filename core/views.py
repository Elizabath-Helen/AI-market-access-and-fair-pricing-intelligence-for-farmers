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

from .forms import FarmerQueryForm, CropRecommendationForm, ProfitAnalysisForm, NegotiationAnalysisForm
from .models import FarmerQuery, CropRecommendation, ProfitAnalysis, NegotiationAnalysis
from .crop_advisor import CropAdvisorService
from .negotiation_coach import NegotiationCoachService
# Temporarily disabled: from .profit_advisor import ProfitAdvisorService


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
            
            # Temporarily using mock data until import issue is resolved
            total_costs = sum([
                float(form.cleaned_data['seed_cost']),
                float(form.cleaned_data['fertilizer_cost']),
                float(form.cleaned_data['labor_cost']),
                float(form.cleaned_data['irrigation_cost']),
                float(form.cleaned_data.get('other_costs', 0))
            ])
            
            total_yield = float(form.cleaned_data['total_yield'])
            current_price = float(form.cleaned_data['current_price'])
            current_revenue = total_yield * current_price
            current_profit = current_revenue - total_costs
            
            # Generate mock strategies
            strategies = [
                {
                    'name': 'Optimal Market Timing',
                    'priority': 'High',
                    'description': 'Strategic timing can increase your revenue by 10-15%',
                    'recommendation': 'Wait for peak season or sell now based on storage',
                    'reason': 'Market prices vary significantly by season',
                    'potential_benefit': round(current_revenue * 0.10, 2),
                    'action_items': [
                        'Monitor daily market prices',
                        'Ensure proper storage if waiting',
                        'Consider forward contracts for price security'
                    ]
                },
                {
                    'name': 'Multi-Channel Selling Strategy',
                    'priority': 'High',
                    'description': 'Diversify selling channels to maximize revenue',
                    'recommendation': 'Split: 40% Direct, 40% Distributors, 20% Traders',
                    'reason': 'Different channels offer different prices',
                    'potential_benefit': round(current_revenue * 0.12, 2),
                    'breakdown': {
                        'direct_sales': {
                            'percentage': 40,
                            'quantity': round(total_yield * 0.40, 2),
                            'price': round(current_price * 1.25, 2),
                            'revenue': round(total_yield * 0.40 * current_price * 1.25, 2),
                            'advantages': ['Highest price', 'Build relationships', 'No middleman']
                        },
                        'distributors': {
                            'percentage': 40,
                            'quantity': round(total_yield * 0.40, 2),
                            'price': round(current_price * 1.10, 2),
                            'revenue': round(total_yield * 0.40 * current_price * 1.10, 2),
                            'advantages': ['Good price', 'Reliable payment', 'Regular orders']
                        },
                        'traders': {
                            'percentage': 20,
                            'quantity': round(total_yield * 0.20, 2),
                            'price': round(current_price * 0.95, 2),
                            'revenue': round(total_yield * 0.20 * current_price * 0.95, 2),
                            'advantages': ['Quick sale', 'Bulk disposal', 'Immediate payment']
                        }
                    },
                    'action_items': [
                        'Set up direct sales at local markets',
                        'Build relationships with distributors',
                        'Keep trader contacts for bulk sales'
                    ]
                }
            ]
            
            # Add value-added processing if interested
            if form.cleaned_data['processing_interest'] != 'No, prefer raw sale':
                strategies.append({
                    'name': 'Value-Added Processing',
                    'priority': 'Medium',
                    'description': f"Convert {form.cleaned_data['crop_type']} into processed products",
                    'recommendation': 'Process 30% of yield into value-added products',
                    'reason': 'Can increase value by 40-150%',
                    'potential_benefit': round(current_revenue * 0.20, 2),
                    'details': {
                        'product': 'Processed Product',
                        'value_increase': 50,
                        'investment_level': 'medium',
                        'target_market': 'Retail & Wholesale',
                        'quantity_to_process': round(total_yield * 0.30, 2),
                        'processing_cost': round(current_revenue * 0.20 * 0.30, 2),
                        'additional_revenue': round(current_revenue * 0.20, 2),
                        'net_benefit': round(current_revenue * 0.20 * 0.70, 2)
                    },
                    'action_items': [
                        'Research processing equipment',
                        'Check licensing requirements',
                        'Identify potential buyers',
                        'Start with small batch'
                    ]
                })
            
            # Cost optimization strategy
            strategies.append({
                'name': 'Cost Optimization',
                'priority': 'High',
                'description': 'Reduce production costs without compromising quality',
                'recommendation': f"Potential to save ₹{round(total_costs * 0.15, 2)} (15% of costs)",
                'reason': 'Lower costs directly increase profit margins',
                'potential_benefit': round(total_costs * 0.15, 2),
                'opportunities': [
                    {
                        'area': 'Seeds',
                        'current_cost': round(float(form.cleaned_data['seed_cost']), 2),
                        'potential_saving': round(float(form.cleaned_data['seed_cost']) * 0.15, 2),
                        'methods': ['Buy in bulk', 'Seed treatment at home', 'Join cooperatives']
                    },
                    {
                        'area': 'Fertilizers',
                        'current_cost': round(float(form.cleaned_data['fertilizer_cost']), 2),
                        'potential_saving': round(float(form.cleaned_data['fertilizer_cost']) * 0.20, 2),
                        'methods': ['Soil testing', 'Organic composting', 'Government subsidies']
                    }
                ],
                'action_items': [
                    'Get soil tested',
                    'Explore government subsidies',
                    'Consider drip irrigation'
                ]
            })
            
            total_potential_benefit = sum(s.get('potential_benefit', 0) for s in strategies)
            
            result = {
                'current_situation': {
                    'total_costs': round(total_costs, 2),
                    'total_yield': round(total_yield, 2),
                    'current_price': round(current_price, 2),
                    'current_revenue': round(current_revenue, 2),
                    'current_profit': round(current_profit, 2),
                    'current_roi': round((current_profit / total_costs * 100) if total_costs > 0 else 0, 2),
                    'cost_per_kg': round(total_costs / total_yield if total_yield > 0 else 0, 2),
                    'yield_per_acre': round(total_yield / float(form.cleaned_data['land_area']) if float(form.cleaned_data['land_area']) > 0 else 0, 2),
                },
                'strategies': strategies,
                'summary': {
                    'current_profit': round(current_profit, 2),
                    'potential_additional_profit': round(total_potential_benefit, 2),
                    'projected_profit': round(current_profit + total_potential_benefit, 2),
                    'improvement_percentage': round((total_potential_benefit / current_profit * 100) if current_profit > 0 else 0, 2),
                    'top_recommendations': [
                        s['name'] for s in sorted(strategies, key=lambda x: x.get('potential_benefit', 0), reverse=True)[:3]
                    ],
                    'implementation_priority': [
                        s['name'] for s in sorted(strategies, key=lambda x: (x.get('priority') == 'High', x.get('potential_benefit', 0)), reverse=True)
                    ]
                }
            }
            
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


class NegotiationCoachView(LoginRequiredMixin, View):
    """
    View for AI-powered negotiation coaching.
    """
    login_url = '/login/'
    
    def get(self, request):
        """Display the negotiation coach form."""
        form = NegotiationAnalysisForm()
        
        # Get recent analyses
        recent_analyses = NegotiationAnalysis.objects.filter(
            session_id=request.session.session_key
        )[:5] if request.session.session_key else []
        
        context = {
            'form': form,
            'recent_analyses': recent_analyses
        }
        return render(request, 'core/negotiation_coach.html', context)
    
    def post(self, request):
        """Handle form submission and generate negotiation analysis."""
        form = NegotiationAnalysisForm(request.POST)
        
        if form.is_valid():
            # Save the analysis request
            analysis = form.save(commit=False)
            
            # Ensure session exists
            if not request.session.session_key:
                request.session.create()
            
            analysis.session_id = request.session.session_key
            
            # Get nearby market prices from the form
            nearby_prices = form.cleaned_data.get('nearby_market_prices_text', [])
            analysis.nearby_market_prices = nearby_prices
            
            # Use negotiation coach service
            coach = NegotiationCoachService()
            result = coach.analyze_offer(
                crop_type=form.cleaned_data['crop_type'],
                farmer_location=form.cleaned_data['farmer_location'],
                quantity=float(form.cleaned_data['quantity']),
                offered_price=float(form.cleaned_data['offered_price']),
                nearby_market_prices=nearby_prices
            )
            
            # Update analysis with results
            analysis.offer_analysis = result['offer_analysis']
            analysis.fair_price_range = result['fair_price_range']
            analysis.negotiation_advice = result['negotiation_advice']
            analysis.market_context = result['market_context']
            analysis.save()
            
            # Get recent analyses
            recent_analyses = NegotiationAnalysis.objects.filter(
                session_id=request.session.session_key
            )[:5]
            
            context = {
                'form': NegotiationAnalysisForm(),  # Fresh form
                'analysis': analysis,
                'result': result,
                'recent_analyses': recent_analyses,
                'show_results': True
            }
            
            messages.success(request, 'Negotiation analysis completed successfully!')
            return render(request, 'core/negotiation_coach.html', context)
        
        # Form is invalid
        context = {
            'form': form,
            'recent_analyses': []
        }
        return render(request, 'core/negotiation_coach.html', context)
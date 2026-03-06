"""
URL configuration for core app.
"""

from django.urls import path
from .views import (
    LandingView, RegisterView, LoginView, 
    LogoutView, DashboardView, CropRecommendationView, ProfitAdvisorView, NegotiationCoachView
)
from . import api_views

app_name = 'core'

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('crop-recommendation/', CropRecommendationView.as_view(), name='crop_recommendation'),
    path('profit-advisor/', ProfitAdvisorView.as_view(), name='profit_advisor'),
    path('negotiation-coach/', NegotiationCoachView.as_view(), name='negotiation_coach'),
    
    # API endpoints
    path('api/negotiation-advice/', api_views.negotiation_advice_api, name='api_negotiation_advice'),
    path('api/docs/', api_views.api_documentation, name='api_docs'),
]

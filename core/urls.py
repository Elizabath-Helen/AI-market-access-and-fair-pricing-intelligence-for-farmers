"""
URL configuration for core app.
"""

from django.urls import path
from .views import (
    LandingView, RegisterView, LoginView, 
    LogoutView, DashboardView, CropRecommendationView, ProfitAdvisorView
)

app_name = 'core'

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('crop-recommendation/', CropRecommendationView.as_view(), name='crop_recommendation'),
    path('profit-advisor/', ProfitAdvisorView.as_view(), name='profit_advisor'),
]

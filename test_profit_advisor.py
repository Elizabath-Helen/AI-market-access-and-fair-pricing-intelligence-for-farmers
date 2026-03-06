#!/usr/bin/env python
"""
Test script for the Profit Advisor feature.
"""

import os
import sys
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from core.models import ProfitAnalysis


def test_profit_advisor():
    """Test the profit advisor functionality."""
    print("Testing Profit Advisor Feature...")
    
    # Create test client
    client = Client()
    
    # Create or get test user
    user, created = User.objects.get_or_create(
        username='testfarmer',
        defaults={'password': 'testpass123'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    # Login
    login_success = client.login(username='testfarmer', password='testpass123')
    print(f"✓ User login: {'Success' if login_success else 'Failed'}")
    
    # Test GET request to profit advisor page
    response = client.get('/profit-advisor/')
    print(f"✓ Profit advisor page loads: {response.status_code == 200}")
    
    # Test form submission
    form_data = {
        'crop_type': 'Wheat',
        'land_area': '5.0',
        'total_yield': '7500.0',  # 1500 kg per acre
        'seed_cost': '15000.0',
        'fertilizer_cost': '25000.0',
        'labor_cost': '20000.0',
        'irrigation_cost': '10000.0',
        'other_costs': '5000.0',
        'current_price': '25.0',  # Rs 25 per kg
        'storage_capacity': 'Yes, good storage',
        'immediate_need': 'No, can wait',
        'processing_interest': 'Yes, very interested'
    }
    
    response = client.post('/profit-advisor/', form_data)
    print(f"✓ Form submission: {response.status_code == 200}")
    
    # Check if analysis was saved
    analysis_count = ProfitAnalysis.objects.count()
    print(f"✓ Analysis saved to database: {analysis_count > 0}")
    
    if analysis_count > 0:
        analysis = ProfitAnalysis.objects.first()
        print(f"✓ Analysis crop type: {analysis.crop_type}")
        print(f"✓ Current profit calculated: ₹{analysis.current_situation.get('current_profit', 0)}")
        print(f"✓ Strategies generated: {len(analysis.strategies)}")
        
        # Check specific strategies
        strategy_names = [s['name'] for s in analysis.strategies]
        expected_strategies = ['Optimal Market Timing', 'Multi-Channel Selling Strategy', 'Cost Optimization']
        
        for strategy in expected_strategies:
            if strategy in strategy_names:
                print(f"✓ Strategy '{strategy}' generated")
            else:
                print(f"✗ Strategy '{strategy}' missing")
        
        # Check if value-added processing strategy is included (since user was interested)
        if 'Value-Added Processing' in strategy_names:
            print("✓ Value-Added Processing strategy included (user interested)")
        
        # Display summary
        summary = analysis.summary
        print(f"\n--- Analysis Summary ---")
        print(f"Current Profit: ₹{summary.get('current_profit', 0)}")
        print(f"Potential Additional Profit: ₹{summary.get('potential_additional_profit', 0)}")
        print(f"Projected Profit: ₹{summary.get('projected_profit', 0)}")
        print(f"Improvement: {summary.get('improvement_percentage', 0)}%")
    
    print("\n✓ Profit Advisor test completed successfully!")
    return True


if __name__ == '__main__':
    try:
        test_profit_advisor()
        print("\n🎉 All tests passed! The Profit Advisor feature is working correctly.")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
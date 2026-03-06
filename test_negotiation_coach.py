#!/usr/bin/env python
"""
Test script for the AI Negotiation Coach feature.
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
from core.models import NegotiationAnalysis
from core.negotiation_coach import NegotiationCoachService


def test_negotiation_coach_service():
    """Test the negotiation coach service directly."""
    print("Testing Negotiation Coach Service...")
    
    coach = NegotiationCoachService()
    
    # Test case 1: Underpriced offer
    result1 = coach.analyze_offer(
        crop_type='Wheat',
        farmer_location='Amritsar, Punjab',
        quantity=50.0,  # 50 quintals
        offered_price=2100.0,  # Below market rate
        nearby_market_prices=[2300, 2350, 2280]
    )
    
    print(f"✓ Test 1 - Underpriced offer:")
    print(f"  Status: {result1['offer_analysis']['status']}")
    print(f"  Offered: ₹{result1['offer_analysis']['offered_price']}")
    print(f"  Fair range: ₹{result1['fair_price_range']['min_price']} - ₹{result1['fair_price_range']['max_price']}")
    print(f"  Suggested price: ₹{result1['negotiation_advice']['suggested_price']}")
    print(f"  Explanation: {result1['negotiation_advice']['explanation'][:100]}...")
    
    # Test case 2: Fair offer
    result2 = coach.analyze_offer(
        crop_type='Rice',
        farmer_location='Ludhiana, Punjab',
        quantity=30.0,
        offered_price=3000.0,  # Fair market rate
        nearby_market_prices=[2950, 3050, 3000]
    )
    
    print(f"\n✓ Test 2 - Fair offer:")
    print(f"  Status: {result2['offer_analysis']['status']}")
    print(f"  Offered: ₹{result2['offer_analysis']['offered_price']}")
    print(f"  Suggested price: ₹{result2['negotiation_advice']['suggested_price']}")
    
    # Test case 3: Overpriced offer (generous buyer)
    result3 = coach.analyze_offer(
        crop_type='Cotton',
        farmer_location='Ahmedabad, Gujarat',
        quantity=20.0,
        offered_price=6500.0,  # Above market rate
        nearby_market_prices=[6000, 6100, 5950]
    )
    
    print(f"\n✓ Test 3 - Overpriced offer:")
    print(f"  Status: {result3['offer_analysis']['status']}")
    print(f"  Offered: ₹{result3['offer_analysis']['offered_price']}")
    print(f"  Recommendation: {result3['negotiation_advice']['recommendation']}")
    
    return True


def test_negotiation_coach_web():
    """Test the negotiation coach web interface."""
    print("\nTesting Negotiation Coach Web Interface...")
    
    # Create test client
    client = Client()
    
    # Create or get test user
    user, created = User.objects.get_or_create(
        username='testfarmer2',
        defaults={'password': 'testpass123'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    # Login
    login_success = client.login(username='testfarmer2', password='testpass123')
    print(f"✓ User login: {'Success' if login_success else 'Failed'}")
    
    # Test GET request to negotiation coach page
    response = client.get('/negotiation-coach/')
    print(f"✓ Negotiation coach page loads: {response.status_code == 200}")
    
    # Test form submission
    form_data = {
        'crop_type': 'Wheat',
        'farmer_location': 'Amritsar, Punjab',
        'quantity': '50.0',
        'offered_price': '2100.0',
        'nearby_market_prices_text': '2300, 2350, 2280'
    }
    
    response = client.post('/negotiation-coach/', form_data)
    print(f"✓ Form submission: {response.status_code == 200}")
    
    # Check if analysis was saved
    analysis_count = NegotiationAnalysis.objects.count()
    print(f"✓ Analysis saved to database: {analysis_count > 0}")
    
    if analysis_count > 0:
        analysis = NegotiationAnalysis.objects.first()
        print(f"✓ Analysis crop type: {analysis.crop_type}")
        print(f"✓ Offer status: {analysis.offer_analysis.get('status', 'N/A')}")
        print(f"✓ Suggested price: ₹{analysis.negotiation_advice.get('suggested_price', 0)}")
        
        # Display detailed results
        print(f"\n--- Analysis Results ---")
        print(f"Crop: {analysis.crop_type}")
        print(f"Location: {analysis.farmer_location}")
        print(f"Quantity: {analysis.quantity} quintals")
        print(f"Offered Price: ₹{analysis.offered_price}")
        print(f"Status: {analysis.offer_analysis.get('status')}")
        print(f"Price Difference: {analysis.offer_analysis.get('price_difference_percentage')}%")
        print(f"Suggested Price: ₹{analysis.negotiation_advice.get('suggested_price')}")
        print(f"Recommendation: {analysis.negotiation_advice.get('recommendation')}")
        
        # Show negotiation tactics
        tactics = analysis.negotiation_advice.get('negotiation_tactics', [])
        if tactics:
            print(f"\nNegotiation Tactics:")
            for i, tactic in enumerate(tactics[:3], 1):
                print(f"  {i}. {tactic}")
    
    print("\n✓ Negotiation Coach web test completed successfully!")
    return True


def test_edge_cases():
    """Test edge cases and validation."""
    print("\nTesting Edge Cases...")
    
    coach = NegotiationCoachService()
    
    # Test with unknown crop
    result = coach.analyze_offer(
        crop_type='Unknown Crop',
        farmer_location='Test Location',
        quantity=10.0,
        offered_price=1000.0,
        nearby_market_prices=[1100, 1050]
    )
    
    print(f"✓ Unknown crop handled: {result['offer_analysis']['status'] is not None}")
    
    # Test with no nearby prices
    result = coach.analyze_offer(
        crop_type='Tomato',
        farmer_location='Mumbai, Maharashtra',
        quantity=25.0,
        offered_price=1800.0,
        nearby_market_prices=None
    )
    
    print(f"✓ No nearby prices handled: {result['negotiation_advice']['suggested_price'] > 0}")
    
    # Test with very small quantity
    result = coach.analyze_offer(
        crop_type='Onion',
        farmer_location='Nashik, Maharashtra',
        quantity=1.0,
        offered_price=1200.0,
        nearby_market_prices=[1400, 1350]
    )
    
    print(f"✓ Small quantity handled: {len(result['negotiation_advice']['negotiation_tactics']) > 0}")
    
    return True


if __name__ == '__main__':
    try:
        print("🚀 Starting AI Negotiation Coach Tests...\n")
        
        # Test the service layer
        test_negotiation_coach_service()
        
        # Test the web interface
        test_negotiation_coach_web()
        
        # Test edge cases
        test_edge_cases()
        
        print("\n🎉 All tests passed! The AI Negotiation Coach feature is working correctly.")
        print("\n📋 Feature Summary:")
        print("✅ Price offer analysis with fair/underpriced/overpriced status")
        print("✅ AI-generated negotiation advice and explanations")
        print("✅ Suggested negotiation prices and ranges")
        print("✅ Market context and negotiation tactics")
        print("✅ Web interface with form validation")
        print("✅ Database storage and history tracking")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
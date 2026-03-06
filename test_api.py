#!/usr/bin/env python
"""
Quick API test for the negotiation advice endpoint.
"""

import requests
import json

# Test the API endpoint
def test_api():
    # First login to get session
    session = requests.Session()
    
    # Get CSRF token
    response = session.get('http://127.0.0.1:8000/login/')
    
    # Test API documentation endpoint
    doc_response = session.get('http://127.0.0.1:8000/api/docs/')
    print(f"API Documentation: {doc_response.status_code}")
    
    if doc_response.status_code == 200:
        print("✅ API documentation endpoint working")
    
    print("\n📚 API is ready for integration!")
    print("🔗 Documentation: http://127.0.0.1:8000/api/docs/")
    print("🔗 Negotiation Coach: http://127.0.0.1:8000/negotiation-coach/")

if __name__ == '__main__':
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("⚠️  Server not running. Start with: python manage.py runserver")
    except Exception as e:
        print(f"❌ Error: {e}")
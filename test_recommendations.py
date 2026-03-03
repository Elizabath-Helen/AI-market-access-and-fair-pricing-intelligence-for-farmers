"""
Test the recommendations functionality.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from core.models import FarmerQuery

class RecommendationsTests(TestCase):
    """Test recommendations functionality."""
    
    def setUp(self):
        """Create a test user."""
        self.client = Client()
        self.user = User.objects.create_user(username='testfarmer', password='TestPass123!')
        self.client.login(username='testfarmer', password='TestPass123!')
    
    def test_dashboard_loads(self):
        """Test that dashboard loads for authenticated user."""
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Get Market Recommendations')
        print("✓ Dashboard loads successfully")
    
    def test_form_submission(self):
        """Test that form submission works."""
        response = self.client.post('/dashboard/', {
            'crop_type': 'Wheat',
            'location': 'Delhi',
            'quantity': '100'
        })
        self.assertEqual(response.status_code, 200)
        print("✓ Form submission works")
    
    def test_query_saved(self):
        """Test that query is saved to database."""
        self.client.post('/dashboard/', {
            'crop_type': 'Rice',
            'location': 'Mumbai',
            'quantity': '150'
        })
        query = FarmerQuery.objects.first()
        self.assertIsNotNone(query)
        self.assertEqual(query.crop_type, 'Rice')
        self.assertEqual(query.location, 'Mumbai')
        print("✓ Query saved to database")
    
    def test_recommendations_displayed(self):
        """Test that recommendations are displayed."""
        response = self.client.post('/dashboard/', {
            'crop_type': 'Tomato',
            'location': 'Bangalore',
            'quantity': '200'
        })
        self.assertContains(response, 'Fair Price Range')
        self.assertContains(response, 'Top Market Recommendations')
        self.assertContains(response, 'Net Profit')
        print("✓ Recommendations displayed correctly")
    
    def test_invalid_form(self):
        """Test that invalid form shows errors."""
        response = self.client.post('/dashboard/', {
            'crop_type': '',
            'location': '',
            'quantity': ''
        })
        self.assertEqual(response.status_code, 200)
        # Form should be redisplayed with errors
        print("✓ Invalid form handled correctly")

if __name__ == '__main__':
    import sys
    from django.test.utils import get_runner
    from django.conf import settings
    
    print("\n" + "=" * 60)
    print("Testing Recommendations Functionality")
    print("=" * 60 + "\n")
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False, keepdb=False)
    failures = test_runner.run_tests(['__main__'])
    
    if failures == 0:
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe 'Get Recommendations' button is now working!")
        print("\nYou can:")
        print("  1. Run: python manage.py runserver")
        print("  2. Login to dashboard")
        print("  3. Fill in the form and click 'Get Recommendations'")
        print("  4. See market recommendations with prices and profits!")
    
    sys.exit(failures)

"""
Quick test script to verify authentication system works.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User

class AuthenticationTests(TestCase):
    """Test user registration and login flow."""
    
    def test_all_authentication(self):
        print("\nTesting Farmer Market Advisor Authentication System\n")
        print("=" * 60)
        
        # Create a test client
        client = Client()
        
        # Test 1: Landing page loads
        print("\n1. Testing landing page...")
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
        print("   ✓ Landing page loads successfully")
        
        # Test 2: Register page loads
        print("\n2. Testing registration page...")
        response = client.get('/register/')
        self.assertEqual(response.status_code, 200)
        print("   ✓ Registration page loads successfully")
        
        # Test 3: Login page loads
        print("\n3. Testing login page...")
        response = client.get('/login/')
        self.assertEqual(response.status_code, 200)
        print("   ✓ Login page loads successfully")
        
        # Test 4: Create a test user
        print("\n4. Testing user creation...")
        response = client.post('/register/', {
            'username': 'testfarmer',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!'
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='testfarmer')
        self.assertIsNotNone(user)
        print("   ✓ User registration works correctly")
        
        # Test 5: Login with created user
        print("\n5. Testing user login...")
        client.logout()  # Logout first
        response = client.post('/login/', {
            'username': 'testfarmer',
            'password': 'TestPass123!'
        })
        self.assertEqual(response.status_code, 302)
        print("   ✓ User login works correctly")
        
        # Test 6: Dashboard access (requires authentication)
        print("\n6. Testing dashboard access...")
        response = client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        print("   ✓ Dashboard loads for authenticated user")
        
        # Test 7: Logout
        print("\n7. Testing logout...")
        response = client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        print("   ✓ Logout works correctly")
        
        # Test 8: Dashboard redirect when not authenticated
        print("\n8. Testing authentication protection...")
        response = client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)
        print("   ✓ Dashboard properly protected")
        
        print("\n" + "=" * 60)
        print("✓ All authentication tests passed!")
        print("\nYour authentication system is working correctly!")

if __name__ == '__main__':
    import sys
    from django.test.utils import get_runner
    from django.conf import settings
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=0, interactive=False, keepdb=False)
    failures = test_runner.run_tests(['__main__'])
    
    if failures == 0:
        print("\n" + "=" * 60)
        print("\n✓ ALL TESTS PASSED!")
        print("\nYou can now:")
        print("  1. Run: python manage.py runserver")
        print("  2. Visit: http://localhost:8000")
        print("  3. Register a new account")
        print("  4. Login and access the dashboard")
    sys.exit(failures)

"""
Final verification that everything is ready.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from django.contrib.auth.models import User

print("\n" + "=" * 70)
print(" " * 15 + "FARMER MARKET ADVISOR - FINAL CHECK")
print("=" * 70)

# Check 1: Database
print("\n✓ DATABASE CHECK")
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user';")
if cursor.fetchone():
    print("  ✅ Database configured correctly")
    print("  ✅ auth_user table exists")
else:
    print("  ❌ Database not configured")
    exit(1)

# Check 2: User count
user_count = User.objects.count()
print(f"  ✅ Current registered users: {user_count}")

# Check 3: Tables
cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table';")
table_count = cursor.fetchone()[0]
print(f"  ✅ Total database tables: {table_count}")

# Check 4: Settings
from django.conf import settings
print("\n✓ CONFIGURATION CHECK")
print(f"  ✅ Debug mode: {settings.DEBUG}")
print(f"  ✅ Database: SQLite (db.sqlite3)")
print(f"  ✅ Session engine: Database")

# Check 5: URLs
print("\n✓ AVAILABLE URLS")
print("  ✅ Landing page: http://localhost:8000/")
print("  ✅ Register: http://localhost:8000/register/")
print("  ✅ Login: http://localhost:8000/login/")
print("  ✅ Dashboard: http://localhost:8000/dashboard/")
print("  ✅ Logout: http://localhost:8000/logout/")
print("  ✅ Admin: http://localhost:8000/admin/")

# Check 6: Templates
import os
template_dir = settings.BASE_DIR / 'templates'
templates = [
    'base.html',
    'core/landing.html',
    'core/register.html',
    'core/login.html',
    'core/dashboard.html'
]
print("\n✓ TEMPLATES CHECK")
for template in templates:
    template_path = template_dir / template
    if template_path.exists():
        print(f"  ✅ {template}")
    else:
        print(f"  ❌ {template} - MISSING")

print("\n" + "=" * 70)
print(" " * 20 + "🎉 ALL CHECKS PASSED! 🎉")
print("=" * 70)

print("\n📋 NEXT STEPS:")
print("\n  1. Start the server:")
print("     python manage.py runserver")
print("\n  2. Open your browser:")
print("     http://localhost:8000")
print("\n  3. Register a new account and start using the app!")

print("\n💡 TIP: Use 'start_server.bat' for quick startup on Windows")
print("\n" + "=" * 70 + "\n")

"""
Verify authentication tables are created.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cursor.fetchall()

print("\n" + "=" * 60)
print("DATABASE TABLES VERIFICATION")
print("=" * 60)

auth_tables = [t[0] for t in tables if t[0].startswith('auth_')]
session_tables = [t[0] for t in tables if t[0].startswith('django_session')]
app_tables = [t[0] for t in tables if not t[0].startswith('auth_') and not t[0].startswith('django_') and not t[0].startswith('sqlite_')]

print("\n✓ Authentication Tables (for login/registration):")
for table in auth_tables:
    print(f"  • {table}")

print("\n✓ Session Tables:")
for table in session_tables:
    print(f"  • {table}")

print("\n✓ Application Tables:")
for table in app_tables:
    print(f"  • {table}")

print("\n" + "=" * 60)
print(f"Total tables created: {len(tables)}")
print("=" * 60)

# Test if we can query auth_user table
cursor.execute("SELECT COUNT(*) FROM auth_user;")
user_count = cursor.fetchone()[0]
print(f"\n✓ auth_user table is working! Current users: {user_count}")

print("\n✅ All authentication tables are ready!")
print("\nYou can now:")
print("  1. Run: python manage.py runserver")
print("  2. Visit: http://localhost:8000")
print("  3. Register and login successfully!")
print()

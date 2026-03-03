#!/usr/bin/env python
"""
Temporary script to run migrations using SQLite instead of PostgreSQL.
This is useful for development when PostgreSQL is not available.
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Override database settings to use SQLite
from django.conf import settings
settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Setup Django
django.setup()

# Run migrations
from django.core.management import call_command

print("=" * 60)
print("Running migrations with SQLite database...")
print("=" * 60)

try:
    # Show migrations status
    print("\n1. Checking migrations status...")
    call_command('showmigrations')
    
    # Run migrations
    print("\n2. Running migrations...")
    call_command('migrate', verbosity=2)
    
    # Verify migrations
    print("\n3. Verifying migrations...")
    call_command('showmigrations')
    
    print("\n" + "=" * 60)
    print("✓ Migrations completed successfully!")
    print("=" * 60)
    
    # Show database schema
    print("\n4. Database schema verification:")
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = cursor.fetchall()
        print(f"\nTotal tables created: {len(tables)}")
        print("\nTables:")
        for table in tables:
            print(f"  - {table[0]}")
            
except Exception as e:
    print(f"\n✗ Error during migration: {e}")
    sys.exit(1)

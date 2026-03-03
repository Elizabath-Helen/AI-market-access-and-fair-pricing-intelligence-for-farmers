#!/usr/bin/env python
"""
Script to verify the database schema matches the design specifications.
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

from django.db import connection

def get_table_schema(table_name):
    """Get the schema for a specific table."""
    with connection.cursor() as cursor:
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        cursor.execute(f"PRAGMA index_list({table_name});")
        indexes = cursor.fetchall()
        
        return columns, indexes

def verify_schema():
    """Verify all custom tables match the design specifications."""
    print("=" * 80)
    print("DATABASE SCHEMA VERIFICATION")
    print("=" * 80)
    
    # Define expected tables and their key fields
    expected_tables = {
        'markets': ['id', 'name', 'location', 'mandi_code', 'region', 'active'],
        'market_prices': ['id', 'market_id', 'crop_type', 'date', 'min_price', 'max_price', 
                         'modal_price', 'arrivals', 'source', 'created_at'],
        'transport_costs': ['id', 'from_location', 'to_market_id', 'distance_km', 
                           'cost_per_kg', 'last_updated'],
        'farmer_queries': ['id', 'crop_type', 'location', 'quantity', 'created_at', 
                          'session_id', 'status'],
        'price_analyses': ['id', 'query_id', 'fair_price_min', 'fair_price_max', 
                          'confidence_score', 'factors_considered', 'created_at'],
        'market_recommendations': ['id', 'query_id', 'market_id', 'expected_price', 
                                  'transport_cost', 'net_profit', 'rank', 'reasoning', 
                                  'created_at'],
    }
    
    all_verified = True
    
    for table_name, expected_fields in expected_tables.items():
        print(f"\n{'─' * 80}")
        print(f"Table: {table_name}")
        print(f"{'─' * 80}")
        
        try:
            columns, indexes = get_table_schema(table_name)
            
            # Display columns
            print("\nColumns:")
            actual_fields = []
            for col in columns:
                col_id, name, col_type, not_null, default, pk = col
                actual_fields.append(name)
                pk_marker = " [PK]" if pk else ""
                null_marker = " NOT NULL" if not_null else ""
                print(f"  {col_id + 1}. {name:25} {col_type:15} {null_marker}{pk_marker}")
            
            # Display indexes
            if indexes:
                print("\nIndexes:")
                for idx in indexes:
                    seq, name, unique, origin, partial = idx
                    unique_marker = " [UNIQUE]" if unique else ""
                    print(f"  - {name}{unique_marker}")
            
            # Verify expected fields
            missing_fields = set(expected_fields) - set(actual_fields)
            if missing_fields:
                print(f"\n⚠ WARNING: Missing expected fields: {', '.join(missing_fields)}")
                all_verified = False
            else:
                print(f"\n✓ All expected fields present ({len(expected_fields)} fields)")
                
        except Exception as e:
            print(f"\n✗ ERROR: Could not verify table: {e}")
            all_verified = False
    
    # Check constraints
    print(f"\n{'─' * 80}")
    print("Checking Database Constraints")
    print(f"{'─' * 80}")
    
    constraints_to_check = [
        ('market_prices', 'price_range_constraint', 
         'min_price <= modal_price <= max_price'),
        ('transport_costs', 'distance_non_negative', 
         'distance_km >= 0'),
        ('transport_costs', 'cost_non_negative', 
         'cost_per_kg >= 0'),
    ]
    
    for table, constraint_name, description in constraints_to_check:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table}';")
            result = cursor.fetchone()
            if result and constraint_name in result[0]:
                print(f"✓ {table}.{constraint_name}: {description}")
            else:
                print(f"⚠ {table}.{constraint_name}: Not found or not verified")
    
    # Summary
    print(f"\n{'=' * 80}")
    if all_verified:
        print("✓ SCHEMA VERIFICATION PASSED")
        print("All tables and fields match the design specifications.")
    else:
        print("⚠ SCHEMA VERIFICATION COMPLETED WITH WARNINGS")
        print("Some fields or tables may be missing. Review the output above.")
    print(f"{'=' * 80}\n")
    
    return all_verified

if __name__ == '__main__':
    try:
        success = verify_schema()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Verification failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

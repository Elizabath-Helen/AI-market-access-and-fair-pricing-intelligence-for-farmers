# Setup Verification Guide

This document helps verify that the Django project structure is correctly set up.

## Project Structure Checklist

### ✓ Core Configuration Files
- [x] `manage.py` - Django management script
- [x] `requirements.txt` - Python dependencies
- [x] `.env.example` - Environment variables template
- [x] `.gitignore` - Git ignore rules
- [x] `pytest.ini` - Pytest configuration
- [x] `README.md` - Project documentation
- [x] `setup.sh` - Setup automation script

### ✓ Django Project (config/)
- [x] `config/__init__.py` - Package initialization with Celery import
- [x] `config/settings.py` - Django settings with PostgreSQL, Redis, Celery
- [x] `config/urls.py` - URL routing
- [x] `config/wsgi.py` - WSGI application
- [x] `config/asgi.py` - ASGI application
- [x] `config/celery.py` - Celery configuration

### ✓ Core App (core/)
- [x] `core/models.py` - FarmerQuery model
- [x] `core/forms.py` - QueryInputForm
- [x] `core/views.py` - HomeView
- [x] `core/urls.py` - URL patterns
- [x] `core/admin.py` - Admin configuration
- [x] `core/apps.py` - App configuration
- [x] `core/tests.py` - Test placeholder
- [x] `core/templates/core/home.html` - Home template

### ✓ Market Data App (market_data/)
- [x] `market_data/models.py` - Market, MarketPrice, TransportCost models
- [x] `market_data/services.py` - MarketDataService
- [x] `market_data/adapters.py` - AgmarknetAdapter
- [x] `market_data/cache.py` - MarketDataCache
- [x] `market_data/admin.py` - Admin configuration
- [x] `market_data/apps.py` - App configuration
- [x] `market_data/tests.py` - Test placeholder

### ✓ AI Analysis App (ai_analysis/)
- [x] `ai_analysis/models.py` - PriceAnalysis, MarketRecommendation models
- [x] `ai_analysis/tasks.py` - Celery tasks
- [x] `ai_analysis/ml_models.py` - PricePredictor
- [x] `ai_analysis/predictor.py` - MarketAnalyzer
- [x] `ai_analysis/explainer.py` - ExplainabilityEngine
- [x] `ai_analysis/admin.py` - Admin configuration
- [x] `ai_analysis/apps.py` - App configuration
- [x] `ai_analysis/tests.py` - Test placeholder

### ✓ Templates and Static Files
- [x] `templates/base.html` - Base template with Bootstrap
- [x] `static/.gitkeep` - Static files directory
- [x] `logs/.gitkeep` - Logs directory

## Configuration Verification

### Environment Variables (.env)
The following variables need to be configured:

**Django Settings:**
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

**Database:**
- `DB_NAME` - PostgreSQL database name
- `DB_USER` - PostgreSQL username
- `DB_PASSWORD` - PostgreSQL password
- `DB_HOST` - PostgreSQL host
- `DB_PORT` - PostgreSQL port

**Redis:**
- `REDIS_HOST` - Redis host
- `REDIS_PORT` - Redis port
- `REDIS_DB` - Redis database number

**Celery:**
- `CELERY_BROKER_URL` - Celery broker URL
- `CELERY_RESULT_BACKEND` - Celery result backend URL

**Cache TTL:**
- `CACHE_TTL_REALTIME` - Real-time data cache TTL (seconds)
- `CACHE_TTL_HISTORICAL` - Historical data cache TTL (seconds)
- `CACHE_TTL_TRANSPORT` - Transport cost cache TTL (seconds)

**External APIs:**
- `AGMARKNET_API_URL` - Agmarknet API endpoint
- `AGMARKNET_API_KEY` - Agmarknet API key

**Application:**
- `DEFAULT_TRANSPORT_COST_PER_KM` - Default transport cost per km
- `SESSION_COOKIE_AGE` - Session cookie age (seconds)

## Dependencies Verification

All required packages are listed in `requirements.txt`:

**Core Django:**
- Django >= 5.0
- psycopg2-binary >= 2.9.9

**Async Processing:**
- celery >= 5.3.4
- redis >= 5.0.1

**Machine Learning:**
- scikit-learn >= 1.3.2
- statsmodels >= 0.14.1
- shap >= 0.44.0

**HTTP Requests:**
- requests >= 2.31.0

**Testing:**
- hypothesis >= 6.92.1
- pytest >= 7.4.3
- pytest-django >= 4.7.0
- factory-boy >= 3.3.0

**Environment:**
- python-decouple >= 3.8

## Quick Start Commands

```bash
# 1. Setup (automated)
bash setup.sh

# 2. Manual setup steps
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings

# 3. Database setup
createdb farmer_market_advisor
python manage.py migrate

# 4. Create admin user
python manage.py createsuperuser

# 5. Run services
# Terminal 1: Redis
redis-server

# Terminal 2: Celery
celery -A config worker -l info

# Terminal 3: Django
python manage.py runserver
```

## Verification Tests

After setup, verify the installation:

```bash
# Check Django installation
python manage.py check

# Check database connection
python manage.py dbshell

# Check migrations
python manage.py showmigrations

# Run tests
pytest
```

## Next Steps

After completing this task, the following tasks will implement:
1. Market data models and database schema
2. Core functionality and forms
3. AI analysis components
4. User interface and templates
5. Testing suite

## Requirements Satisfied

This setup satisfies the following requirements:
- **Requirement 10.1**: Django MVT architecture
- **Requirement 10.2**: Separate Django apps (core, market_data, ai_analysis)
- **Requirement 10.7**: Environment variables for configuration

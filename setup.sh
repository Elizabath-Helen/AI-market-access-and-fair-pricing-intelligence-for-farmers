#!/bin/bash

# Setup script for Farmer Market Advisor

echo "Setting up Farmer Market Advisor..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please update .env with your configuration"
fi

# Create logs directory if it doesn't exist
mkdir -p logs

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your database credentials"
echo "2. Create PostgreSQL database: createdb farmer_market_advisor"
echo "3. Run migrations: python manage.py migrate"
echo "4. Create superuser: python manage.py createsuperuser"
echo "5. Start Redis: redis-server"
echo "6. Start Celery: celery -A config worker -l info"
echo "7. Run server: python manage.py runserver"

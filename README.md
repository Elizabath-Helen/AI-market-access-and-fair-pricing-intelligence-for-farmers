# Farmer Market Advisor

AI-powered market intelligence system for small and marginal farmers.

## Features

- AI-powered fair price analysis
- Profitable market recommendations
- Explainable AI reasoning
- Real-time market data integration
- Transport cost calculations

## Tech Stack

- Django 5.0+
- PostgreSQL 15+
- Redis 7+
- Celery 5+
- scikit-learn, statsmodels, SHAP

## Setup Instructions

### Prerequisites

- Python 3.10+
- PostgreSQL 15+
- Redis 7+

### Installation

1. Clone the repository and navigate to the project directory

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

5. Update the `.env` file with your database credentials and other settings

6. Create the PostgreSQL database:
```bash
createdb farmer_market_advisor
```

7. Run migrations:
```bash
python manage.py migrate
```

8. Create a superuser:
```bash
python manage.py createsuperuser
```

9. Run the development server:
```bash
python manage.py runserver
```

10. In a separate terminal, start Redis:
```bash
redis-server
```

11. In another terminal, start Celery worker:
```bash
celery -A config worker -l info
```

## Project Structure

```
farmer_market_advisor/
├── config/              # Django project settings
├── core/                # Core app - user workflows
├── market_data/         # Market data integration
├── ai_analysis/         # AI/ML engine
├── templates/           # HTML templates
├── static/              # CSS, JS, images
└── logs/                # Application logs
```

## Development

- Access admin panel at: http://localhost:8000/admin/
- Main application at: http://localhost:8000/

## Testing

Run tests with:
```bash
pytest
```

Run property-based tests:
```bash
pytest tests/property/
```

## License

MIT

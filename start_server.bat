@echo off
echo ========================================
echo Farmer Market Advisor - Starting Server
echo ========================================
echo.

echo Checking database migrations...
python manage.py migrate

echo.
echo Starting development server...
echo.
echo Visit: http://localhost:8000
echo Press CTRL+C to stop the server
echo.

python manage.py runserver

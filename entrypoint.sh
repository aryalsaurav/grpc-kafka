#!/bin/bash

# Exit script on error
set -e

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the Uvicorn server
echo "Starting Uvicorn server..."

exec gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3 --reload
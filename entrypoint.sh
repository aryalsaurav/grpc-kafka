#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "Waiting for PostgreSQL at $POSTGRES_HOST:$POSTGRES_PORT..."
  sleep 2
done

echo "PostgreSQL is ready."

# Only run migrations and collectstatic if running the dev server
# if [[ "$1" == "python3" && "$2" == "manage.py" && "$3" == "runserver" ]]; then
  echo "Running migrations..."
  python manage.py migrate --noinput

  echo "Collecting static files..."
  python manage.py collectstatic --noinput
# fi

echo "Starting: $@"
exec "$@"

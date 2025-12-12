#!/bin/bash

# Exit on error
set -e

echo "Waiting for PostgreSQL..."
while ! nc -z $POSTGRES_DB_HOST $POSTGRES_DB_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn..."
exec gunicorn vetlms.wsgi:application \
    --config /app/gunicorn.conf.py \
    --bind 0.0.0.0:8000 \
    --log-level info


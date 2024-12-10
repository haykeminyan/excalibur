#!/bin/bash

# Wait for the database to be ready
echo "Waiting for database..."
while ! nc -z $POSTGRES_HOST 5432; do
  sleep 1
done
echo "Database is ready."

# Run any migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the server
echo "Starting server..."
exec "$@"

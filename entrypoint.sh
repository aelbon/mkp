#!/bin/bash

# TODO debug.log should be turned off in production
echo "Ensuring debug.log file exists"
touch /app/debug.log

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Setting postgres env vars..."
export POSTGRES_USER=mkp
export POSTGRES_PASSWORD=mkp

echo "Exec the rest of the command line:"
echo "$@"
exec $@
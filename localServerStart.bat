@echo off
echo:
echo:
echo:
echo:
echo ======================================
echo:
echo ==== Ensuring debug.log exists    ====
IF NOT EXIST debug.log (
    echo Creating debug.log
    type NUL > debug.log
)
echo ==== Updating python packages     ====
pip install --require-virtualenv --quiet -r requirements.txt

echo:
echo ==== Starting postgres            ====

SET COMPOSE_IGNORE_ORPHANS=True
docker compose -f docker-compose-local.yml up -d

echo:
echo ==== Applying database migrations ====
python manage.py migrate

echo:
echo ==== Collecting static files      ====
python manage.py collectstatic --noinput

@REM Next statements have no influence here, so they are commented out
@REM SET POSTGRES_USER=mkp
@REM SET POSTGRES_PASSWORD=mkp

echo:
echo ==== Django RunServer             ====
python manage.py runserver 0.0.0.0:8000

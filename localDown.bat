@echo off

@REM Docker compose down with -v flag can give ownership problems
@REM when starting the containers again. This script will remove
@REM the volumes as well (if the -v flag is set) to avoid this.

REM Check for the -v flag
SET VOLUME_FLAG=0
IF "%1"=="-v" SET VOLUME_FLAG=1

docker-compose -f docker-compose-local.yml down

IF %VOLUME_FLAG%==1 (
    docker volume rm django-tryout_postgres_data
    docker volume rm django-tryout_static_volume
)

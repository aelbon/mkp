echo:
echo ==== Starting Docker Compose services ====
SET COMPOSE_IGNORE_ORPHANS=True
docker-compose -f docker-compose-local-containers.yml up -d

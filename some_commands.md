# Django development

```bash
python manage.py collectstatic
```
(gather all static files and cop them into the STATIC_ROOT directory)  

```bash 
python manage.py runserver 0.0.0.0:8000
```

```bash 
python manage.py makemigrations
```
(create database migrations based on changes you've made to your models;
    it does NOT apply it) 

```bash 
python manage.py makemigrations --dry-run
```
(Show what migrations would be made without actually creating files)

```bash 
python manage.py migrate
```

```bash 
python manage.py showmigrations
```
   
```bash 
python manage.py createsuperuser
```
   
```bash 
python manage.py flush
```
(delete data from the database)

# Docker

```bash 
docker-compose down -v
```
(stops and removes containers and volumes defined in docker-compose.yml)

```bash 
docker system prune -f
```  

```bash 
docker-compose up --build -d
```  
(Builds the Docker images if they have changed, creates and starts the containers in detached mode (running in the background), as defined in the docker-compose.yml file)


```bash 
docker-compose logs -f
```  
Shows logs from all containers

```bash 
docker-compose exec django bash
```  
(opens an interactive shell inside the django container)

```bash 
docker-compose exec django python manage.py migrate
```  
(Runs migrate command inside the running django container)

```bash 
docker-compose exec django python manage.py createsuperuser
```  
(create superuser with django rights (we hope))

```bash
docker-compose -f docker-compose-local.yml up -d
```
Start up local postgres for development

```bash
docker-compose -f docker-compose-local.yml down
```
Remove local postgres container

```bash
docker-compose -f docker-compose-local.yml down -v
```
Remove local postgres container and related volumes
THIS IS NOT RECOMMENDED when using docker-compose up after this (can give migrate problems because of ownership)
For complete volume removal use after this (but be careful about what you delete):
docker volume prune



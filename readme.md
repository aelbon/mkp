# Django Example Project

### Table of Contents  

- [Projedct setup](#project-setup)
- [Cloning the Repository](#cloning-the-repository)
- [Running the Django Project in Development](#running-the-django-project-in-development)
- [Running the Project Using Docker Compose](#running-the-project-using-docker-compose)
- [Building the Docker Image](#building-the-docker-image)
- [Project Layout](#project-layout)
- [GitLab Pipeline](#gitlab-pipeline)
- [Improving](#improving)
- [Some links](#some-links)

## Overview

This repository contains a Django [example project](https://docs.djangoproject.com/en/5.1/intro/tutorial01/) with added functionality to demonstrate how a marketplace application might be implemented using Django. **Note:** This is a minimal implementation due to time constraints, so the functionality is limited.

### Features

- **Main Page**: A simple landing page.
- **Signup Screen**: Currently non-functional, placeholder only.
- **View Listings Page**: Displays available listings.
- **View Singular Listing Page**: Details of a single listing.
- **Listing Create Form**: Form to create a new listing.
- **Static FAQ Page**: A basic FAQ page.
- **Automatic deployment**: Deployed to a production-like environment using gitlab ci/cd

A "Production" version of the application is hosted on [miekeservices](http://miekeservices.soops.intern:3333/)

---
&nbsp;

# Project setup

## Prerequisites for this project

To set up and run this project, you need the following tools installed:

- **Git**: Version control system for cloning the repository.
- **Python**: Programming language required to run the Django application. Minimum version 12. Make SURE its added to your path.
- **PostgreSQL**: Database server (or use the Docker setup).
- **Docker/Docker Compose**: For containerized deployment.
- **WSL** (Windows only): For running a Linux-based environment.
- **Terminal Knowledge**: Familiarity with command-line tools.

---
&nbsp;

## Cloning the Repository

Clone this repository from GitLab using the following command:

```bash
git clone http://gitlab.soops.intern/soops/marketplaces/django-tryout.git
```

Alternatively, click the blue "Code" button on GitLab for more options to download the repository.

Configure Git with your username and email:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@address.com"
```

---
&nbsp;

## Running the Django Project in Development

### Prerequisites

1. Install Python on your local machine.
2. Install PostgreSQL and ensure it is running.
3. Configure the PostgreSQL database if needed (update `DATABASES` settings in `settings.py`).

**Alternative:** Use the Docker-based database configuration from the **docker compose** by running:

```bash
docker compose up db -d
```

This will spin up a PostgreSQL database with the correct configuration for development.

---

### Steps

1. Create a virtual environment in `venv/`

   ```bash
   python -m venv venv
   ```

   Activate the venv if VsCode did not do that automatically yet:

   MsWindows powershell:

   ```ps2
   .\venv\Scripts\Activate.ps1
   ```

   Unix:

   ```bash
      . venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run database migrations:

   ```bash
   python manage.py migrate
   ```

4. Start the development server (on all local loopback interfaces!):

   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

5. Open your browser and navigate to [http://localhost:8000](http://localhost:8000) 


The development server auto-updates whenever source code changes.

---
&nbsp;

## Running the Project Using Docker Compose

### Prerequisites

1. Ensure Docker/Docker desktop is installed.
2. Set up an insecure Docker registry.

To add the gitlab registry to the docker engine.
In docker desktop go to settings/docker engine and add to

```bash
"insecure-registries": [
    "gitlab.soops.intern:5050"
  ]
```

In my case the text field will look like this:

```bash
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "experimental": false,
  "insecure-registries": [
    "gitlab.soops.intern:5050"
  ]
}
```

---

### Steps

The docker compose configuration can be found in `docker-compose.yml`.

1. Pull the Docker image and start the containers:

   ```bash
   docker compose up
   ```

   This pulls the latest image of the application from gitlab and starts the services.

2. Open a browser and [navigate](http://localhost:3333) to the url `http://localhost:3333`

---
&nbsp;

## Building the Docker Image

**Note:** Running the container standalone is not recommended, as it depends on a database connection and requires Nginx to serve static files properly. For that running the application with docker compose is preffered.

However knowledge about building docker images is needed when expanding on this project in the future. Below some basic commands for building and running the docker container.
<!-- link to docker docs -->

### Steps

1. Build the Docker image:

   ```bash
   docker build -t <image-name> .
   ```

   Replace `<image-name>` with your preferred image name.

2. Run the Docker image:

   ```bash
   docker run -p 8000:8000 <image-name>
   ```

   In actuality database variables are needed to be able to connect to a database. These variables can be passed through like this:

   ```bash
   docker run -p 8000:8000 \
   -e POSTGRES_DB=postgres \
   -e POSTGRES_USER=postgres \
   -e POSTGRES_PASSWORD=1234 \
   -e POSTGRES_HOST=db \
   -e POSTGRES_PORT=5432 \
   <image-name>
   ```

3. Debugging a Docker container:
   - Access the container's shell:

     ```bash
     docker exec -it <container-id> /bin/bash
     ```

   - Replace `<container-id>` with the running container ID.

        You can also overwrite the entrypoint of a container by using the `--entrypoint` flag. Example:

        ```bash
        docker run -p 8000:8000 -it --entrypoint "/bin/bash" <image-name>
        ```

        To start the docker container on the shell. `-it` makes it so the input/oputput of the container is bound to the terminal.

---
&nbsp;

# Project Layout

This Django application is divided into three smaller parts (referred to as ["applications"](https://docs.djangoproject.com/en/5.1/ref/applications/) in Django):  

- **website**: The base folder containing project configuration.  
- **shop**: The application where the shop functionality is implemented.  
- **polls**: An application created as part of the Django tutorial.

### Git/GitLab Files  

These files are related to version control and CI/CD processes:  

- **.git**: A hidden folder that makes this directory a Git repository.  
- **.gitignore**: Specifies files and folders Git should ignore when tracking changes.  
- **.gitlab-ci.yml**: Defines the GitLab CI/CD pipeline executed on every commit.  
- **README.md**: This documentation file you're currently reading.

### Docker Environment  

These files facilitate containerization and managing the application stack:  

- **Dockerfile**: Instructions for building the Django application container.  
- **docker-compose.yml**: Configuration file for running multiple containers, representing the complete application stack.

### Other Files  

Additional configuration and management files include:  

- **nginx.conf**: Configuration file for Nginx, used as part of the application stack.  
- **manage.py**: A command-line utility for interacting with the Django application, such as running the server, applying migrations, or managing the database.

---
&nbsp;

# Project stack

- nginx
- django
- postgresql datbase

**Nginx**: acts as a reverse proxy, forwarding incoming requests to the Django application. It also handles:

- Serving static files (e.g., CSS, JavaScript, and images) to improve performance.
- Load balancing and caching, if configured, to optimize request handling.

**Django**: serves as the backend framework responsible for:

- Handling incoming HTTP requests.
- Executing business logic and interacting with the PostgreSQL database to fetch or modify data.
- Generating dynamic HTML pages and API responses.

**PostgreSQL**: is the database used to:

- Store data for the application.
- Ensure data integrity and provide support for complex queries and transactions.

---
&nbsp;

# GitLab Pipeline

The GitLab CI/CD pipeline (found in `.gitlab-ci.yml`) automates the process of building, testing (not in this project) and deploying Docker containers to a production environment. It consists of the following stages:

### Stages

1. **Build**: The Docker image is built using the `docker:latest` image and pushed to the GitLab registry with both a commit-specific tag and a `latest` tag.
2. **Test**: Currently, no test stage is defined in the pipeline.
3. **Deploy**: The built Docker images are deployed to the production environment on the `mieke.soops.intern` server using `docker compose`.

### Pipeline Details

- **Build Stage**:
  - This stage triggers only for commits to the `main` branch.
  - It builds the Docker image using `docker build`, tags the image with both the `commit SHA` and `latest`, and pushes the image to the GitLab registry.

- **Deploy Stage**:
  - This stage also runs only for the `main` branch.
  - It prepares the environment by installing necessary SSH dependencies and using `ssh-agent` to authenticate with the target server.
  - Docker Compose is used to pull the latest images and deploy the application on the production server (`mieke`).

### Variables

- `TAG_LATEST`: Tags the Docker image with the `latest` tag.
- `TAG_COMMIT`: Tags the Docker image with the short commit SHA for versioning.

### Deployment Environment

- **Name**: production
- **URL**: [Production Site](http://miekeservices.soops.intern:3333/)

This setup ensures that only the `main` branch is used for production builds and deployments, allowing for smooth and automated workflows.

---
&nbsp;

# Improving

This project was made to demonstrate how marketplaces application might be implemented using Django, but how can this be expanded?

### 1. **RLS (Row-Level Security)**

- Look into implementing Row-Level Security for fine-grained data access control based on user roles.

### 2. **HTMX for UX Improvement**

- Use HTMX to enhance UX.

      For instance in [listing create form](http://miekeservices.soops.intern:3333/watches/listing/create). When an invallid form is send the page is reloaded with a new form containing all the errors. When this happends the images input is cleard. HTMX would make it so that the page doesnt have to be reloaded when the errors are returned.

### 3. **Pipeline Optimization**

- Ongoing optimization of the CI/CD pipeline to improve build times and efficiency.

      By caching more of the application build step. Or using a shell runnen to avoid spinning up containers for every step (this also has some drawbacks further research is recommended).

### 4. **Serving Images**

- Introduction of a more efficient method for serving images, ensuring faster load times and reduced bandwidth usage by using optimized image formats and or CDNs.

      Currently when an image is uploaded the entire file is checked to see what type of image it is. This is not very efficient. Likewise when serving the image the entire image is copied into memory before it can be served to the user. Streaming the images from a database or using a CDN would make this part of the process more efficient.

### 5. **Different Configuration Options**

- Implementation of flexible configuration options to allow easier switching between different environments (e.g., development, staging, production) without requiring code changes. This would simplify the setup and management of multiple deployment environments.

While further research and experimentation are needed, this project provides a solid foundation for building the future of marketplaces.

# Some links

- [Miekeservices](http://miekeservices.soops.intern:3333)
- [Nginx docs](https://nginx.org/en/docs/)
- [Docker docs](https://docs.docker.com/reference/cli/docker/)
- [Docker compose docs](https://docs.docker.com/compose/)
- [Gitlab ci/cd](https://docs.gitlab.com/ee/ci/)
- [Django Project Structure](https://medium.com/django-unleashed/django-project-structure-a-comprehensive-guide-4b2ddbf2b6b8)
- [Django example tuturial](https://docs.djangoproject.com/en/5.1/intro/tutorial01/)
- [Django htmx form example](https://www.youtube.com/watch?v=XdZoYmLkQ4w)

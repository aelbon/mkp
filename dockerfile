FROM python:3.13-slim

RUN apt-get update && apt-get install -y libpq-dev gcc

# set environment variables
# (prevent Python from writing pyc files and buffering output)
ENV APP=/app \
   PYTHONDONTWRITEBYTECODE=1 \
   PYTHONUNBUFFERED=1

WORKDIR $APP

RUN pip install --upgrade pip

COPY . .

# makes the entrypoint.sh script executable
RUN chmod +x entrypoint.sh

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# run entrypoint.sh once the container starts
ENTRYPOINT ["/app/entrypoint.sh"]
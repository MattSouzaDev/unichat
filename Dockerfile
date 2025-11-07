FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Env defaults
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=unichat.settings

# Make entrypoint executable
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Collect static (safe if all files are in repo)
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Use entrypoint to run migrations and start daphne binding to $PORT
ENTRYPOINT ["/entrypoint.sh"]
CMD ["daphne", "-b", "0.0.0.0", "-p", "${PORT:-8000}", "unichat.asgi:application"]

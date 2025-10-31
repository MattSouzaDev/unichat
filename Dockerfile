FROM python:3.11-slim

# System dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

WORKDIR /app

#Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Environment setup
ENV DJANGO_SETTINGS_MODULE=unichat.settings
ENV PYTHONUNBUFFERED=1

# Collect static files for production
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

#  Start command
CMD ["sh", "-c", "python manage.py migrate --noinput && daphne -b 0.0.0.0 -p 8000 unichat.asgi:application"]

# Use official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory inside the container
WORKDIR /app

COPY requirements.txt .

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files (optional if you use them)
RUN python manage.py collectstatic --noinput

# Expose port 8000
EXPOSE 8000

# Run the app using gunicorn (production)
CMD ["gunicorn", "job_platform.wsgi:application", "--bind", "0.0.0.0:8000"]

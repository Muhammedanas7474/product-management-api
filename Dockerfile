FROM python:3.13-slim

# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create logs directory for supervisor
RUN mkdir -p /var/log/supervisor

# Expose port
EXPOSE 8000

# Run migrations then start supervisor
CMD ["sh", "-c", "python manage.py migrate && supervisord -c deploy/supervisord.conf"]

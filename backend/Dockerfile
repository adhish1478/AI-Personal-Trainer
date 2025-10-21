FROM python:3.11-slim

# Prevents Python from writing pyc files to disk and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set working directory
WORKDIR /app

# Install system dependencies (for psycopg2, Pillow, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    netcat-traditional \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files (optional if you serve via CDN or Nginx)
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8000

# Default command (can be overridden by docker-compose)
CMD ["gunicorn", "backend.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]

RUN useradd -m appuser
USER appuser
# Stage 1: Builder Image
FROM python:3.12 AS builder

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# Install system dependencies, PostgreSQL dev libraries, gettext, and other tools
RUN apt-get update && \
    apt-get install -y \
    netcat-traditional \
    libpq-dev \
    gcc \
    gettext \
    locales \
    wget \
    build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Verify gettext installation
RUN msguniq --version

# Create necessary directories
RUN mkdir -p /usr/src/app/logs

# Upgrade pip and install dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
# Create the logs directory (if not already created)
RUN mkdir -p /usr/src/app/logs
RUN chmod -R 755 /usr/src/app/logs
COPY wait_for_service.py /usr/src/app/

# Install Celery and Flower in the final image to be able to run the Celery worker and Flower
RUN pip install celery
RUN pip install flower
# Copy the application files
COPY . .

# Run collectstatic to collect static files
RUN python manage.py collectstatic --noinput

# Stage 2: Production Image
FROM python:3.12-slim

# Set work directory
WORKDIR /usr/src/app

# Install PostgreSQL client libraries and clean up
RUN apt-get update && \
    apt-get install -y libpq5 gettext && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Verify gettext installation
RUN msguniq --version

# Copy installed dependencies from builder stage
COPY --from=builder /root/.local /root/.local

# Set PATH to include local pip installations
ENV PATH=/root/.local/bin:$PATH

# Copy application and collected static files
COPY --from=builder /usr/src/app /usr/src/app

# Ensure entrypoint script is executable
RUN chmod +x entrypoint.sh

# Specify the command to run on container start
CMD ["./entrypoint.sh"]

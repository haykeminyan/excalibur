# Stage 1: Builder Image
FROM python:3.12 AS builder

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# Install system dependencies, PostgreSQL dev libraries, and pip
RUN apt-get update && apt-get install -y \
    netcat-traditional \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /usr/src/app/logs
# Upgrade pip and install dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Run collectstatic to collect the static files in the build stage
RUN python manage.py collectstatic --noinput

# Stage 2: Production Image
FROM python:3.12-slim

# Set work directory
WORKDIR /usr/src/app

# Install PostgreSQL client libraries and clean up
RUN apt-get update && apt-get install -y libpq5 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Copy installed dependencies from builder stage
COPY --from=builder /root/.local /root/.local

# Set PATH to include local pip installations
ENV PATH=/root/.local/bin:$PATH

# Copy the rest of the application (including collected static files)
COPY --from=builder /usr/src/app /usr/src/app


# Ensure entrypoint script is executable
RUN chmod +x entrypoint.sh

# Specify the command to run on container start
CMD ["./entrypoint.sh"]

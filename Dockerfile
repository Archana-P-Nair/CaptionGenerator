# Use an official Python runtime as a parent image
# Switch to bookworm (Debian 12) which is the current stable release
FROM python:3.10-slim-bookworm

# Set the working directory to /app
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt /app/backend/requirements.txt

# Install python dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy the rest of the application
COPY backend /app/backend
COPY models /app/models
COPY tokenizer.p /app/tokenizer.p

# Define default port
ENV PORT=8000

# Expose the port
EXPOSE $PORT

# Run uvicorn server, binding to the PORT environment variable
CMD sh -c "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT}"

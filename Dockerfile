# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies if needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY source/ ./source/

# Copy .env file if it exists (for local development)
# In production, use environment variables or secrets management
COPY .env* ./

# Expose port for FastAPI application
EXPOSE 8000

# Default command - you can override this when running the container
# To run the Slack bot: docker run <image> python source/main.py
# To run the FastAPI app: docker run <image> uvicorn source.app:app --host 0.0.0.0 --port 8000
CMD ["uvicorn", "source.app:app", "--host", "0.0.0.0", "--port", "8000"]
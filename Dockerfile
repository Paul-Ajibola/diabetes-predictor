# Use an official lightweight Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered output for cleaner logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies if required (kept minimal for slim image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definition first for efficient Docker layer caching
COPY requirements_clean.txt ./requirements.txt

# Install dependencies without cache to keep image lightweight
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and models into the image
COPY app/ ./app/
COPY models/ ./models/

# Expose port 8000 for web traffic
EXPOSE 8000

# Healthcheck to verify the FastAPI container is running and healthy
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start Uvicorn pointing to FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

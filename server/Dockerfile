# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python packages
RUN pip install --no-cache-dir --timeout=600 -r requirements.txt

# Expose the port
EXPOSE 8001

# Default to running server (can be overridden)
CMD ["python", "server.py"]

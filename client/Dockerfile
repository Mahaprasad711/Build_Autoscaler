# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y netcat-openbsd

# Copy project files
COPY . .

# Install Python packages
RUN pip install --no-cache-dir --timeout=600 -r requirements.txt

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Run entrypoint script which waits for server then runs client.py
ENTRYPOINT ["./entrypoint.sh"]
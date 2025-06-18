
FROM python:3.12-slim

WORKDIR /app

# Install aiohttp for HTTP server/client
RUN pip install aiohttp==3.9.5

# Copy source code
COPY dispatcher.py .

# Run the server
CMD ["python", "dispatcher.py"]

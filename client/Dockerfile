FROM python:3.12-slim

WORKDIR /app

COPY . .

# Install system libraries for OpenCV + networking tools
RUN apt-get update && \
    apt-get install -y netcat-openbsd libgl1 libglib2.0-0 && \
    pip install --no-cache-dir requests opencv-python && \
    rm -rf /var/lib/apt/lists/*

CMD ["./entrypoint.sh"]

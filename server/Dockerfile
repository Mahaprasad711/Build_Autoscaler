FROM python:3.12-slim

RUN apt-get update && apt-get install -y libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY server.py .
COPY requirements.txt .

RUN pip install --no-cache-dir --timeout 600 -r requirements.txt

EXPOSE 8001 8002
CMD ["python", "server.py"]

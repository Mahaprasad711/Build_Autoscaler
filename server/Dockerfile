FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgl1 && rm -rf /var/lib/apt/lists/*

# ⬇️ Copy only requirements first (for caching)
COPY requirements.txt .

# ⬇️ Install dependencies
RUN pip install --no-cache-dir --timeout=600 -r requirements.txt

# ⬇️ Now copy the rest
COPY . .

EXPOSE 8001

CMD ["python", "server.py"]
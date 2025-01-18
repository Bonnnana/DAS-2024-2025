FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    libta-lib0-dev \
    && pip install --no-cache-dir -r requirements.txt.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 5002

CMD ["python", "app.py"]

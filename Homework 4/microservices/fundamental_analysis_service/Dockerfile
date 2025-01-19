FROM python:3.9-slim

COPY microservices/fundamental_analysis_service/ /app
COPY shared_logic /app/shared_logic

RUN apt-get update && apt-get install -y \
    build-essential \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgfortran5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5003

CMD ["python", "app.py"]

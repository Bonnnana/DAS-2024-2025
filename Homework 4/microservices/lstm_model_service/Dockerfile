FROM python:3.7-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY microservices/lstm_model_service/ /app
COPY shared_logic /app/shared_logic

RUN apt-get update && apt-get install -y \
    build-essential \
    libhdf5-dev \
    libfreetype6-dev \
    libjpeg-dev \
    zlib1g-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5004

CMD ["python", "app.py"]

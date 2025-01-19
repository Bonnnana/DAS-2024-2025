FROM python:3.7-slim

WORKDIR /app

COPY stockApi.py /app
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "stockApi.py"]

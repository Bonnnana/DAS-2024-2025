FROM python:3.7-slim

WORKDIR /app

COPY microservices/most_liquid_service/ /app

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5005

CMD ["python", "app.py"]

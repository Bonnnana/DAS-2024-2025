FROM python:3.7-slim

WORKDIR /app

COPY microservices/issuers_scraping_service/ /app
COPY shared_logic /app/shared_logic

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

CMD ["python", "app.py"]

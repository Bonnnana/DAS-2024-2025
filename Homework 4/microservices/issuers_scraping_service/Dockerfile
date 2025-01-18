FROM python:3.7-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt.txt

EXPOSE 5001

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

CMD ["python", "app.py"]

FROM python:3.7-slim

WORKDIR /app

COPY microservices/technical_analysis_service/ /app
COPY shared_logic /app/shared_logic

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    tar \
    gcc \
    && wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
    && tar -xzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib \
    && ./configure --prefix=/usr \
    && make \
    && make install \
    && cd .. \
    && rm -rf ta-lib ta-lib-0.4.0-src.tar.gz \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 5002

CMD ["python", "app.py"]

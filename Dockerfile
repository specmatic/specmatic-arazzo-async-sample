FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app

WORKDIR /app

# Install dependencies
COPY requirements.txt .
COPY .env .
RUN pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

# Copy services
COPY ./location_api ./location_api
COPY ./order_api ./order_api

CMD ["python", "-c", "print('Image built. Override command in compose.')"]

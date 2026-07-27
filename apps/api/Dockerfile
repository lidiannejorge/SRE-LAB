FROM python:3.12-slim

WORKDIR /app


RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*


COPY apps/api/requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY apps/api/app.py .


COPY shared ./shared


ENV PYTHONPATH=/app


# Dynatrace / OpenTelemetry
ENV OTEL_SERVICE_NAME=sre-api


EXPOSE 5000


CMD ["python", "app.py"]

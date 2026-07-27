FROM python:3.12-slim

WORKDIR /app

COPY services/pedido-service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY services/pedido-service/app.py .

COPY shared ./shared

ENV PYTHONPATH=/app

EXPOSE 5002

CMD ["python", "app.py"]

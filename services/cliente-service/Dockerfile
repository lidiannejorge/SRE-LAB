FROM python:3.12-slim

WORKDIR /app

COPY services/cliente-service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY services/cliente-service/app.py .

COPY shared ./shared

ENV PYTHONPATH=/app

EXPOSE 5001

CMD ["python", "app.py"]

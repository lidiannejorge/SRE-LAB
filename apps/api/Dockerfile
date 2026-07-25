FROM python:3.12-slim


WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY app.py .


RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app


USER appuser


EXPOSE 5000


CMD ["python", "app.py"]

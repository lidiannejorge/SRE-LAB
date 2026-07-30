import os
import psycopg2
import logging

from flask import Flask, Response, jsonify, request
from prometheus_client import Counter, generate_latest

# ==================================================
# OpenTelemetry Compartilhado
# ==================================================
from shared.telemetry import configure_telemetry

# ==================================================
# Flask
# ==================================================
app = Flask(__name__)

# ==================================================
# OpenTelemetry
# ==================================================
tracer = configure_telemetry(app)

# ==================================================
# Logging
# ==================================================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================================================
# Prometheus Metrics
# ==================================================
REQUEST_COUNT = Counter(
    "cliente_service_requests_total",
    "Total de requests",
    ["method", "endpoint", "status"]
)

# ==================================================
# Database
# ==================================================
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "sre_database")
DB_USER = os.getenv("DB_USER", "sre_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "sre_password")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


# ==================================================
# Health
# ==================================================
@app.route("/health")
def health():

    with tracer.start_as_current_span("cliente-health"):

        logger.info("Health check cliente-service")

        return jsonify({
            "status": "UP",
            "service": "cliente-service"
        })


# ==================================================
# GET Clientes
# ==================================================
@app.route("/clientes", methods=["GET"])
def listar_clientes():

    with tracer.start_as_current_span("listar-clientes"):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id,nome,email FROM clientes"
        )

        clientes = [
            {
                "id": row[0],
                "nome": row[1],
                "email": row[2]
            }
            for row in cursor.fetchall()
        ]

        cursor.close()
        conn.close()

        REQUEST_COUNT.labels(
            "GET",
            "/clientes",
            "200"
        ).inc()

        logger.info("Clientes listados com sucesso")

        return jsonify(clientes)


# ==================================================
# POST Cliente
# ==================================================
@app.route("/clientes", methods=["POST"])
def criar_cliente():

    with tracer.start_as_current_span("criar-cliente"):

        dados = request.json

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO clientes (nome,email)
            VALUES (%s,%s)
            RETURNING id
            """,
            (
                dados["nome"],
                dados["email"]
            )
        )

        cliente_id = cursor.fetchone()[0]

        conn.commit()

        cursor.close()
        conn.close()

        REQUEST_COUNT.labels(
            "POST",
            "/clientes",
            "201"
        ).inc()

        logger.info(
            f"Cliente criado com id={cliente_id}"
        )

        return jsonify({
            "id": cliente_id,
            "status": "created"
        }), 201


# ==================================================
# Metrics
# ==================================================
@app.route("/metrics")
def metrics():

    return Response(
        generate_latest(),
        mimetype="text/plain"
    )


# ==================================================
# Start
# ==================================================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001
    )

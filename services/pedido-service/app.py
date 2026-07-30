import os
import psycopg2
import logging

from flask import Flask, Response, jsonify, request
from prometheus_client import Counter, generate_latest

# ==========================
# OpenTelemetry Compartilhado
# ==========================
from shared.telemetry import configure_telemetry


# ==========================
# Logging
# ==========================
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pedido-service")


# ==========================
# Flask
# ==========================
app = Flask(__name__)


# ==========================
# OpenTelemetry
# ==========================
tracer = configure_telemetry(app)


# ==========================
# Prometheus
# ==========================
REQUEST_COUNT = Counter(
    "pedido_service_requests_total",
    "Total de requests do pedido service",
    ["method", "endpoint", "status"]
)


# ==========================
# Database
# ==========================
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


# ==========================
# Health
# ==========================
@app.route("/health")
def health():

    with tracer.start_as_current_span("pedido-health"):

        logger.info(
            "Health check pedido-service"
        )

        return jsonify({
            "status": "UP",
            "service": "pedido-service"
        })


# ==========================
# GET Pedidos
# ==========================
@app.route("/pedidos", methods=["GET"])
def listar_pedidos():

    with tracer.start_as_current_span("listar-pedidos"):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id, cliente_id, produto, valor, criado_em
            FROM pedidos
            """
        )

        pedidos = [
            {
                "id": row[0],
                "cliente_id": row[1],
                "produto": row[2],
                "valor": float(row[3]),
                "criado_em": str(row[4])
            }
            for row in cursor.fetchall()
        ]

        cursor.close()
        conn.close()

        REQUEST_COUNT.labels(
            "GET",
            "/pedidos",
            "200"
        ).inc()

        logger.info(
            "Pedidos listados com sucesso"
        )

        return jsonify(pedidos)


# ==========================
# POST Pedido
# ==========================
@app.route("/pedidos", methods=["POST"])
def criar_pedido():

    with tracer.start_as_current_span("criar-pedido"):

        dados = request.json

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO pedidos
            (cliente_id, produto, valor)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (
                dados["cliente_id"],
                dados["produto"],
                dados["valor"]
            )
        )

        pedido_id = cursor.fetchone()[0]

        conn.commit()

        cursor.close()
        conn.close()

        REQUEST_COUNT.labels(
            "POST",
            "/pedidos",
            "201"
        ).inc()

        logger.info(
            f"Pedido criado com id={pedido_id}"
        )

        return jsonify({
            "id": pedido_id,
            "status": "created"
        }), 201


# ==========================
# Metrics
# ==========================
@app.route("/metrics")
def metrics():

    return Response(
        generate_latest(),
        mimetype="text/plain"
    )


# ==========================
# Start
# ==========================
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5002
    )

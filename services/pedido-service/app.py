from flask import Flask, Response, jsonify, request
import psycopg2
import os

from prometheus_client import Counter, generate_latest


app = Flask(__name__)


REQUEST_COUNT = Counter(
    "pedido_service_requests_total",
    "Total de requests do pedido service",
    ["method", "endpoint", "status"]
)



DB_HOST = os.getenv(
    "DB_HOST",
    "sre-postgres"
)

DB_NAME = os.getenv(
    "DB_NAME",
    "sre_database"
)

DB_USER = os.getenv(
    "DB_USER",
    "sre_user"
)

DB_PASSWORD = os.getenv(
    "DB_PASSWORD",
    "sre_password"
)



def get_connection():

    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )



@app.route("/health")
def health():

    return jsonify(
        {
            "status": "UP",
            "service": "pedido-service"
        }
    )



@app.route("/pedidos", methods=["GET"])
def listar_pedidos():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            id,
            cliente_id,
            produto,
            valor,
            criado_em
        FROM pedidos
        """
    )


    pedidos = []


    for row in cursor.fetchall():

        pedidos.append(
            {
                "id": row[0],
                "cliente_id": row[1],
                "produto": row[2],
                "valor": float(row[3]),
                "criado_em": str(row[4])
            }
        )


    cursor.close()
    conn.close()


    REQUEST_COUNT.labels(
        "GET",
        "/pedidos",
        "200"
    ).inc()


    return jsonify(pedidos)



@app.route("/pedidos", methods=["POST"])
def criar_pedido():

    dados = request.json


    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO pedidos
        (
            cliente_id,
            produto,
            valor
        )

        VALUES
        (
            %s,
            %s,
            %s
        )

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


    return jsonify(
        {
            "id": pedido_id,
            "message": "Pedido criado"
        }
    ),201



@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype="text/plain"
 	)

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5002
    )

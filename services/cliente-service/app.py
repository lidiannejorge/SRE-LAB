from flask import Flask, Response, jsonify, request
import psycopg2
from prometheus_client import Counter, generate_latest
import os


app = Flask(__name__)


REQUEST_COUNT = Counter(
    "cliente_service_requests_total",
    "Total de requests",
    ["method", "endpoint", "status"]
)


DB_HOST = os.getenv("DB_HOST", "sre-postgres")
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



@app.route("/health")
def health():

    return jsonify(
        {
            "status": "UP",
            "service": "cliente-service"
        }
    )



@app.route("/clientes", methods=["GET"])
def listar_clientes():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id,nome,email
        FROM clientes
        """
    )


    clientes = []

    for row in cursor.fetchall():

        clientes.append(
            {
                "id": row[0],
                "nome": row[1],
                "email": row[2]
            }
        )


    cursor.close()
    conn.close()


    REQUEST_COUNT.labels(
        "GET",
        "/clientes",
        "200"
    ).inc()


    return jsonify(clientes)



@app.route("/clientes", methods=["POST"])
def criar_cliente():

    dados = request.json


    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO clientes(nome,email)
        VALUES(%s,%s)
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


    return jsonify(
        {
            "id": cliente_id,
            "message": "Cliente criado"
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
        port=5001
    )

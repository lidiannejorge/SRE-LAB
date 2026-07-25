from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)


# Habilita métricas para Prometheus
metrics = PrometheusMetrics(app)


@app.route("/")
def home():

    return jsonify(
        {
            "application": "SRE LAB API",
            "status": "running"
        }
    )


@app.route("/health")
def health():

    return jsonify(
        {
            "status": "UP"
        }
    )


@app.route("/users")
def users():

    return jsonify(
        [
            {
                "id": 1,
                "name": "Lidiane"
            },
            {
                "id": 2,
                "name": "SRE User"
            }
        ]
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )

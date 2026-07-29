import os
import requests
import logging
from flask import Flask, jsonify
from prometheus_flask_exporter import PrometheusMetrics

# ==================================================
# OpenTelemetry
# ==================================================
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# ==================================================
# Flask
# ==================================================
app = Flask(__name__)

# Prometheus Metrics
metrics = PrometheusMetrics(app)

# ==================================================
# OpenTelemetry Configuration
# ==================================================
service_name = os.getenv("OTEL_SERVICE_NAME", "sre-api")
otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4318")

trace.set_tracer_provider(TracerProvider())
tracer_provider = trace.get_tracer_provider()

otlp_exporter = OTLPSpanExporter(endpoint=f"{otlp_endpoint}/v1/traces")
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)

# Instrumentação
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
tracer = trace.get_tracer(service_name)

# Logging configurado para incluir trace_id
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==================================================
# Microservices URLs
# ==================================================
CLIENTE_SERVICE_URL = os.getenv("CLIENTE_SERVICE_URL", "http://cliente-service:5001")
PEDIDO_SERVICE_URL = os.getenv("PEDIDO_SERVICE_URL", "http://pedido-service:5002")

# ==================================================
# Rotas
# ==================================================
@app.route("/")
def home():
    with tracer.start_as_current_span("home-request"):
        logger.info("Home endpoint chamado")
        return jsonify({"application": "SRE LAB API", "status": "running"})

@app.route("/health")
def health():
    with tracer.start_as_current_span("health-check"):
        logger.info("Health check chamado")
        return jsonify({"status": "UP"})

@app.route("/users")
def users():
    with tracer.start_as_current_span("list-users"):
        logger.info("Listando usuários")
        return jsonify([
            {"id": 1, "name": "Lidiane"},
            {"id": 2, "name": "SRE User"}
        ])

@app.route("/clientes")
def clientes():
    with tracer.start_as_current_span("call-cliente-service"):
        response = requests.get(f"{CLIENTE_SERVICE_URL}/clientes")
        logger.info("Chamando cliente-service")
        return jsonify(response.json())

@app.route("/pedidos")
def pedidos():
    with tracer.start_as_current_span("call-pedido-service"):
        response = requests.get(f"{PEDIDO_SERVICE_URL}/pedidos")
        logger.info("Chamando pedido-service")
        return jsonify(response.json())

@app.route("/erro")
def erro():
    with tracer.start_as_current_span("simulate-error") as span:
        try:
            raise Exception("Erro simulado SRE para teste de observabilidade")
        except Exception as exc:
            span.record_exception(exc)
            span.set_status(Status(StatusCode.ERROR))
            logger.error(f"Erro simulado capturado: {exc}")
            raise

# ==================================================
# Global Exception Handler
# ==================================================
@app.errorhandler(Exception)
def handle_exception(error):
    logger.error(f"Exceção global: {error}")
    return jsonify({"error": str(error), "status": "FAILED"}), 500

# ==================================================
# Start
# ==================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


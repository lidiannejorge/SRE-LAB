import os

from flask import Flask, jsonify

from prometheus_flask_exporter import PrometheusMetrics


# ==================================================
# OpenTelemetry
# ==================================================

from opentelemetry import trace

from opentelemetry.sdk.trace import TracerProvider

from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor
)

from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter
)

from opentelemetry.instrumentation.flask import (
    FlaskInstrumentor
)


# ==================================================
# Flask
# ==================================================

app = Flask(__name__)


# ==================================================
# Prometheus Metrics
# ==================================================

metrics = PrometheusMetrics(app)


# ==================================================
# OpenTelemetry Configuration
# ==================================================

service_name = os.getenv(
    "OTEL_SERVICE_NAME",
    "sre-api"
)

otlp_endpoint = os.getenv(
    "OTEL_EXPORTER_OTLP_ENDPOINT",
    "http://otel-collector:4318"
)


# Criar TracerProvider

trace.set_tracer_provider(
    TracerProvider()
)


tracer_provider = trace.get_tracer_provider()


# Exportador OTLP HTTP

otlp_exporter = OTLPSpanExporter(
    endpoint=f"{otlp_endpoint}/v1/traces"
)


span_processor = BatchSpanProcessor(
    otlp_exporter
)


tracer_provider.add_span_processor(
    span_processor
)


# Instrumentação Flask

FlaskInstrumentor().instrument_app(app)


tracer = trace.get_tracer(
    service_name
)


# ==================================================
# Rotas
# ==================================================

@app.route("/")
def home():

    with tracer.start_as_current_span("home-request"):

        return jsonify(
            {
                "application": "SRE LAB API",
                "status": "running"
            }
        )


@app.route("/health")
def health():

    with tracer.start_as_current_span("health-check"):

        return jsonify(
            {
                "status": "UP"
            }
        )


@app.route("/users")
def users():

    with tracer.start_as_current_span("list-users"):

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


@app.route("/erro")
def erro():

    with tracer.start_as_current_span("simulate-error"):

        return jsonify(
            {
                "error": "Erro simulado SRE",
                "status": "FAILED"
            }
        ), 500


# ==================================================
# Start
# ==================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )

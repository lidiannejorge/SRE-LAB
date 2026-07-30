import os

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.flask import FlaskInstrumentor


def configure_telemetry(app, instrument_requests=False):

    service_name = os.getenv(
        "OTEL_SERVICE_NAME",
        "unknown-service"
    )

    endpoint = os.getenv(
        "OTEL_EXPORTER_OTLP_ENDPOINT",
        "http://otel-collector:4318"
    )

    current_provider = trace.get_tracer_provider()

    if not isinstance(current_provider, TracerProvider):

        resource = Resource.create({
            "service.name": service_name
        })

        provider = TracerProvider(resource=resource)

        exporter = OTLPSpanExporter(
            endpoint=f"{endpoint}/v1/traces"
        )

        provider.add_span_processor(
            BatchSpanProcessor(exporter)
        )

        trace.set_tracer_provider(provider)

    FlaskInstrumentor().instrument_app(app)

    if instrument_requests:
        from opentelemetry.instrumentation.requests import (
            RequestsInstrumentor,
        )

        RequestsInstrumentor().instrument()

    return trace.get_tracer(service_name)

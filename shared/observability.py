from prometheus_client import Counter, Histogram
import time


REQUEST_COUNTER = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["service", "method", "endpoint", "status"]
)


REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    ["service", "method", "endpoint"]
)


ERROR_COUNTER = Counter(
    "http_errors_total",
    "Total HTTP errors",
    ["service", "method", "endpoint", "status"]
)


def before_request():
    return time.time()


def after_request(service_name, endpoint, method, status_code, start_time):

    REQUEST_COUNTER.labels(
        service_name,
        method,
        endpoint,
        str(status_code)
    ).inc()

    REQUEST_DURATION.labels(
        service_name,
        method,
        endpoint
    ).observe(
        time.time() - start_time
    )

    if status_code >= 400:

        ERROR_COUNTER.labels(
            service_name,
            method,
            endpoint,
            str(status_code)
        ).inc()

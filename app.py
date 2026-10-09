
import os
import random
import time
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

APP_NAME = os.getenv("APP_NAME", "auth")
OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")

resource = Resource.create({
    "service.name": APP_NAME,
    "service.version": "1.0.0",
    "deployment.environment": "training",
})
provider = TracerProvider(resource=resource)
provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(endpoint=OTLP_ENDPOINT, insecure=True)
    )
)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(f"{APP_NAME}.tracer")


def auth_flow():
    with tracer.start_as_current_span("auth.login") as span:
        span.set_attribute("user.id", "23782")
        span.set_attribute("user.email", "mohammed@hotmail.com")
        span.set_attribute("user.name", "Mohammed Ahmed")
        span.set_attribute("client.address", "192.0.2.44")
        span.set_attribute("auth.password", "moh-ahmed22131")
        span.set_attribute("auth.token", "dsgjfdghj433ldjgnaasa=z1221dsfdsdsgsa")
        span.set_attribute("auth.result", "success")
        span.set_attribute("auth.mfa.enabled", True)
        


def payment_flow():
    with tracer.start_as_current_span("payment.authorize") as span:
        span.set_attribute("user.id", "user-demo-1042")
        span.set_attribute("payment.id", "pay-demo-7781")
        span.set_attribute("payment.amount", 149.95)
        span.set_attribute("payment.currency", "USD")
        span.set_attribute("payment.card.number", "4111111111111111")
        span.set_attribute("payment.card.cvv", "123")
        span.set_attribute("payment.card.brand", "visa")
        span.set_attribute("payment.result", "approved")
        time.sleep(random.uniform(0.05, 0.2))




def flight_flow():
    with tracer.start_as_current_span("flight.booking") as span:
        span.set_attribute("user.id", "user-demo-1042")
        span.set_attribute("flight.booking.id", "booking-demo-920")
        span.set_attribute("flight.number", "XY204")
        span.set_attribute("flight.route", "KRT-JED")
        span.set_attribute("flight.passenger.name", "Example Passenger")
        span.set_attribute("flight.passport.number", "P00000000")
        span.set_attribute("flight.seat", "14A")
        span.set_attribute("flight.result", "confirmed")
        time.sleep(random.uniform(0.05, 0.2))


flows = {"auth": auth_flow, "payment": payment_flow, "flight": flight_flow}

print(f"[{APP_NAME}] exporting traces to {OTLP_ENDPOINT}", flush=True)
try:
    while True:
        flows.get(APP_NAME, auth_flow)()
        print(f"[{APP_NAME}] emitted a trace batch", flush=True)
        time.sleep(5)
except KeyboardInterrupt:
    pass
finally:
    provider.force_flush()
    provider.shutdown()

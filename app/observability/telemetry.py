from opentelemetry import trace

from opentelemetry.sdk.trace import TracerProvider

from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)

provider = TracerProvider()

trace.set_tracer_provider(provider)

processor = SimpleSpanProcessor(
    ConsoleSpanExporter(out=__import__("sys").stdout)
)

provider.add_span_processor(processor)

tracer = trace.get_tracer("ai-assistant")
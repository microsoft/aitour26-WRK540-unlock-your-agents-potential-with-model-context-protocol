import logging
import os
import sys

from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def configure_oltp_grpc_tracing(logging_level: int = logging.INFO, tracer_name: str = __name__) -> trace.Tracer:
    # Check if OTEL endpoint is configured
    has_otel_endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT") is not None

    # Configure Tracing
    traceProvider = TracerProvider()

    # Add OTLP exporter for remote tracing only if endpoint is configured
    if has_otel_endpoint:
        logging.info("OTEL endpoint detected. Setting up OTLP tracing exporter.")
        otlp_processor = BatchSpanProcessor(OTLPSpanExporter())
        traceProvider.add_span_processor(otlp_processor)
    else:
        logging.info("No OTEL endpoint detected. Skipping OTLP tracing exporter.")

    trace.set_tracer_provider(traceProvider)

    # Configure Metrics
    if has_otel_endpoint:
        reader = PeriodicExportingMetricReader(OTLPMetricExporter())
        meterProvider = MeterProvider(metric_readers=[reader])
        metrics.set_meter_provider(meterProvider)
    else:
        # Set up a basic meter provider without exporters
        meterProvider = MeterProvider()
        metrics.set_meter_provider(meterProvider)

    # Configure Logging
    logger_provider = LoggerProvider()
    set_logger_provider(logger_provider)

    # Add OTLP exporter for remote logging only if endpoint is configured
    if has_otel_endpoint:
        logging.info("Setting up OTLP log exporter.")
        otlp_log_exporter = OTLPLogExporter()
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(otlp_log_exporter))

    # Always add Console exporter for local debugging
    console_log_exporter = ConsoleLogExporter()
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(console_log_exporter))

    # Always add a standard console handler for immediate visibility
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    # Configure the root logger
    root_logger = logging.getLogger()

    # Add OTLP handler if configured
    if has_otel_endpoint:
        handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
        handler.setFormatter(logging.Formatter("%(message)s"))
        root_logger.addHandler(handler)

    # Always add console handler
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging_level)

    return trace.get_tracer(tracer_name)

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

# Azure Monitor imports
try:
    from azure.monitor.opentelemetry.exporter import (
        AzureMonitorLogExporter,
        AzureMonitorMetricExporter,
        AzureMonitorTraceExporter,
    )
    AZURE_MONITOR_AVAILABLE = True
except ImportError:
    AZURE_MONITOR_AVAILABLE = False


def configure_oltp_grpc_tracing(logging_level: int = logging.INFO, tracer_name: str = __name__, azure_monitor_connection_string: str | None = None) -> trace.Tracer:
    # Check if OTEL endpoint is configured
    has_otel_endpoint = os.environ.get(
        "OTEL_EXPORTER_OTLP_ENDPOINT") is not None
    has_azure_monitor = azure_monitor_connection_string is not None and AZURE_MONITOR_AVAILABLE

    # Configure Tracing
    traceProvider = TracerProvider()

    # Add OTLP exporter for remote tracing only if endpoint is configured
    if has_otel_endpoint:
        logging.info(
            "OTEL endpoint detected. Setting up OTLP tracing exporter.")
        otlp_processor = BatchSpanProcessor(OTLPSpanExporter())
        traceProvider.add_span_processor(otlp_processor)
    else:
        logging.info(
            "No OTEL endpoint detected. Skipping OTLP tracing exporter.")

    # Add Azure Monitor exporter for tracing if configured
    if has_azure_monitor:
        logging.info(
            "Azure Monitor connection string detected. Setting up Azure Monitor tracing exporter.")
        azure_processor = BatchSpanProcessor(AzureMonitorTraceExporter(
            connection_string=azure_monitor_connection_string,
            disable_offline_storage=True))
        traceProvider.add_span_processor(azure_processor)

    trace.set_tracer_provider(traceProvider)

    # Configure Metrics
    metric_readers = []
    if has_otel_endpoint:
        metric_readers.append(
            PeriodicExportingMetricReader(OTLPMetricExporter()))
    if has_azure_monitor:
        metric_readers.append(PeriodicExportingMetricReader(
            AzureMonitorMetricExporter(connection_string=azure_monitor_connection_string,
                                       disable_offline_storage=True)))

    meterProvider = MeterProvider(
        metric_readers=metric_readers) if metric_readers else MeterProvider()
    metrics.set_meter_provider(meterProvider)

    # Configure Logging
    logger_provider = LoggerProvider()
    set_logger_provider(logger_provider)

    # Add OTLP exporter for remote logging only if endpoint is configured
    if has_otel_endpoint:
        logging.info("Setting up OTLP log exporter.")
        otlp_log_exporter = OTLPLogExporter()
        logger_provider.add_log_record_processor(
            BatchLogRecordProcessor(otlp_log_exporter))

    # Add Azure Monitor exporter for logging if configured
    if has_azure_monitor:
        logging.info("Setting up Azure Monitor log exporter.")
        azure_log_exporter = AzureMonitorLogExporter(
            connection_string=azure_monitor_connection_string,
            disable_offline_storage=True)
        logger_provider.add_log_record_processor(
            BatchLogRecordProcessor(azure_log_exporter))

    # Always add Console exporter for local debugging
    console_log_exporter = ConsoleLogExporter()
    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(console_log_exporter))

    # Create and configure the logging handler if OTEL endpoint or Azure Monitor is configured
    if has_otel_endpoint or has_azure_monitor:
        handler = LoggingHandler(level=logging.NOTSET,
                                 logger_provider=logger_provider)
        handler.setFormatter(logging.Formatter("%(message)s"))

    # Always add a standard console handler for immediate visibility
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    # Configure the root logger
    root_logger = logging.getLogger()

    # Add OTLP/Azure Monitor handler if configured
    if has_otel_endpoint or has_azure_monitor:
        root_logger.addHandler(handler)

    # Always add console handler
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging_level)

    return trace.get_tracer(tracer_name)

"""
FastAPI application for Package Sorting API.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import Response
import time
import os
from fastapi.middleware.cors import CORSMiddleware
import logging

from .models import PackageRequest, PackageResponse, HealthResponse
from .sort_packages import sort
from .auth import require_role

# Prometheus metrics (minimal)
try:
    from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
except Exception:  # pragma: no cover - optional dependency in dev
    Counter = None
    Histogram = None
    generate_latest = None
    CONTENT_TYPE_LATEST = "text/plain; version=0.0.4"

REQUEST_COUNT = Counter("app_http_requests_total", "Total HTTP requests") if Counter else None
REQUEST_LATENCY = Histogram("app_http_request_latency_seconds", "Request latency seconds") if Histogram else None

# OpenTelemetry tracing initialization
try:
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

    resource = Resource.create({"service.name": "package-sorting-api"})
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    # Instrument FastAPI app so incoming requests create spans
    FastAPIInstrumentor.instrument_app(app)
    TRACING_ENABLED = True
except Exception:
    TRACING_ENABLED = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Package Sorting API",
    description="REST API for sorting packages into appropriate stacks based on dimensions and mass",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/sort", response_model=PackageResponse)
async def sort_package(request: PackageRequest, _auth: None = Depends(require_role("sort:invoke"))) -> PackageResponse:
    """
    Sort a package into the appropriate stack.

    Determines the stack (STANDARD, SPECIAL, or REJECTED) for a package
    based on its dimensions and mass.
    """
    start = time.perf_counter()
    try:
        logger.info(f"Sorting package: width={request.width}, height={request.height}, length={request.length}, mass={request.mass}")

        stack = sort(request.width, request.height, request.length, request.mass)

        logger.info(f"Package sorted to: {stack}")

        return PackageResponse(stack=stack)

    except Exception as e:
        logger.error(f"Error sorting package: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        latency = time.perf_counter() - start
        if REQUEST_COUNT is not None:
            try:
                REQUEST_COUNT.inc()
            except Exception:
                pass
        if REQUEST_LATENCY is not None:
            try:
                REQUEST_LATENCY.observe(latency)
            except Exception:
                pass


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns the health status of the API.
    """
    return HealthResponse(status="healthy")


@app.get("/metrics")
async def metrics() -> Response:
    """Expose Prometheus metrics."""
    if generate_latest is None:
        return Response(content="metrics not available", media_type="text/plain")
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
"""FastAPI application for the Microsoft Purview Policy Simulator."""
from __future__ import annotations

import logging
import os
import time
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from .simulator import SimulationRequest, SimulationResult, evaluate_policies

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s – %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Microsoft Purview Policy Simulator",
    description=(
        "Simulate Microsoft Purview data-access policy evaluation. "
        "Upload policies, define a subject + resource + action, "
        "and instantly see which policies would grant or deny access."
    ),
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

# ---------------------------------------------------------------------------
# CORS – restrict to configured origins in production
# ---------------------------------------------------------------------------
_cors_origins_env = os.getenv("CORS_ORIGINS", "*")
_cors_origins = [o.strip() for o in _cors_origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Static files (frontend)
# ---------------------------------------------------------------------------
_static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=_static_dir), name="static")


# ---------------------------------------------------------------------------
# Request timing middleware
# ---------------------------------------------------------------------------
@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Any) -> Any:
    start = time.perf_counter()
    response = await call_next(request)
    elapsed = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{elapsed:.4f}s"
    return response


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def serve_index() -> HTMLResponse:
    """Serve the frontend SPA."""
    index_path = os.path.join(_static_dir, "index.html")
    with open(index_path, encoding="utf-8") as fh:
        content = fh.read()
    return HTMLResponse(content=content)


@app.get("/api/health", tags=["Health"])
async def health() -> Dict[str, str]:
    """Liveness / readiness probe."""
    return {"status": "ok", "version": app.version}


@app.post(
    "/api/simulate",
    response_model=SimulationResult,
    tags=["Simulation"],
    summary="Evaluate policies against a subject / resource / action triple",
)
async def simulate(request: Request, body: SimulationRequest) -> SimulationResult:
    """
    Accepts a list of Purview policies and a simulation context (subject,
    resource, action) and returns the access-evaluation result.
    """
    logger.info(
        "Simulation request: subject=%s action=%s resource=%s policies=%d",
        body.subject.id,
        body.action.value,
        body.resource.resource_path,
        len(body.policies),
    )
    result = evaluate_policies(body)
    logger.info(
        "Simulation result: access_granted=%s effect=%s",
        result.access_granted,
        result.effective_effect,
    )
    return result

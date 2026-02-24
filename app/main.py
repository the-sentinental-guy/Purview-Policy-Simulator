"""Purview Policy Simulator — FastAPI application."""
import time
import logging
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.models.simulation import SimulationRequest, SimulationResponse
from app.models.policy import PolicyTemplate
from app.engine.simulator import PolicySimulator
from app.mcp_client import mcp_client
from app.knowledge_base.dlp_templates import get_dlp_templates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Purview Policy Simulator",
    description="Simulate Microsoft Purview DLP, Sensitivity Label, and Compliance policies",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

simulator = PolicySimulator()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    mcp_available = await mcp_client.is_available()
    return {
        "status": "healthy",
        "version": "2.0.0",
        "mcp_available": mcp_available,
        "templates_loaded": len(get_dlp_templates()),
    }


@app.get("/templates", response_model=List[PolicyTemplate])
async def list_templates(category: str = None):
    """List all available DLP policy templates, optionally filtered by category."""
    templates = get_dlp_templates()
    if category:
        templates = [t for t in templates if t.category.lower() == category.lower()]
    return templates


@app.get("/templates/categories")
async def list_categories():
    """List all template categories."""
    templates = get_dlp_templates()
    categories: dict = {}
    for t in templates:
        cat = t.category
        categories[cat] = categories.get(cat, 0) + 1
    return {"categories": [{"name": k, "count": v} for k, v in sorted(categories.items())]}


@app.post("/simulate", response_model=SimulationResponse)
async def simulate_policy(request: SimulationRequest):
    """Simulate a Microsoft Purview policy based on a natural language description."""
    start = time.perf_counter()
    try:
        response = await simulator.simulate(request)
        response.processing_time_ms = (time.perf_counter() - start) * 1000

        if request.use_mcp and await mcp_client.is_available():
            template_names = [m.template.name for m in response.template_matches]
            enrichment = await mcp_client.enrich_simulation(request.query, template_names)
            response.documentation_links = enrichment.get("documentation_links", [])
            response.mcp_enriched = True

        return response
    except Exception as exc:
        logger.exception("Simulation error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/mcp/status")
async def mcp_status():
    """Check Microsoft Learn MCP server availability."""
    available = await mcp_client.is_available()
    tools = mcp_client._available_tools if available else []
    return {
        "available": available,
        "endpoint": mcp_client.endpoint,
        "tools": [t.get("name") for t in tools],
    }


# Serve static frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def serve_frontend():
    """Serve the frontend SPA."""
    return FileResponse("static/index.html")

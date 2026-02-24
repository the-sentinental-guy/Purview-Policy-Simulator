from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from simulator.config import APP_NAME, VERSION
from simulator.models.simulation import SimulationRequest, SimulationResult
from simulator.engine.simulator import SimulationEngine
from simulator.knowledge_base.dlp_templates import get_all_templates

app = FastAPI(title=APP_NAME, version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = SimulationEngine()

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


@app.get("/health")
async def health():
    return {"status": "healthy", "version": VERSION}


@app.get("/templates")
async def templates():
    all_templates = get_all_templates()
    categorized = {}
    for t in all_templates:
        cat = t.get("category", "General")
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append({
            "id": t["template_id"],
            "name": t["name"],
            "description": t["description"]
        })
    return {"categories": categorized, "total": len(all_templates)}


@app.post("/simulate", response_model=SimulationResult)
async def simulate(request: SimulationRequest):
    result = await engine.simulate(request.query, request.mcp_enabled)
    return result


# Serve static files - must be mounted AFTER API routes
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/")
    async def index():
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))

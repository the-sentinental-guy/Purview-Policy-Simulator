"""Simulation request and response models."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from .policy import PolicyTemplate
from .confidence import ConfidenceScore
from .effects import SimulationEffects


class SimulationRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Natural language policy description")
    use_mcp: bool = Field(default=False, description="Enable Microsoft Learn MCP enrichment")
    max_templates: int = Field(default=3, ge=1, le=10)


class TemplateMatch(BaseModel):
    template: PolicyTemplate
    confidence: ConfidenceScore
    similarity_score: float
    matched_keywords: List[str] = []
    matched_frameworks: List[str] = []


class GapAnalysis(BaseModel):
    covered: List[str] = []
    missing: List[str] = []
    recommendations: List[str] = []


class CustomConfiguration(BaseModel):
    title: str
    steps: List[str] = []
    locations: List[str] = []
    sensitive_info_types: List[str] = []
    actions: List[str] = []
    gap_analysis: Optional[GapAnalysis] = None


class MCPDocumentation(BaseModel):
    title: str
    url: str
    summary: str
    source: str = "Microsoft Learn"


class SimulationResponse(BaseModel):
    query: str
    intent: str
    entities: Dict[str, List[str]] = {}
    template_matches: List[TemplateMatch] = []
    custom_configuration: Optional[CustomConfiguration] = None
    effects: Optional[SimulationEffects] = None
    documentation_links: List[MCPDocumentation] = []
    troubleshooting_tips: List[str] = []
    mcp_enriched: bool = False
    processing_time_ms: float = 0.0

from pydantic import BaseModel, Field
from typing import List, Dict, Any


class SimulationRequest(BaseModel):
    query: str
    mcp_enabled: bool = True


class TemplateMatch(BaseModel):
    template: Dict[str, Any]
    confidence_score: float
    confidence_level: str
    effects: Dict[str, Any]
    explanation: str


class SimulationResult(BaseModel):
    query: str
    matches: List[TemplateMatch]
    nlp_analysis: Dict[str, Any]
    mcp_references: List[Dict[str, Any]] = Field(default_factory=list)
    summary: str
    timestamp: str

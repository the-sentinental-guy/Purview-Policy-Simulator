"""Knowledge base package."""
from app.knowledge_base.insider_risk import (
    get_insider_risk_templates,
    get_triggering_events,
    get_risk_indicators,
    get_investigation_workflow,
)
from app.knowledge_base.troubleshooting import get_troubleshooting_guide
from app.knowledge_base.architecture import get_architecture_reference

__all__ = [
    "get_insider_risk_templates",
    "get_triggering_events",
    "get_risk_indicators",
    "get_investigation_workflow",
    "get_troubleshooting_guide",
    "get_architecture_reference",
]

"""Effects data models."""
from pydantic import BaseModel
from typing import List, Optional


class SimulationEffects(BaseModel):
    blocked_actions: List[str] = []
    audited_actions: List[str] = []
    notifications: List[str] = []
    user_experience: str = ""
    admin_experience: str = ""
    false_positive_risk: str = "Low"
    deployment_recommendations: List[str] = []
    policy_tips: List[str] = []
    incident_reports: List[str] = []

from pydantic import BaseModel, Field
from typing import List, Dict, Any


class ExpectedEffects(BaseModel):
    blocked_actions: List[str] = Field(default_factory=list)
    audited_actions: List[str] = Field(default_factory=list)
    user_notifications: Dict[str, Any] = Field(default_factory=dict)
    admin_notifications: Dict[str, Any] = Field(default_factory=dict)
    false_positive_risk: str = "MEDIUM"
    deployment_recommendations: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    estimated_coverage: str = ""

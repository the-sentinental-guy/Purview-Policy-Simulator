"""Policy data models."""
from pydantic import BaseModel, Field
from typing import List, Optional


class PolicyLocation(BaseModel):
    name: str
    enabled: bool = True


class PolicyCondition(BaseModel):
    type: str
    values: List[str] = []
    operator: str = "ContainsSensitiveInformation"


class PolicyAction(BaseModel):
    type: str
    description: str
    severity: str = "medium"


class PolicyTemplate(BaseModel):
    id: str
    name: str
    category: str
    description: str
    keywords: List[str] = []
    locations: List[str] = []
    sensitive_info_types: List[str] = []
    actions: List[str] = []
    compliance_frameworks: List[str] = []
    severity: str = "medium"
    tags: List[str] = []
    source_url: str = ""
    specific_blocked_actions: List[str] = []
    specific_audit_actions: List[str] = []
    specific_notifications: List[str] = []
    specific_user_experience: str = ""
    specific_admin_experience: str = ""
    specific_policy_tips: List[str] = []

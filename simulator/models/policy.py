from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class PolicyCondition(BaseModel):
    content_contains: Optional[List[str]] = None
    share_with: Optional[str] = None
    content_count: Optional[Dict[str, int]] = None
    sender_domain: Optional[str] = None
    recipient_domain: Optional[str] = None
    document_property: Optional[Dict[str, str]] = None


class PolicyAction(BaseModel):
    block_sharing: bool = False
    encrypt: bool = False
    notify_user: bool = True
    notify_admin: bool = True
    generate_incident_report: bool = True
    restrict_access: bool = False
    apply_label: Optional[str] = None
    block_download: bool = False
    block_paste: bool = False


class DLPPolicy(BaseModel):
    template_id: str
    name: str
    description: str
    category: str
    subcategory: Optional[str] = None
    sensitive_info_types: List[str]
    locations: List[str]
    conditions: PolicyCondition
    actions: PolicyAction
    priority: int = 1
    regulatory_references: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)

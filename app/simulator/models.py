"""Data models for the Purview Policy Simulator."""
from __future__ import annotations

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class PolicyEffect(str, Enum):
    ALLOW = "Allow"
    DENY = "Deny"


class PolicyAction(str, Enum):
    READ = "Microsoft.Purview/accounts/data/read"
    MODIFY = "Microsoft.Purview/accounts/data/modify"
    READ_LINEAGE = "Microsoft.Purview/accounts/scan/read"
    DEVOPS_READ = "Microsoft.Purview/accounts/devops/read"
    DEVOPS_MODIFY = "Microsoft.Purview/accounts/devops/modify"


class SubjectType(str, Enum):
    USER = "User"
    GROUP = "Group"
    SERVICE_PRINCIPAL = "ServicePrincipal"


class Subject(BaseModel):
    id: str = Field(..., description="AAD object ID or UPN")
    subject_type: SubjectType = SubjectType.USER
    display_name: Optional[str] = None


class ResourcePathType(str, Enum):
    PURVIEW_ACCOUNT = "PurviewAccount"
    AZURE_STORAGE = "AzureStorage"
    AZURE_SQL = "AzureSQL"
    AZURE_DATA_LAKE = "AzureDataLakeStorage"
    AZURE_SYNAPSE = "AzureSynapse"


class Resource(BaseModel):
    resource_path: str = Field(
        ...,
        description=(
            "Full resource path, e.g. "
            "/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.Storage/storageAccounts/{account}"
        ),
    )
    resource_type: ResourcePathType = ResourcePathType.AZURE_STORAGE
    collection: Optional[str] = Field(
        None, description="Purview collection the resource belongs to"
    )


class PolicyStatement(BaseModel):
    effect: PolicyEffect
    actions: List[PolicyAction]
    subjects: List[Subject]
    resources: List[Resource]


class Policy(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    statements: List[PolicyStatement]
    enabled: bool = True


class SimulationRequest(BaseModel):
    subject: Subject
    resource: Resource
    action: PolicyAction
    policies: List[Policy]


class PolicyMatch(BaseModel):
    policy_id: str
    policy_name: str
    statement_index: int
    effect: PolicyEffect


class SimulationResult(BaseModel):
    access_granted: bool
    effective_effect: Optional[PolicyEffect]
    matched_policies: List[PolicyMatch]
    evaluation_notes: List[str]

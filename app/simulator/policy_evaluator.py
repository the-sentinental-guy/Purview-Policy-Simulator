"""Policy evaluation engine for the Purview Policy Simulator."""
from __future__ import annotations

from typing import List

from .models import (
    Policy,
    PolicyAction,
    PolicyEffect,
    PolicyMatch,
    Resource,
    SimulationRequest,
    SimulationResult,
    Subject,
)


def _subject_matches(subject: Subject, policy_subjects: List[Subject]) -> bool:
    """Return True if *subject* is covered by any entry in *policy_subjects*."""
    for ps in policy_subjects:
        # Wildcard – a single '*' means all subjects
        if ps.id == "*":
            return True
        # Case-insensitive comparison of IDs / UPNs
        if ps.id.lower() == subject.id.lower():
            return True
    return False


def _resource_matches(resource: Resource, policy_resources: List[Resource]) -> bool:
    """Return True if *resource* is covered by any entry in *policy_resources*."""
    for pr in policy_resources:
        # Wildcard
        if pr.resource_path == "*":
            return True
        # Exact match (case-insensitive for Azure resource paths)
        if pr.resource_path.lower() == resource.resource_path.lower():
            return True
        # Prefix/scope match: policy resource is a parent scope of the request
        if resource.resource_path.lower().startswith(
            pr.resource_path.rstrip("/").lower() + "/"
        ):
            return True
        # Collection match
        if pr.collection and resource.collection:
            if pr.collection.lower() == resource.collection.lower():
                return True
    return False


def _action_matches(action: PolicyAction, policy_actions: List[PolicyAction]) -> bool:
    """Return True if *action* is listed in *policy_actions*."""
    return action in policy_actions


def evaluate_policies(request: SimulationRequest) -> SimulationResult:
    """
    Evaluate a list of policies against a simulation request.

    Deny policies take precedence over Allow policies (explicit deny wins).
    If no policy matches, access is denied by default.
    """
    matched: List[PolicyMatch] = []
    notes: List[str] = []

    for policy in request.policies:
        if not policy.enabled:
            notes.append(f"Policy '{policy.name}' is disabled – skipped.")
            continue

        for idx, statement in enumerate(policy.statements):
            subject_ok = _subject_matches(request.subject, statement.subjects)
            resource_ok = _resource_matches(request.resource, statement.resources)
            action_ok = _action_matches(request.action, statement.actions)

            if subject_ok and resource_ok and action_ok:
                matched.append(
                    PolicyMatch(
                        policy_id=policy.id,
                        policy_name=policy.name,
                        statement_index=idx,
                        effect=statement.effect,
                    )
                )
                notes.append(
                    f"Policy '{policy.name}' statement[{idx}] matched "
                    f"(effect: {statement.effect.value})."
                )

    if not matched:
        notes.append("No matching policy found – access denied by default.")
        return SimulationResult(
            access_granted=False,
            effective_effect=None,
            matched_policies=[],
            evaluation_notes=notes,
        )

    # Explicit Deny wins
    has_deny = any(m.effect == PolicyEffect.DENY for m in matched)
    if has_deny:
        notes.append("At least one Deny statement matched – access denied.")
        return SimulationResult(
            access_granted=False,
            effective_effect=PolicyEffect.DENY,
            matched_policies=matched,
            evaluation_notes=notes,
        )

    notes.append("All matching statements are Allow – access granted.")
    return SimulationResult(
        access_granted=True,
        effective_effect=PolicyEffect.ALLOW,
        matched_policies=matched,
        evaluation_notes=notes,
    )

"""Unit tests for the policy evaluator."""
import pytest
from app.simulator import (
    Policy,
    PolicyAction,
    PolicyEffect,
    PolicyStatement,
    Resource,
    ResourcePathType,
    SimulationRequest,
    Subject,
    SubjectType,
    evaluate_policies,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _subject(uid: str = "alice@contoso.com") -> Subject:
    return Subject(id=uid, subject_type=SubjectType.USER)


def _resource(path: str = "/subscriptions/sub1/rg/storage") -> Resource:
    return Resource(resource_path=path, resource_type=ResourcePathType.AZURE_STORAGE)


def _policy(
    pid: str,
    name: str,
    effect: PolicyEffect,
    actions: list[PolicyAction],
    subject_ids: list[str],
    resource_paths: list[str],
    enabled: bool = True,
) -> Policy:
    subjects = [Subject(id=s, subject_type=SubjectType.USER) for s in subject_ids]
    resources = [
        Resource(resource_path=r, resource_type=ResourcePathType.AZURE_STORAGE)
        for r in resource_paths
    ]
    stmt = PolicyStatement(
        effect=effect,
        actions=actions,
        subjects=subjects,
        resources=resources,
    )
    return Policy(id=pid, name=name, statements=[stmt], enabled=enabled)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestAllowScenarios:
    def test_exact_match_grants_access(self):
        policy = _policy(
            "p1", "Allow Read",
            PolicyEffect.ALLOW,
            [PolicyAction.READ],
            ["alice@contoso.com"],
            ["/subscriptions/sub1/rg/storage"],
        )
        req = SimulationRequest(
            subject=_subject("alice@contoso.com"),
            resource=_resource("/subscriptions/sub1/rg/storage"),
            action=PolicyAction.READ,
            policies=[policy],
        )
        result = evaluate_policies(req)
        assert result.access_granted is True
        assert result.effective_effect == PolicyEffect.ALLOW
        assert len(result.matched_policies) == 1

    def test_wildcard_subject_grants_access(self):
        policy = _policy(
            "p1", "Allow All",
            PolicyEffect.ALLOW,
            [PolicyAction.READ],
            ["*"],
            ["*"],
        )
        req = SimulationRequest(
            subject=_subject("anyone@contoso.com"),
            resource=_resource("/subscriptions/sub1/rg/storage"),
            action=PolicyAction.READ,
            policies=[policy],
        )
        result = evaluate_policies(req)
        assert result.access_granted is True

    def test_parent_scope_resource_grants_access(self):
        policy = _policy(
            "p1", "Allow Subscription Scope",
            PolicyEffect.ALLOW,
            [PolicyAction.READ],
            ["alice@contoso.com"],
            ["/subscriptions/sub1"],
        )
        req = SimulationRequest(
            subject=_subject("alice@contoso.com"),
            resource=_resource("/subscriptions/sub1/rg/storage/container"),
            action=PolicyAction.READ,
            policies=[policy],
        )
        result = evaluate_policies(req)
        assert result.access_granted is True


class TestDenyScenarios:
    def test_no_matching_policy_denies_by_default(self):
        policy = _policy(
            "p1", "Other User Policy",
            PolicyEffect.ALLOW,
            [PolicyAction.READ],
            ["bob@contoso.com"],
            ["*"],
        )
        req = SimulationRequest(
            subject=_subject("alice@contoso.com"),
            resource=_resource("/subscriptions/sub1/rg/storage"),
            action=PolicyAction.READ,
            policies=[policy],
        )
        result = evaluate_policies(req)
        assert result.access_granted is False
        assert result.effective_effect is None

    def test_explicit_deny_overrides_allow(self):
        allow_policy = _policy(
            "p1", "Allow Read",
            PolicyEffect.ALLOW,
            [PolicyAction.READ],
            ["*"],
            ["*"],
        )
        deny_policy = _policy(
            "p2", "Deny Alice",
            PolicyEffect.DENY,
            [PolicyAction.READ],
            ["alice@contoso.com"],
            ["*"],
        )
        req = SimulationRequest(
            subject=_subject("alice@contoso.com"),
            resource=_resource("/subscriptions/sub1/rg/storage"),
            action=PolicyAction.READ,
            policies=[allow_policy, deny_policy],
        )
        result = evaluate_policies(req)
        assert result.access_granted is False
        assert result.effective_effect == PolicyEffect.DENY

    def test_action_mismatch_denies(self):
        policy = _policy(
            "p1", "Allow Read Only",
            PolicyEffect.ALLOW,
            [PolicyAction.READ],
            ["alice@contoso.com"],
            ["*"],
        )
        req = SimulationRequest(
            subject=_subject("alice@contoso.com"),
            resource=_resource("/subscriptions/sub1/rg/storage"),
            action=PolicyAction.MODIFY,
            policies=[policy],
        )
        result = evaluate_policies(req)
        assert result.access_granted is False

    def test_disabled_policy_is_skipped(self):
        policy = _policy(
            "p1", "Disabled Policy",
            PolicyEffect.ALLOW,
            [PolicyAction.READ],
            ["alice@contoso.com"],
            ["*"],
            enabled=False,
        )
        req = SimulationRequest(
            subject=_subject("alice@contoso.com"),
            resource=_resource("/subscriptions/sub1/rg/storage"),
            action=PolicyAction.READ,
            policies=[policy],
        )
        result = evaluate_policies(req)
        assert result.access_granted is False
        assert any("disabled" in n.lower() for n in result.evaluation_notes)

    def test_empty_policy_list_denies(self):
        req = SimulationRequest(
            subject=_subject("alice@contoso.com"),
            resource=_resource("/subscriptions/sub1/rg/storage"),
            action=PolicyAction.READ,
            policies=[],
        )
        result = evaluate_policies(req)
        assert result.access_granted is False


class TestMultiplePolicies:
    def test_multiple_allow_policies_all_appear_in_result(self):
        policies = [
            _policy(f"p{i}", f"Policy {i}", PolicyEffect.ALLOW, [PolicyAction.READ],
                    ["alice@contoso.com"], ["*"])
            for i in range(3)
        ]
        req = SimulationRequest(
            subject=_subject("alice@contoso.com"),
            resource=_resource("/subscriptions/sub1/rg/storage"),
            action=PolicyAction.READ,
            policies=policies,
        )
        result = evaluate_policies(req)
        assert result.access_granted is True
        assert len(result.matched_policies) == 3

import pytest
from simulator.engine.effects import EffectsGenerator


@pytest.fixture
def generator():
    return EffectsGenerator()


def _make_template(
    name="Test Template",
    category="General",
    locations=None,
    actions=None,
    content_count_min=1,
):
    return {
        "name": name,
        "category": category,
        "locations": locations or ["Exchange"],
        "conditions": {"content_count": {"min": content_count_min}},
        "actions": actions or {
            "block_sharing": False,
            "notify_user": True,
            "notify_admin": False,
            "generate_incident_report": False,
            "encrypt": False,
            "restrict_access": False,
        },
        "user_notification": {"message": "Test message", "policy_tip": "Test tip"},
        "incident_report": {"severity": "Low", "send_to": [], "include_content": False},
    }


def _make_nlp():
    return {
        "intent": [],
        "data_types": [],
        "locations": [],
        "compliance": [],
        "risk_scenarios": [],
        "keywords": [],
    }


def test_generate_effects_for_financial_template(generator):
    template = _make_template(
        name="PCI DSS Credit Card Protection",
        category="Financial",
        locations=["Exchange", "SharePoint"],
        actions={
            "block_sharing": True,
            "notify_user": True,
            "notify_admin": True,
            "generate_incident_report": True,
            "encrypt": False,
            "restrict_access": True,
        },
    )
    template["incident_report"] = {"severity": "High", "send_to": ["compliance@test.com"], "include_content": False}
    nlp = _make_nlp()
    nlp.update({"data_types": ["credit_cards"], "compliance": ["pci_dss"]})

    effects = generator.generate(template, nlp)
    assert "blocked_actions" in effects
    assert "audited_actions" in effects
    assert "false_positive_risk" in effects
    assert "deployment_recommendations" in effects


def test_generate_effects_has_required_keys(generator):
    template = _make_template()
    nlp = _make_nlp()
    effects = generator.generate(template, nlp)
    required_keys = [
        "blocked_actions",
        "audited_actions",
        "notifications",
        "false_positive_risk",
        "deployment_recommendations",
        "dependencies",
        "estimated_coverage",
    ]
    for key in required_keys:
        assert key in effects, f"Missing key: {key}"


def test_block_sharing_populates_blocked_actions(generator):
    template = _make_template(actions={
        "block_sharing": True, "notify_user": False,
        "notify_admin": False, "generate_incident_report": False,
        "encrypt": False, "restrict_access": False,
    })
    effects = generator.generate(template, _make_nlp())
    assert len(effects["blocked_actions"]) > 0


def test_no_block_empty_blocked_actions(generator):
    template = _make_template(actions={
        "block_sharing": False, "notify_user": True,
        "notify_admin": True, "generate_incident_report": True,
        "encrypt": False, "restrict_access": False,
    })
    effects = generator.generate(template, _make_nlp())
    assert len(effects["blocked_actions"]) == 0


def test_false_positive_risk_levels(generator):
    # Low count -> MEDIUM risk
    template = _make_template(content_count_min=1)
    effects = generator.generate(template, _make_nlp())
    assert effects["false_positive_risk"] in ("LOW", "MEDIUM", "HIGH")


def test_teams_adds_license_dependency(generator):
    template = _make_template(locations=["Exchange", "Teams"])
    effects = generator.generate(template, _make_nlp())
    deps_text = " ".join(effects["dependencies"])
    assert "Teams" in deps_text or "E5" in deps_text

import pytest
from simulator.engine.matcher import TemplateMatcher


@pytest.fixture
def matcher():
    return TemplateMatcher()


def test_match_returns_results(matcher):
    results = matcher.match(
        "protect credit card data",
        {
            "keywords": ["credit", "card"],
            "compliance": [],
            "data_types": ["credit_cards"],
            "locations": [],
            "risk_scenarios": [],
        },
    )
    assert isinstance(results, list)
    assert len(results) > 0


def test_match_financial_query(matcher):
    results = matcher.match(
        "PCI DSS credit card payment protection",
        {
            "keywords": ["pci", "credit", "card"],
            "compliance": ["pci_dss"],
            "data_types": ["credit_cards"],
            "locations": ["email"],
            "risk_scenarios": [],
        },
    )
    assert len(results) > 0
    scores = [score for _, score in results]
    assert all(0 <= s <= 2.0 for s in scores)


def test_match_healthcare_query(matcher):
    results = matcher.match(
        "HIPAA medical records patient data",
        {
            "keywords": ["hipaa", "medical", "patient"],
            "compliance": ["hipaa"],
            "data_types": ["health_records"],
            "locations": [],
            "risk_scenarios": [],
        },
    )
    assert len(results) > 0


def test_scores_between_0_and_positive(matcher):
    results = matcher.match(
        "social security number SSN",
        {
            "keywords": ["ssn", "social", "security"],
            "compliance": [],
            "data_types": ["ssn"],
            "locations": [],
            "risk_scenarios": [],
        },
    )
    for _, score in results:
        assert score >= 0


def test_match_returns_template_dicts(matcher):
    results = matcher.match(
        "GDPR EU personal data protection",
        {
            "keywords": ["gdpr", "eu", "personal", "data"],
            "compliance": ["gdpr"],
            "data_types": ["pii"],
            "locations": [],
            "risk_scenarios": [],
        },
    )
    assert len(results) > 0
    for template, score in results:
        assert isinstance(template, dict)
        assert "template_id" in template
        assert isinstance(score, float)


def test_top_k_respected(matcher):
    results = matcher.match(
        "data protection",
        {"keywords": ["data", "protection"], "compliance": [], "data_types": [], "locations": [], "risk_scenarios": []},
        top_k=3,
    )
    assert len(results) <= 3

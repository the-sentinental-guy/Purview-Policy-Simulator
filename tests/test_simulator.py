import pytest
from app.engine.nlp_processor import NLPProcessor
from app.engine.matcher import PolicyMatcher
from app.engine.simulator import PolicySimulator
from app.models.simulation import SimulationRequest


def test_nlp_extract_intent_protect():
    nlp = NLPProcessor()
    assert nlp.extract_intent("prevent sharing credit cards") in ["prevent", "protect"]


def test_nlp_extract_intent_retain():
    nlp = NLPProcessor()
    assert nlp.extract_intent("retain financial records for 7 years") == "retain"


def test_nlp_extract_entities_frameworks():
    nlp = NLPProcessor()
    entities = nlp.extract_entities("PCI-DSS compliance for credit card data")
    assert any("pci" in f.lower() for f in entities.get("frameworks", []))


def test_nlp_extract_entities_locations():
    nlp = NLPProcessor()
    entities = nlp.extract_entities("protect data in SharePoint and Teams")
    locations = [l.lower() for l in entities.get("locations", [])]
    assert any("sharepoint" in l for l in locations) or any("teams" in l for l in locations)


def test_matcher_finds_templates():
    matcher = PolicyMatcher()
    from app.engine.nlp_processor import NLPProcessor
    nlp = NLPProcessor()
    # Use a query with strong keyword overlap to exceed the 70% threshold
    matches = matcher.find_matches(
        "PCI DSS payment card industry data security standard credit card CVV", nlp, max_results=3
    )
    assert len(matches) >= 1


def test_matcher_pci_template():
    matcher = PolicyMatcher()
    nlp = NLPProcessor()
    matches = matcher.find_matches(
        "PCI DSS payment card industry data security standard credit card CVV", nlp, max_results=3
    )
    assert len(matches) >= 1
    # Top match should be PCI-related
    top_match = matches[0]
    assert top_match.confidence.score > 0
    assert "PCI" in top_match.template.name or "Credit Card" in top_match.template.name


def test_matcher_low_confidence_excluded():
    """Templates scoring below 70% should NOT be returned by find_matches."""
    matcher = PolicyMatcher()
    nlp = NLPProcessor()
    # Generic unrelated query that won't score ≥ 70% for any template
    matches = matcher.find_matches("general business process improvement", nlp, max_results=3)
    for match in matches:
        assert match.similarity_score >= 0.70, (
            f"Template '{match.template.name}' scored {match.similarity_score:.4f}, "
            "which is below the 70% minimum threshold"
        )


@pytest.mark.asyncio
async def test_simulator_basic():
    sim = PolicySimulator()
    request = SimulationRequest(
        query="PCI DSS payment card industry data security standard credit card CVV"
    )
    response = await sim.simulate(request)
    assert response.query == request.query
    assert response.intent in ["protect", "prevent", "detect", "monitor", "retain", "classify", "investigate"]
    assert len(response.template_matches) >= 1


@pytest.mark.asyncio
async def test_simulator_hipaa():
    sim = PolicySimulator()
    request = SimulationRequest(
        query="HIPAA protected health information PHI patient records SharePoint"
    )
    response = await sim.simulate(request)
    assert response.intent is not None
    assert len(response.template_matches) >= 1


@pytest.mark.asyncio
async def test_simulator_gdpr():
    sim = PolicySimulator()
    request = SimulationRequest(query="GDPR EU general data protection regulation personal data")
    response = await sim.simulate(request)
    assert len(response.template_matches) >= 1


@pytest.mark.asyncio
async def test_simulator_custom_config_disclaimer():
    """Custom configuration title should have the warning prefix."""
    sim = PolicySimulator()
    # Use a vague query unlikely to match any template at 70%
    request = SimulationRequest(query="general business compliance policy")
    response = await sim.simulate(request)
    if response.custom_configuration:
        assert response.custom_configuration.title.startswith("⚠️ Suggested Starting Point")
        # First step should be the disclaimer note
        assert response.custom_configuration.steps[0].startswith("Note:")


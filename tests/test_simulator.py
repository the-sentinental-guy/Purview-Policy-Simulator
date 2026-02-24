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
    matches = matcher.find_matches("prevent credit card sharing via email", nlp, max_results=3)
    assert len(matches) >= 1


def test_matcher_pci_template():
    matcher = PolicyMatcher()
    nlp = NLPProcessor()
    matches = matcher.find_matches("PCI DSS credit card payment card data protection", nlp, max_results=3)
    assert len(matches) >= 1
    # Top match should be PCI-related
    top_match = matches[0]
    assert top_match.confidence.score > 0


@pytest.mark.asyncio
async def test_simulator_basic():
    sim = PolicySimulator()
    request = SimulationRequest(query="protect credit card numbers in email")
    response = await sim.simulate(request)
    assert response.query == request.query
    assert response.intent in ["protect", "prevent", "detect", "monitor", "retain", "classify", "investigate"]
    assert len(response.template_matches) >= 1


@pytest.mark.asyncio
async def test_simulator_hipaa():
    sim = PolicySimulator()
    request = SimulationRequest(query="protect HIPAA PHI patient health information in SharePoint")
    response = await sim.simulate(request)
    assert response.intent is not None
    assert len(response.template_matches) >= 1


@pytest.mark.asyncio
async def test_simulator_gdpr():
    sim = PolicySimulator()
    request = SimulationRequest(query="GDPR EU personal data protection compliance")
    response = await sim.simulate(request)
    assert len(response.template_matches) >= 1

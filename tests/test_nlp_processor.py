import pytest
from simulator.engine.nlp_processor import NLPProcessor


@pytest.fixture
def nlp():
    return NLPProcessor()


def test_process_financial_query(nlp):
    result = nlp.process("Prevent credit card numbers from being shared via email")
    assert "credit_cards" in result["data_types"]
    assert "protect" in result["intent"]


def test_extract_compliance_frameworks(nlp):
    result = nlp.process("HIPAA compliance for medical records GDPR")
    assert "hipaa" in result["compliance"]
    assert "gdpr" in result["compliance"]


def test_extract_locations(nlp):
    result = nlp.process("Protect data in SharePoint and Teams")
    assert "sharepoint" in result["locations"]
    assert "teams" in result["locations"]


def test_keywords_extracted(nlp):
    result = nlp.process("Protect SSN social security numbers")
    assert len(result["keywords"]) > 0


def test_default_intent(nlp):
    result = nlp.process("credit card data")
    assert len(result["intent"]) > 0


def test_detect_intent(nlp):
    result = nlp.process("detect SSN in Teams messages")
    assert "detect" in result["intent"]


def test_classify_intent(nlp):
    result = nlp.process("classify documents with sensitivity labels")
    assert "classify" in result["intent"]


def test_risk_scenario_departing(nlp):
    result = nlp.process("protect source code from departing employees resigning")
    assert "departing_employee" in result["risk_scenarios"]


def test_pci_dss_compliance(nlp):
    result = nlp.process("PCI DSS payment card industry compliance")
    assert "pci_dss" in result["compliance"]


def test_returns_all_keys(nlp):
    result = nlp.process("test query")
    expected_keys = {"intent", "data_types", "locations", "compliance", "risk_scenarios", "keywords"}
    assert expected_keys.issubset(result.keys())

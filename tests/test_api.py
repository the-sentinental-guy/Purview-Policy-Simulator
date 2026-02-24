import pytest
from fastapi.testclient import TestClient
from simulator.app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_templates_endpoint():
    response = client.get("/templates")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert "total" in data
    assert data["total"] >= 50


def test_templates_has_categories():
    response = client.get("/templates")
    data = response.json()
    categories = data["categories"]
    assert isinstance(categories, dict)
    assert len(categories) > 0


def test_simulate_endpoint():
    response = client.post(
        "/simulate",
        json={"query": "Protect credit card numbers from email", "mcp_enabled": False},
    )
    assert response.status_code == 200
    data = response.json()
    assert "matches" in data
    assert "nlp_analysis" in data
    assert "summary" in data
    assert isinstance(data["matches"], list)


def test_simulate_returns_matches():
    response = client.post(
        "/simulate",
        json={"query": "HIPAA medical records PHI SharePoint protection", "mcp_enabled": False},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["matches"]) > 0


def test_simulate_match_structure():
    response = client.post(
        "/simulate",
        json={"query": "PCI DSS credit card", "mcp_enabled": False},
    )
    data = response.json()
    if data["matches"]:
        match = data["matches"][0]
        assert "template" in match
        assert "confidence_score" in match
        assert "confidence_level" in match
        assert "effects" in match
        assert "explanation" in match


def test_simulate_empty_query():
    response = client.post(
        "/simulate",
        json={"query": "   ", "mcp_enabled": False},
    )
    # Should still return 200 with empty/no match results
    assert response.status_code == 200


def test_simulate_timestamp_present():
    response = client.post(
        "/simulate",
        json={"query": "data protection", "mcp_enabled": False},
    )
    data = response.json()
    assert "timestamp" in data
    assert data["timestamp"] != ""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from app.main import app

client = TestClient(app)


def test_health_check():
    with patch("app.main.mcp_client.is_available", new_callable=AsyncMock, return_value=False):
        response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "templates_loaded" in data
    assert data["templates_loaded"] >= 40


def test_list_templates():
    response = client.get("/templates")
    assert response.status_code == 200
    templates = response.json()
    assert len(templates) >= 40


def test_list_templates_by_category():
    response = client.get("/templates?category=Financial")
    assert response.status_code == 200
    templates = response.json()
    assert all(t["category"].lower() == "financial" for t in templates)


def test_list_categories():
    response = client.get("/templates/categories")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert len(data["categories"]) >= 4


def test_simulate_basic():
    response = client.post("/simulate", json={
        "query": "PCI DSS payment card industry data security standard credit card CVV",
        "use_mcp": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "PCI DSS payment card industry data security standard credit card CVV"
    assert "template_matches" in data
    assert len(data["template_matches"]) >= 1


def test_simulate_hipaa():
    response = client.post("/simulate", json={
        "query": "HIPAA protected health information PHI patient records SharePoint",
        "use_mcp": False
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data["template_matches"]) >= 1


def test_simulate_missing_query():
    response = client.post("/simulate", json={"use_mcp": False})
    assert response.status_code == 422


def test_mcp_status():
    with patch("app.main.mcp_client.is_available", new_callable=AsyncMock, return_value=False):
        response = client.get("/mcp/status")
    assert response.status_code == 200
    data = response.json()
    assert "available" in data

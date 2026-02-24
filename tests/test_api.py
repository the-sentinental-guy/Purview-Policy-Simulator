"""Integration tests for the FastAPI routes."""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


SIMULATE_PAYLOAD = {
    "subject": {"id": "alice@contoso.com", "subject_type": "User"},
    "resource": {
        "resource_path": "/subscriptions/sub1/rg/storage",
        "resource_type": "AzureStorage",
    },
    "action": "Microsoft.Purview/accounts/data/read",
    "policies": [
        {
            "id": "p1",
            "name": "Allow Read",
            "enabled": True,
            "statements": [
                {
                    "effect": "Allow",
                    "actions": ["Microsoft.Purview/accounts/data/read"],
                    "subjects": [{"id": "alice@contoso.com", "subject_type": "User"}],
                    "resources": [
                        {
                            "resource_path": "/subscriptions/sub1/rg/storage",
                            "resource_type": "AzureStorage",
                        }
                    ],
                }
            ],
        }
    ],
}


class TestHealthEndpoint:
    def test_health_returns_ok(self):
        resp = client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "version" in data


class TestSimulateEndpoint:
    def test_simulate_allow(self):
        resp = client.post("/api/simulate", json=SIMULATE_PAYLOAD)
        assert resp.status_code == 200
        data = resp.json()
        assert data["access_granted"] is True
        assert data["effective_effect"] == "Allow"
        assert len(data["matched_policies"]) == 1

    def test_simulate_deny_no_match(self):
        payload = {**SIMULATE_PAYLOAD}
        payload["subject"] = {"id": "stranger@contoso.com", "subject_type": "User"}
        resp = client.post("/api/simulate", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["access_granted"] is False

    def test_simulate_invalid_json_returns_422(self):
        resp = client.post("/api/simulate", json={"bad": "payload"})
        assert resp.status_code == 422

    def test_simulate_explicit_deny(self):
        payload = {
            **SIMULATE_PAYLOAD,
            "policies": [
                {
                    "id": "p-deny",
                    "name": "Deny All",
                    "enabled": True,
                    "statements": [
                        {
                            "effect": "Deny",
                            "actions": ["Microsoft.Purview/accounts/data/read"],
                            "subjects": [{"id": "*", "subject_type": "User"}],
                            "resources": [
                                {
                                    "resource_path": "*",
                                    "resource_type": "AzureStorage",
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        resp = client.post("/api/simulate", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["access_granted"] is False
        assert data["effective_effect"] == "Deny"


class TestFrontend:
    def test_index_returns_html(self):
        resp = client.get("/")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]
        assert "Purview Policy Simulator" in resp.text

    def test_openapi_schema_accessible(self):
        resp = client.get("/api/openapi.json")
        assert resp.status_code == 200

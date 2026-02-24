"""Tests for the Purview Policy Simulator engine."""

import pytest

from purview_simulator.engine import (
    TEMPLATE_MATCH_THRESHOLD,
    ParsedRequirement,
    PolicyRecommendation,
    SimulationResult,
    parse_requirement,
    run_simulation,
)
from purview_simulator.knowledge_base import (
    POLICY_TEMPLATES,
    SENSITIVE_INFO_TYPES,
)


# ── parse_requirement tests ──────────────────────────────────────────────

class TestParseRequirement:
    def test_detects_credit_card_keyword(self):
        parsed = parse_requirement("Block credit card numbers in email")
        assert "credit_card" in parsed.detected_info_types

    def test_detects_multiple_info_types(self):
        parsed = parse_requirement("Protect SSN and passport data")
        assert "ssn" in parsed.detected_info_types
        assert "passport" in parsed.detected_info_types

    def test_detects_location_exchange(self):
        parsed = parse_requirement("Prevent sharing sensitive data via email")
        assert "exchange" in parsed.detected_locations

    def test_detects_location_teams(self):
        parsed = parse_requirement("Block PII in Teams chat messages")
        assert "teams" in parsed.detected_locations

    def test_detects_action_block(self):
        parsed = parse_requirement("Block external sharing of financial data")
        assert "block" in parsed.detected_actions

    def test_detects_action_encrypt(self):
        parsed = parse_requirement("Encrypt health records automatically")
        assert "encrypt" in parsed.detected_actions

    def test_detects_template_hint_hipaa(self):
        parsed = parse_requirement("I need a HIPAA compliant policy for patient data")
        assert "hipaa_dlp" in parsed.detected_template_hints

    def test_empty_input_returns_empty_parsed(self):
        parsed = parse_requirement("")
        assert parsed.detected_info_types == []
        assert parsed.detected_locations == []
        assert parsed.detected_actions == []
        assert parsed.detected_template_hints == []

    def test_case_insensitive(self):
        parsed = parse_requirement("CREDIT CARD numbers in SHAREPOINT")
        assert "credit_card" in parsed.detected_info_types
        assert "sharepoint" in parsed.detected_locations


# ── run_simulation tests ─────────────────────────────────────────────────

class TestRunSimulation:
    def test_financial_scenario_matches_template(self):
        result = run_simulation(
            "Prevent credit card numbers from being shared externally via email"
        )
        assert result.achievable_with_template is True
        assert len(result.recommendations) > 0
        top = result.recommendations[0]
        assert top.policy_type == "template"
        assert top.confidence >= TEMPLATE_MATCH_THRESHOLD

    def test_hipaa_scenario(self):
        result = run_simulation(
            "We need to comply with HIPAA and protect patient health records"
        )
        assert result.achievable_with_template is True
        template_names = [r.policy_name for r in result.recommendations]
        assert any("HIPAA" in n for n in template_names)

    def test_gdpr_scenario(self):
        result = run_simulation(
            "We must protect EU personal data under GDPR regulations"
        )
        assert result.achievable_with_template is True
        template_names = [r.policy_name for r in result.recommendations]
        assert any("GDPR" in n for n in template_names)

    def test_custom_scenario_returns_custom_recommendation(self):
        result = run_simulation(
            "Block source code from being copied to USB on developer laptops and "
            "also encrypt it when sent via email"
        )
        types = [r.policy_type for r in result.recommendations]
        # Should include at least some recommendations
        assert len(result.recommendations) > 0

    def test_recommendations_have_expected_effects(self):
        result = run_simulation("Protect credit card data in SharePoint")
        for rec in result.recommendations:
            assert len(rec.expected_effects) > 0

    def test_recommendations_have_confidence(self):
        result = run_simulation("Block SSN from being shared in Teams")
        for rec in result.recommendations:
            assert 0.0 <= rec.confidence <= 1.0

    def test_recommendations_have_configurations(self):
        result = run_simulation("Encrypt financial data in OneDrive")
        for rec in result.recommendations:
            assert len(rec.configurations) > 0

    def test_vague_requirement_produces_results(self):
        result = run_simulation("I want to protect sensitive data")
        # Even vague requests should return something useful
        assert len(result.recommendations) > 0

    def test_credential_protection_scenario(self):
        result = run_simulation(
            "Prevent API keys and secrets from being shared in Teams or email"
        )
        assert len(result.recommendations) > 0
        # Should detect credential-related info type
        assert "azure_secret" in result.parsed.detected_info_types

    def test_endpoint_dlp_scenario(self):
        result = run_simulation(
            "Block users from copying credit card data to USB drives on their laptops"
        )
        assert "devices" in result.parsed.detected_locations
        assert len(result.recommendations) > 0


# ── SimulationResult structure tests ─────────────────────────────────────

class TestSimulationResultStructure:
    def test_result_contains_original_requirement(self):
        text = "Test requirement"
        result = run_simulation(text)
        assert result.original_requirement == text

    def test_result_parsed_is_populated(self):
        result = run_simulation("Protect SSN in email")
        assert isinstance(result.parsed, ParsedRequirement)
        assert result.parsed.raw_text == "Protect SSN in email"

    def test_recommendation_fields(self):
        result = run_simulation("Block credit card sharing in SharePoint")
        rec = result.recommendations[0]
        assert isinstance(rec, PolicyRecommendation)
        assert rec.policy_name
        assert rec.policy_type in ("template", "custom")
        assert rec.description
        assert isinstance(rec.confidence, float)

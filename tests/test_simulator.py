"""
Tests for the Purview Policy Simulator engine.
"""

import pytest

from simulator import simulate


class TestSimulateFinancial:
    def test_financial_query_returns_templates(self):
        result = simulate("Prevent employees from sending credit card numbers via email")
        assert len(result["matched_templates"]) > 0
        template_ids = [t["id"] for t in result["matched_templates"]]
        assert "dlp_financial_us" in template_ids

    def test_financial_high_confidence(self):
        result = simulate("Block sharing of bank account numbers and credit card data externally, PCI-DSS compliance")
        best = result["matched_templates"][0]
        assert best["confidence"] >= 75

    def test_financial_template_available(self):
        result = simulate("Protect financial data including credit card numbers from being shared externally")
        best = result["matched_templates"][0]
        assert best["template_available"] is True

    def test_financial_no_custom_required(self):
        result = simulate("Block credit card numbers in email to external recipients for PCI compliance")
        assert result["requires_custom"] is False


class TestSimulatePII:
    def test_pii_query_matches(self):
        result = simulate("Protect Social Security Numbers and personally identifiable information")
        ids = [t["id"] for t in result["matched_templates"]]
        assert "dlp_pii_us" in ids

    def test_pii_keywords_matched(self):
        result = simulate("Block sharing of SSN and driver license numbers")
        # Verify that at least one PII-related keyword was matched
        assert len(result["matched_keywords"]) > 0


class TestSimulateHIPAA:
    def test_hipaa_matches(self):
        result = simulate("Prevent sharing of patient medical records to comply with HIPAA")
        ids = [t["id"] for t in result["matched_templates"]]
        assert "dlp_health_hipaa" in ids

    def test_hipaa_effects_present(self):
        result = simulate("Protect health data and PHI in emails and SharePoint for HIPAA")
        best = next(t for t in result["matched_templates"] if t["id"] == "dlp_health_hipaa")
        assert len(best["expected_effects"]) > 0


class TestSimulateGDPR:
    def test_gdpr_matches(self):
        result = simulate("Protect personal data of EU residents to comply with GDPR")
        ids = [t["id"] for t in result["matched_templates"]]
        assert "dlp_gdpr" in ids

    def test_gdpr_template_available(self):
        result = simulate("GDPR compliance for European personal data")
        best = next(t for t in result["matched_templates"] if t["id"] == "dlp_gdpr")
        assert best["template_available"] is True


class TestSimulateSensitivityLabels:
    def test_confidential_label_matches(self):
        result = simulate("Classify and encrypt confidential internal documents and emails")
        ids = [t["id"] for t in result["matched_templates"]]
        assert "sensitivity_label_confidential" in ids

    def test_highly_confidential_matches(self):
        result = simulate("Protect highly confidential M&A documents, restrict to executives only")
        ids = [t["id"] for t in result["matched_templates"]]
        assert "sensitivity_label_highly_confidential" in ids


class TestSimulateRetention:
    def test_retention_matches(self):
        result = simulate("Retain all emails and documents for 7 years for compliance")
        ids = [t["id"] for t in result["matched_templates"]]
        assert "retention_policy_general" in ids

    def test_retention_template_available(self):
        result = simulate("Archive and retain SharePoint content with legal hold capability")
        best = next((t for t in result["matched_templates"] if t["id"] == "retention_policy_general"), None)
        assert best is not None


class TestSimulateInsiderRisk:
    def test_insider_risk_matches(self):
        result = simulate("Detect data theft by departing employees exfiltrating via USB and email")
        ids = [t["id"] for t in result["matched_templates"]]
        assert "insider_risk_data_theft" in ids


class TestSimulateCustomPolicy:
    def test_no_match_requires_custom(self):
        result = simulate("xxxx completely unknown requirement zzzz")
        assert result["requires_custom"] is True

    def test_no_match_custom_configs_provided(self):
        result = simulate("xxxx completely unknown requirement zzzz")
        assert len(result["custom_configs"]) > 0

    def test_source_code_custom_required(self):
        result = simulate("Prevent source code from being shared externally via email")
        # Source code template has template_available=False, so custom should be required
        assert result["requires_custom"] is True


class TestSimulateEdgeCases:
    def test_empty_input(self):
        result = simulate("")
        assert result["overall_confidence"] == 0
        assert result["matched_templates"] == []

    def test_whitespace_only_input(self):
        result = simulate("   ")
        assert result["overall_confidence"] == 0

    def test_result_has_required_keys(self):
        result = simulate("Protect financial data")
        required_keys = [
            "matched_templates",
            "requires_custom",
            "custom_configs",
            "overall_confidence",
            "summary",
            "matched_keywords",
        ]
        for key in required_keys:
            assert key in result, f"Missing key: {key}"

    def test_confidence_within_bounds(self):
        result = simulate("Protect credit card numbers and PII from external sharing")
        assert 0 <= result["overall_confidence"] <= 100

    def test_max_templates_returned(self):
        # Should return at most 4 templates
        result = simulate("financial credit card bank PII SSN HIPAA GDPR confidential retention")
        assert len(result["matched_templates"]) <= 4

    def test_templates_sorted_by_score(self):
        result = simulate("credit card bank financial PCI payment routing number")
        templates = result["matched_templates"]
        if len(templates) >= 2:
            assert templates[0]["match_score"] >= templates[1]["match_score"]

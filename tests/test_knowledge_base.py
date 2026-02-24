"""Tests for the Purview Policy Simulator knowledge base."""

from purview_simulator.knowledge_base import (
    CUSTOM_POLICY_OPTIONS,
    POLICY_ACTIONS,
    POLICY_LOCATIONS,
    POLICY_TEMPLATES,
    SENSITIVE_INFO_TYPES,
    get_all_keywords,
)


class TestKnowledgeBaseIntegrity:
    def test_all_templates_reference_valid_info_types(self):
        for tmpl in POLICY_TEMPLATES:
            for sit_id in tmpl["sensitive_info_types"]:
                assert sit_id in SENSITIVE_INFO_TYPES, (
                    f"Template '{tmpl['name']}' references unknown info type '{sit_id}'"
                )

    def test_all_templates_reference_valid_locations(self):
        for tmpl in POLICY_TEMPLATES:
            for loc_id in tmpl["default_locations"]:
                assert loc_id in POLICY_LOCATIONS, (
                    f"Template '{tmpl['name']}' references unknown location '{loc_id}'"
                )

    def test_all_templates_reference_valid_actions(self):
        for tmpl in POLICY_TEMPLATES:
            for act_id in tmpl["default_actions"]:
                assert act_id in POLICY_ACTIONS, (
                    f"Template '{tmpl['name']}' references unknown action '{act_id}'"
                )

    def test_all_templates_have_expected_effects(self):
        for tmpl in POLICY_TEMPLATES:
            assert len(tmpl["expected_effects"]) > 0, (
                f"Template '{tmpl['name']}' has no expected effects"
            )

    def test_all_templates_have_keywords(self):
        for tmpl in POLICY_TEMPLATES:
            assert len(tmpl["keywords"]) > 0, (
                f"Template '{tmpl['name']}' has no keywords"
            )

    def test_get_all_keywords_returns_nonempty_dict(self):
        kw_map = get_all_keywords()
        assert len(kw_map) > 0

    def test_custom_policy_options_has_conditions(self):
        assert "conditions" in CUSTOM_POLICY_OPTIONS
        assert len(CUSTOM_POLICY_OPTIONS["conditions"]) > 0

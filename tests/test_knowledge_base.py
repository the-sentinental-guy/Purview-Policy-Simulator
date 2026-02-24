import pytest
from app.knowledge_base.dlp_templates import get_dlp_templates
from app.knowledge_base.sensitivity_labels import get_sensitivity_labels, get_label_policies
from app.knowledge_base.retention_policies import get_retention_labels, get_retention_policies
from app.knowledge_base.insider_risk import get_insider_risk_templates
from app.knowledge_base.troubleshooting import get_troubleshooting_guide
from app.knowledge_base.architecture import get_architecture_reference


def test_dlp_templates_count():
    """At least 40 DLP templates."""
    templates = get_dlp_templates()
    assert len(templates) >= 40


def test_dlp_template_structure():
    """Each template has required fields."""
    for t in get_dlp_templates():
        assert t.id, f"Template missing id"
        assert t.name, f"Template missing name"
        assert t.category, f"Template missing category"
        assert t.description, f"Template missing description"
        assert len(t.keywords) >= 5, f"Template {t.id} needs at least 5 keywords"


def test_dlp_template_source_url():
    """Every template must have a non-empty source_url pointing to Microsoft Learn."""
    for t in get_dlp_templates():
        assert t.source_url, f"Template {t.id} is missing source_url"
        assert t.source_url.startswith("https://learn.microsoft.com/"), (
            f"Template {t.id} source_url should point to Microsoft Learn, got: {t.source_url}"
        )


def test_dlp_template_categories():
    """Templates cover all required categories."""
    templates = get_dlp_templates()
    categories = {t.category for t in templates}
    assert "Financial" in categories
    assert "Healthcare" in categories
    assert "Privacy" in categories


def test_sensitivity_labels():
    labels = get_sensitivity_labels()
    assert len(labels) >= 5
    names = [l["name"] for l in labels]
    assert any("Public" in n for n in names)
    assert any("Confidential" in n for n in names)


def test_retention_labels():
    labels = get_retention_labels()
    assert len(labels) >= 5


def test_insider_risk_templates():
    templates = get_insider_risk_templates()
    assert len(templates) >= 5


def test_troubleshooting_guide():
    guide = get_troubleshooting_guide()
    assert "dlp_issues" in guide
    assert "label_issues" in guide


def test_architecture_reference():
    arch = get_architecture_reference()
    assert "overview" in arch
    assert "deployment_checklist" in arch

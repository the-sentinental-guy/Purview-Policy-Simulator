import pytest
from simulator.engine.simulator import SimulationEngine


@pytest.fixture
def engine():
    return SimulationEngine()


@pytest.mark.asyncio
async def test_simulate_returns_result(engine):
    result = await engine.simulate(
        "Protect credit card numbers from being shared externally",
        mcp_enabled=False,
    )
    assert result.query != ""
    assert isinstance(result.matches, list)
    assert result.timestamp != ""


@pytest.mark.asyncio
async def test_simulate_with_financial_query(engine):
    result = await engine.simulate(
        "PCI DSS credit card protection email Exchange",
        mcp_enabled=False,
    )
    assert len(result.matches) > 0
    assert result.nlp_analysis is not None


@pytest.mark.asyncio
async def test_simulate_mcp_disabled(engine):
    result = await engine.simulate("HIPAA medical records SharePoint", mcp_enabled=False)
    assert result is not None
    assert isinstance(result.mcp_references, list)


@pytest.mark.asyncio
async def test_simulate_summary_not_empty(engine):
    result = await engine.simulate("SSN social security protection", mcp_enabled=False)
    assert result.summary != ""


@pytest.mark.asyncio
async def test_simulate_nlp_analysis_present(engine):
    result = await engine.simulate("GDPR EU personal data privacy", mcp_enabled=False)
    assert "intent" in result.nlp_analysis
    assert "compliance" in result.nlp_analysis
    assert "gdpr" in result.nlp_analysis["compliance"]


@pytest.mark.asyncio
async def test_simulate_match_has_effects(engine):
    result = await engine.simulate("Block credit card sharing via email", mcp_enabled=False)
    if result.matches:
        match = result.matches[0]
        assert "blocked_actions" in match.effects or "audited_actions" in match.effects

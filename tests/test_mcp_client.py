import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

from app.mcp_client import MCPClient
from app.models.simulation import MCPDocumentation


@pytest.fixture
def client():
    return MCPClient()


@pytest.mark.asyncio
async def test_discover_tools_success(client):
    """discover_tools returns list on success."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {"content-type": "application/json"}
    mock_response.json.return_value = {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "tools": [
                {"name": "microsoft_docs_search", "description": "Search docs"},
                {"name": "microsoft_docs_fetch", "description": "Fetch docs"},
            ]
        }
    }

    with patch("httpx.AsyncClient") as mock_class:
        mock_instance = AsyncMock()
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=False)
        mock_instance.post = AsyncMock(return_value=mock_response)
        mock_class.return_value = mock_instance

        tools = await client.discover_tools()
        assert len(tools) >= 1


@pytest.mark.asyncio
async def test_discover_tools_failure(client):
    """discover_tools returns empty list on failure."""
    with patch("httpx.AsyncClient") as mock_class:
        mock_instance = AsyncMock()
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=False)
        mock_instance.post = AsyncMock(side_effect=httpx.TimeoutException("timeout"))
        mock_class.return_value = mock_instance

        tools = await client.discover_tools()
        assert tools == []
        assert client._available == False


@pytest.mark.asyncio
async def test_search_docs_when_unavailable(client):
    """search_docs returns empty list when MCP is unavailable."""
    client._available = False
    result = await client.search_docs("test query")
    assert result == []


@pytest.mark.asyncio
async def test_search_docs_success(client):
    """search_docs returns MCPDocumentation list."""
    client._available = True

    tool_result = {
        "content": [
            {
                "type": "text",
                "text": json.dumps({
                    "results": [
                        {
                            "title": "Configure DLP policies",
                            "url": "https://learn.microsoft.com/en-us/purview/dlp-configure",
                            "description": "How to configure DLP policies in Microsoft Purview"
                        }
                    ]
                })
            }
        ]
    }

    with patch.object(client, "_call_tool", new_callable=AsyncMock) as mock_call:
        mock_call.return_value = tool_result
        results = await client.search_docs("DLP credit card")
        assert len(results) >= 1
        assert isinstance(results[0], MCPDocumentation)


@pytest.mark.asyncio
async def test_enrich_simulation_unavailable(client):
    """enrich_simulation returns empty dict when MCP is unavailable."""
    client._available = False
    result = await client.enrich_simulation("test", [])
    assert result.get("documentation_links", []) == []


@pytest.mark.asyncio
async def test_is_available_cached(client):
    """is_available uses cached value on second call."""
    client._available = True
    result = await client.is_available()
    assert result is True

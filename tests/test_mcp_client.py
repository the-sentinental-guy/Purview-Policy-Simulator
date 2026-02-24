import pytest
from simulator.mcp_client import MCPClient


def test_client_initializes():
    client = MCPClient()
    assert client.endpoint is not None
    assert client.available is False


def test_client_custom_endpoint():
    client = MCPClient(endpoint="http://custom-endpoint.example.com")
    assert client.endpoint == "http://custom-endpoint.example.com"


@pytest.mark.asyncio
async def test_search_returns_list_when_unavailable():
    client = MCPClient(endpoint="http://localhost:9999/nonexistent")
    results = await client.microsoft_docs_search("test query")
    assert isinstance(results, list)


@pytest.mark.asyncio
async def test_fetch_returns_dict_when_unavailable():
    client = MCPClient(endpoint="http://localhost:9999/nonexistent")
    result = await client.microsoft_docs_fetch("https://example.com")
    assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_check_availability_false_when_unavailable():
    client = MCPClient(endpoint="http://localhost:9999/nonexistent")
    available = await client.check_availability()
    assert available is False
    assert client.available is False

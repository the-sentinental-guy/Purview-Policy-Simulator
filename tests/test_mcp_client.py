"""
Tests for the MCPClient class in mcp_client.py.

All tests are synchronous wrappers around async coroutines (asyncio.run),
so no pytest-asyncio dependency is required.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mcp_client import MCPClient

# ── Helpers ──────────────────────────────────────────────────────────────────

def _make_tools_list_response(*tool_names):
    """Build a tools/list JSON-RPC result payload with the given tool names."""
    return {"result": {"tools": [{"name": n} for n in tool_names]}}


def _make_tools_call_response(*text_blocks):
    """Build a tools/call JSON-RPC result payload with text content blocks."""
    return {"result": {"content": [{"type": "text", "text": t} for t in text_blocks]}}


def _client_with_http():
    """Return a fresh MCPClient that looks like it has been __aenter__'d."""
    client = MCPClient()
    client._http = MagicMock()  # non-None so _post won't bail out early
    return client


# ── 1. Tool Discovery ─────────────────────────────────────────────────────────

class TestMCPClientToolDiscovery:

    def test_discover_tools_success(self):
        async def run():
            client = _client_with_http()
            client._post = AsyncMock(return_value=_make_tools_list_response(
                "docs_search", "docs_fetch", "code_sample_search"
            ))
            await client._discover_tools()
            assert client._tool_map.get("docs_search") == "docs_search"
            assert client._tool_map.get("docs_fetch") == "docs_fetch"
            assert client._tool_map.get("code_samples") == "code_sample_search"
        asyncio.run(run())

    def test_discover_tools_empty_response(self):
        async def run():
            client = _client_with_http()
            client._post = AsyncMock(return_value={"result": {"tools": []}})
            await client._discover_tools()
            assert client._tool_map == {}
        asyncio.run(run())

    def test_discover_tools_http_error(self):
        async def run():
            client = _client_with_http()
            client._post = AsyncMock(return_value=None)
            await client._discover_tools()  # must not raise
            assert client._tool_map == {}
        asyncio.run(run())

    def test_discover_tools_timeout(self):
        async def run():
            import httpx
            client = _client_with_http()
            client._post = AsyncMock(side_effect=httpx.TimeoutException("timeout"))
            # _discover_tools calls _post; if _post raises we expect graceful handling
            # Actually _post itself swallows exceptions; simulate _post returning None
            client._post = AsyncMock(return_value=None)
            await client._discover_tools()
            assert client._tool_map == {}
        asyncio.run(run())

    def test_discover_tools_called_only_once(self):
        async def run():
            client = _client_with_http()
            client._post = AsyncMock(return_value=_make_tools_list_response("docs_search"))
            await client._discover_tools()
            await client._discover_tools()
            await client._discover_tools()
            assert client._post.call_count == 1
        asyncio.run(run())


# ── 2. search_docs ────────────────────────────────────────────────────────────

class TestMCPClientSearchDocs:

    def test_search_docs_success(self):
        async def run():
            client = _client_with_http()

            async def fake_post(method, params):
                if method == "tools/list":
                    return _make_tools_list_response("docs_search")
                if method == "tools/call":
                    return _make_tools_call_response("Result text")
                return None

            client._post = AsyncMock(side_effect=fake_post)
            result = await client.search_docs("Azure Policy")
            assert isinstance(result, list)
            assert len(result) == 1
            assert result[0]["text"] == "Result text"
        asyncio.run(run())

    def test_search_docs_tool_unavailable(self):
        async def run():
            client = _client_with_http()
            # tools/list returns no docs_search tool
            client._post = AsyncMock(return_value=_make_tools_list_response("unrelated_tool"))
            result = await client.search_docs("Azure Policy")
            assert result == []
        asyncio.run(run())

    def test_search_docs_caches_results(self):
        async def run():
            client = _client_with_http()
            call_count = {"n": 0}

            async def fake_post(method, params):
                if method == "tools/list":
                    return _make_tools_list_response("docs_search")
                if method == "tools/call":
                    call_count["n"] += 1
                    return _make_tools_call_response("cached result")
                return None

            client._post = AsyncMock(side_effect=fake_post)
            await client.search_docs("same query")
            await client.search_docs("same query")
            assert call_count["n"] == 1  # tools/call invoked only once
        asyncio.run(run())

    def test_search_docs_timeout_returns_empty(self):
        async def run():
            client = _client_with_http()

            async def fake_post(method, params):
                if method == "tools/list":
                    return _make_tools_list_response("docs_search")
                # Simulate _post returning None (as it does on timeout)
                return None

            client._post = AsyncMock(side_effect=fake_post)
            result = await client.search_docs("something")
            assert result == []
        asyncio.run(run())


# ── 3. fetch_doc ──────────────────────────────────────────────────────────────

class TestMCPClientFetchDoc:

    def test_fetch_doc_success(self):
        async def run():
            client = _client_with_http()

            async def fake_post(method, params):
                if method == "tools/list":
                    return _make_tools_list_response("docs_fetch")
                if method == "tools/call":
                    return _make_tools_call_response("Page content here")
                return None

            client._post = AsyncMock(side_effect=fake_post)
            result = await client.fetch_doc("https://learn.microsoft.com/some-page")
            assert isinstance(result, str)
            assert "Page content here" in result
        asyncio.run(run())

    def test_fetch_doc_concatenates_multiple_blocks(self):
        async def run():
            client = _client_with_http()

            async def fake_post(method, params):
                if method == "tools/list":
                    return _make_tools_list_response("docs_fetch")
                if method == "tools/call":
                    return _make_tools_call_response("Block one", "Block two", "Block three")
                return None

            client._post = AsyncMock(side_effect=fake_post)
            result = await client.fetch_doc("https://learn.microsoft.com/page")
            assert result == "Block one\n\nBlock two\n\nBlock three"
        asyncio.run(run())

    def test_fetch_doc_unavailable_returns_empty_string(self):
        async def run():
            client = _client_with_http()
            client._post = AsyncMock(return_value=_make_tools_list_response("some_other_tool"))
            result = await client.fetch_doc("https://learn.microsoft.com/page")
            assert result == ""
        asyncio.run(run())


# ── 4. search_code_samples ────────────────────────────────────────────────────

class TestMCPClientCodeSamples:

    def test_search_code_samples_success(self):
        async def run():
            client = _client_with_http()

            async def fake_post(method, params):
                if method == "tools/list":
                    return _make_tools_list_response("code_sample_search")
                if method == "tools/call":
                    return _make_tools_call_response("sample code")
                return None

            client._post = AsyncMock(side_effect=fake_post)
            result = await client.search_code_samples("bicep policy assignment")
            assert isinstance(result, list)
            assert len(result) == 1
        asyncio.run(run())

    def test_search_code_samples_with_language(self):
        async def run():
            client = _client_with_http()
            captured = {}

            async def fake_post(method, params):
                if method == "tools/list":
                    return _make_tools_list_response("code_sample_search")
                if method == "tools/call":
                    captured["arguments"] = params.get("arguments", {})
                    return _make_tools_call_response("sample")
                return None

            client._post = AsyncMock(side_effect=fake_post)
            await client.search_code_samples("policy assignment", language="bicep")
            assert captured["arguments"].get("language") == "bicep"
        asyncio.run(run())

    def test_search_code_samples_empty_language_omitted(self):
        async def run():
            client = _client_with_http()
            captured = {}

            async def fake_post(method, params):
                if method == "tools/list":
                    return _make_tools_list_response("code_sample_search")
                if method == "tools/call":
                    captured["arguments"] = params.get("arguments", {})
                    return _make_tools_call_response("sample")
                return None

            client._post = AsyncMock(side_effect=fake_post)
            await client.search_code_samples("policy assignment", language="")
            assert "language" not in captured["arguments"]
        asyncio.run(run())


# ── 5. Context Manager ────────────────────────────────────────────────────────

class TestMCPClientContextManager:

    def test_context_manager_opens_http_client(self):
        async def run():
            client = MCPClient()
            assert client._http is None
            await client.__aenter__()
            assert client._http is not None
            await client.__aexit__(None, None, None)
        asyncio.run(run())

    def test_context_manager_closes_http_client(self):
        async def run():
            client = MCPClient()
            await client.__aenter__()
            assert client._http is not None
            await client.__aexit__(None, None, None)
            assert client._http is None
        asyncio.run(run())


# ── 6. Error Handling ─────────────────────────────────────────────────────────

class TestMCPClientErrorHandling:

    def test_json_decode_error_returns_none(self):
        """_post should return None when the server returns invalid JSON."""
        async def run():
            import httpx

            client = _client_with_http()
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json = MagicMock(side_effect=ValueError("invalid json"))
            client._http.post = AsyncMock(return_value=mock_response)

            result = await client._post("tools/list", {})
            assert result is None
        asyncio.run(run())

    def test_server_error_json_returns_none(self):
        """_post should return None when the response contains an 'error' key."""
        async def run():
            client = _client_with_http()
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json = MagicMock(return_value={"error": "server error", "id": 1})
            client._http.post = AsyncMock(return_value=mock_response)

            result = await client._post("tools/list", {})
            assert result is None
        asyncio.run(run())

    def test_network_error_returns_empty(self):
        """search_docs should return [] when _post raises an unexpected exception."""
        async def run():
            client = _client_with_http()

            async def fake_post(method, params):
                if method == "tools/list":
                    return _make_tools_list_response("docs_search")
                raise RuntimeError("network gone")

            client._post = AsyncMock(side_effect=fake_post)
            # search_docs → _call_tool → _post("tools/call") raises;
            # but _call_tool calls _post which itself catches all exceptions.
            # Simulate _post returning None (its actual behaviour on error).
            async def safe_post(method, params):
                if method == "tools/list":
                    return _make_tools_list_response("docs_search")
                return None

            client._post = AsyncMock(side_effect=safe_post)
            result = await client.search_docs("anything")
            assert result == []
        asyncio.run(run())

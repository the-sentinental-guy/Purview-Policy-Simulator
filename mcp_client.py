"""
Microsoft Learn MCP Server client.

Implements the MCP Streamable HTTP protocol to communicate with the
Microsoft Learn API at https://learn.microsoft.com/api/mcp.

Protocol summary:
  - POST JSON-RPC 2.0 messages to https://learn.microsoft.com/api/mcp
  - tools/list  → discover available tools
  - tools/call  → invoke a specific tool by name with arguments
  - Responses carry result.tools (list) or result.content (list of {type, text})

Usage (async context manager):

    async with MCPClient() as client:
        results = await client.search_docs("Azure Policy compliance")

Usage (module-level convenience functions, shared client):

    results = await search_docs("Azure Policy compliance")
    page    = await fetch_doc("https://learn.microsoft.com/...")
    samples = await search_code_samples("bicep policy assignment", language="bicep")
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

# ── Constants ────────────────────────────────────────────────────────────────

MCP_ENDPOINT = "https://learn.microsoft.com/api/mcp"
REQUEST_TIMEOUT = 5.0  # seconds per call

# Friendly capability names → possible real tool-name substrings (lowercase).
# The client searches tool names returned by tools/list for these substrings.
_TOOL_HINTS: dict[str, list[str]] = {
    "docs_search":   ["docs_search", "learn_search", "search_documentation", "search_docs"],
    "docs_fetch":    ["docs_fetch",  "fetch_doc",    "get_documentation",    "fetch_page"],
    "code_samples":  ["code_sample", "sample_search","find_sample",          "code_search"],
}


# ── MCPClient ────────────────────────────────────────────────────────────────

class MCPClient:
    """
    Async client for the Microsoft Learn MCP server.

    Discovers available tools on first use, maps them to the three high-level
    capabilities (docs search, doc fetch, code samples), and caches every
    successful response for the lifetime of the instance.
    """

    def __init__(self) -> None:
        self._http: httpx.AsyncClient | None = None
        # In-memory cache: (capability, sorted-arg-pairs) → content list
        self._cache: dict[tuple[str, tuple[tuple[str, Any], ...]], list[dict[str, Any]]] = {}
        # Resolved tool names: capability key → actual tool name on the server
        self._tool_map: dict[str, str] = {}
        self._tools_discovered = False
        self._request_id = 0

    # ── Lifecycle ────────────────────────────────────────────────────────────

    async def __aenter__(self) -> "MCPClient":
        self._http = httpx.AsyncClient(
            timeout=REQUEST_TIMEOUT,
            headers={
                "Content-Type": "application/json",
                "Accept":       "application/json",
                "Accept-Encoding": "gzip, deflate, br",
            },
        )
        return self

    async def __aexit__(self, *_: Any) -> None:
        if self._http:
            await self._http.aclose()
            self._http = None

    # ── Low-level JSON-RPC helpers ────────────────────────────────────────────

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    async def _post(self, method: str, params: dict[str, Any]) -> dict[str, Any] | None:
        """
        Send a single JSON-RPC 2.0 request to the MCP endpoint.

        Returns the parsed response dict on success, or None on any error.
        Never raises — all exceptions are caught and logged.
        """
        if self._http is None:
            # Client was not entered via context manager; caller should use `async with`.
            logger.error("MCPClient._post called before __aenter__; use `async with MCPClient()`.")
            return None

        payload = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": method,
            "params": params,
        }
        try:
            response = await self._http.post(MCP_ENDPOINT, content=json.dumps(payload))
            response.raise_for_status()
            data = response.json()
            if "error" in data:
                logger.warning("MCP error from server: %s", data["error"])
                return None
            return data
        except httpx.TimeoutException:
            logger.warning("MCP request timed out (method=%s)", method)
        except httpx.HTTPStatusError as exc:
            logger.warning("MCP HTTP error %s (method=%s)", exc.response.status_code, method)
        except Exception as exc:  # noqa: BLE001
            logger.warning("MCP unexpected error (method=%s): %s: %s",
                           method, type(exc).__name__, exc)
        return None

    # ── Tool discovery ────────────────────────────────────────────────────────

    async def _discover_tools(self) -> None:
        """
        Call tools/list once and build the internal capability → tool-name map.
        Sets self._tools_discovered=True regardless of outcome so we only try once.
        """
        if self._tools_discovered:
            return
        self._tools_discovered = True  # mark now to avoid re-entry on failure

        data = await self._post("tools/list", {})
        if not data:
            logger.warning("Could not discover MCP tools; will retry on next instantiation.")
            return

        tools: list[dict[str, Any]] = data.get("result", {}).get("tools", [])
        if not tools:
            logger.warning("MCP tools/list returned an empty tool list.")
            return

        logger.debug("MCP tools available: %s", [t.get("name") for t in tools])

        # Build a lower-cased name → original name lookup
        name_lookup = {t["name"].lower(): t["name"] for t in tools if "name" in t}

        for capability, hints in _TOOL_HINTS.items():
            for hint in hints:
                # Exact substring match in any tool name
                matched = next(
                    (orig for lower, orig in name_lookup.items() if hint in lower),
                    None,
                )
                if matched:
                    self._tool_map[capability] = matched
                    logger.debug("Mapped capability '%s' → tool '%s'", capability, matched)
                    break
            else:
                logger.debug("No tool found for capability '%s'", capability)

    # ── Cached tool call ──────────────────────────────────────────────────────

    async def _call_tool(self, capability: str, arguments: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Invoke a tool by capability name.

        Returns the result.content list (each item: {type, text, ...}).
        Returns an empty list if the tool is unavailable or the call fails.
        """
        await self._discover_tools()

        tool_name = self._tool_map.get(capability)
        if not tool_name:
            logger.debug("Capability '%s' is not available on this MCP server.", capability)
            return []

        # Cache key: (capability, sorted argument pairs)
        cache_key = (capability, tuple(sorted(arguments.items())))
        if cache_key in self._cache:
            return self._cache[cache_key]

        data = await self._post("tools/call", {"name": tool_name, "arguments": arguments})
        if not data:
            return []

        content: list[dict[str, Any]] = data.get("result", {}).get("content", [])
        self._cache[cache_key] = content
        return content

    # ── High-level API ────────────────────────────────────────────────────────

    async def search_docs(self, query: str) -> list[dict[str, Any]]:
        """
        Search Microsoft Learn documentation.

        Args:
            query: Natural-language or keyword search query.

        Returns:
            List of result dicts, each typically containing at least
            ``{"type": "text", "text": "..."}`` from the MCP server.
            Returns an empty list when the server is unavailable.
        """
        return await self._call_tool("docs_search", {"query": query})

    async def fetch_doc(self, url: str) -> str:
        """
        Fetch a Microsoft Learn documentation page as Markdown.

        Args:
            url: Full URL of the page (e.g. https://learn.microsoft.com/...).

        Returns:
            The page content as a Markdown string, or an empty string on failure.
        """
        content = await self._call_tool("docs_fetch", {"url": url})
        # Concatenate all text-type content blocks
        return "\n\n".join(
            item["text"] for item in content if item.get("type") == "text" and item.get("text")
        )

    async def search_code_samples(self, query: str, language: str = "") -> list[dict[str, Any]]:
        """
        Search for Microsoft code samples on GitHub / Learn.

        Args:
            query:    Description of the desired sample.
            language: Optional programming language filter (e.g. "python", "bicep").

        Returns:
            List of result dicts from the MCP server, or an empty list on failure.
        """
        arguments: dict[str, Any] = {"query": query}
        if language:
            arguments["language"] = language
        return await self._call_tool("code_samples", arguments)


# ── Module-level shared client & convenience functions ────────────────────────

# A single shared client instance is created lazily and reused across calls.
_shared_client: MCPClient | None = None
_shared_client_lock: asyncio.Lock | None = None


def _get_lock() -> asyncio.Lock:
    """Return (lazily create) the module-level asyncio.Lock for shared-client init."""
    global _shared_client_lock
    if _shared_client_lock is None:
        _shared_client_lock = asyncio.Lock()
    return _shared_client_lock


async def _get_shared_client() -> MCPClient:
    """Return (and lazily initialise) the module-level shared MCPClient."""
    global _shared_client
    async with _get_lock():
        if _shared_client is None or _shared_client._http is None:
            _shared_client = MCPClient()
            await _shared_client.__aenter__()
    return _shared_client


async def close_shared_client() -> None:
    """
    Close the module-level shared MCPClient and release its HTTP connection pool.

    Call this at application shutdown when using the module-level convenience
    functions (``search_docs``, ``fetch_doc``, ``search_code_samples``).
    If you use ``MCPClient`` directly via ``async with``, this is not needed.
    """
    global _shared_client
    async with _get_lock():
        if _shared_client is not None:
            await _shared_client.__aexit__(None, None, None)
            _shared_client = None


async def search_docs(query: str) -> list[dict[str, Any]]:
    """Module-level convenience wrapper for :meth:`MCPClient.search_docs`."""
    client = await _get_shared_client()
    return await client.search_docs(query)


async def fetch_doc(url: str) -> str:
    """Module-level convenience wrapper for :meth:`MCPClient.fetch_doc`."""
    client = await _get_shared_client()
    return await client.fetch_doc(url)


async def search_code_samples(query: str, language: str = "") -> list[dict[str, Any]]:
    """Module-level convenience wrapper for :meth:`MCPClient.search_code_samples`."""
    client = await _get_shared_client()
    return await client.search_code_samples(query, language)

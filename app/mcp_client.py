import asyncio
import json
import logging
import uuid
from typing import Any, Dict, List, Optional

import httpx

from app.models.simulation import MCPDocumentation

logger = logging.getLogger(__name__)


class MCPClient:
    endpoint = "https://learn.microsoft.com/api/mcp"
    timeout = 5.0

    def __init__(self) -> None:
        self._cache: Dict[str, Any] = {}
        self._available: Optional[bool] = None
        self._available_tools: List[Dict] = []

    async def discover_tools(self) -> List[Dict]:
        payload = {"jsonrpc": "2.0", "id": str(uuid.uuid4()), "method": "tools/list", "params": {}}
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.endpoint,
                    json=payload,
                    headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
                )
                data = self._parse_response(response)
                tools = data.get("result", {}).get("tools", []) if data else []
                self._available_tools = tools
                self._available = True
                return tools
        except Exception as exc:
            logger.warning("MCP server unavailable during tool discovery: %s", exc)
            self._available = False
            return []

    async def is_available(self) -> bool:
        if self._available is None:
            await self.discover_tools()
        return bool(self._available)

    async def _call_tool(self, tool_name: str, arguments: Dict) -> Optional[Dict]:
        if self._available is False:
            return None

        cache_key = f"{tool_name}:{json.dumps(arguments, sort_keys=True)}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        call_id = str(uuid.uuid4())
        payload = {
            "jsonrpc": "2.0",
            "id": call_id,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        }
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.endpoint,
                    json=payload,
                    headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
                )
                data = self._parse_response(response)
                if data is None:
                    return None
                result = data.get("result")
                self._cache[cache_key] = result
                return result
        except Exception as exc:
            logger.warning("MCP tool call '%s' failed: %s", tool_name, exc)
            return None

    def _parse_response(self, response: httpx.Response) -> Optional[Dict]:
        """Parse either a regular JSON or SSE (text/event-stream) response."""
        content_type = response.headers.get("content-type", "")
        try:
            if "text/event-stream" in content_type:
                return self._parse_sse(response.text)
            return response.json()
        except Exception as exc:
            logger.warning("Failed to parse MCP response: %s", exc)
            return None

    @staticmethod
    def _parse_sse(text: str) -> Optional[Dict]:
        """Extract the first JSON-RPC message from an SSE stream."""
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("data:"):
                data_str = line[len("data:"):].strip()
                if data_str:
                    try:
                        return json.loads(data_str)
                    except json.JSONDecodeError:
                        continue
        return None

    @staticmethod
    def _extract_content_text(result: Dict) -> Optional[str]:
        """Pull text out of a result that may contain a list of content blocks."""
        if result is None:
            return None
        # Direct text field
        if isinstance(result, str):
            return result
        # content list: [{"type": "text", "text": "..."}]
        content = result.get("content")
        if isinstance(content, list):
            parts = [block.get("text", "") for block in content if block.get("type") == "text"]
            return "\n".join(parts) if parts else None
        if isinstance(content, str):
            return content
        return None

    async def search_docs(self, query: str) -> List[MCPDocumentation]:
        try:
            result = await self._call_tool("microsoft_docs_search", {"query": query})
            if result is None:
                return []
            docs: List[MCPDocumentation] = []
            # Result may be a list directly or wrapped in content blocks
            items = None
            if isinstance(result, list):
                items = result
            else:
                text = self._extract_content_text(result)
                if text:
                    try:
                        parsed = json.loads(text)
                        items = parsed if isinstance(parsed, list) else parsed.get("results", [parsed])
                    except (json.JSONDecodeError, AttributeError):
                        items = []
            for item in (items or []):
                if isinstance(item, dict):
                    docs.append(
                        MCPDocumentation(
                            title=item.get("title", ""),
                            url=item.get("url", item.get("contentUrl", "")),
                            summary=item.get("summary", item.get("description", item.get("content", ""))[:300] if item.get("content") else ""),
                        )
                    )
            return docs
        except Exception as exc:
            logger.warning("search_docs failed: %s", exc)
            return []

    async def fetch_doc(self, url: str) -> Optional[str]:
        try:
            result = await self._call_tool("microsoft_docs_fetch", {"url": url})
            if result is None:
                return None
            return self._extract_content_text(result)
        except Exception as exc:
            logger.warning("fetch_doc failed for %s: %s", url, exc)
            return None

    async def search_code_samples(self, query: str, language: str = "powershell") -> List[Dict]:
        try:
            result = await self._call_tool(
                "microsoft_code_sample_search", {"query": query, "language": language}
            )
            if result is None:
                return []
            if isinstance(result, list):
                return result
            text = self._extract_content_text(result)
            if text:
                try:
                    parsed = json.loads(text)
                    return parsed if isinstance(parsed, list) else parsed.get("results", [])
                except (json.JSONDecodeError, AttributeError):
                    pass
            return []
        except Exception as exc:
            logger.warning("search_code_samples failed: %s", exc)
            return []

    async def enrich_simulation(self, query: str, template_names: List[str]) -> Dict:
        combined_query = query
        if template_names:
            combined_query = f"{query} {' '.join(template_names)}"

        documentation_links, code_samples = await asyncio.gather(
            self.search_docs(combined_query),
            self.search_code_samples(combined_query),
            return_exceptions=True,
        )

        if isinstance(documentation_links, BaseException):
            logger.warning("enrich_simulation search_docs error: %s", documentation_links)
            documentation_links = []
        if isinstance(code_samples, BaseException):
            logger.warning("enrich_simulation search_code_samples error: %s", code_samples)
            code_samples = []

        return {
            "documentation_links": documentation_links,
            "code_samples": code_samples,
        }


mcp_client = MCPClient()

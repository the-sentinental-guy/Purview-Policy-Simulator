import httpx
import logging
from simulator.config import MCP_ENDPOINT

logger = logging.getLogger(__name__)


class MCPClient:
    def __init__(self, endpoint: str = MCP_ENDPOINT):
        self.endpoint = endpoint
        self.available = False

    async def check_availability(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(self.endpoint)
                self.available = response.status_code < 500
        except Exception:
            self.available = False
        return self.available

    async def microsoft_docs_search(self, query: str) -> list:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                payload = {
                    "tool": "microsoft_docs_search",
                    "parameters": {"query": query, "top": 3}
                }
                response = await client.post(self.endpoint, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("results", [])
        except Exception as e:
            logger.debug(f"MCP search unavailable: {e}")
        return []

    async def microsoft_docs_fetch(self, url: str) -> dict:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                payload = {
                    "tool": "microsoft_docs_fetch",
                    "parameters": {"url": url}
                }
                response = await client.post(self.endpoint, json=payload)
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            logger.debug(f"MCP fetch unavailable: {e}")
        return {}

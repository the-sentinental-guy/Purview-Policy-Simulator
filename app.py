"""
Purview Policy Simulator - Flask Application
"""

import asyncio
import logging
import os

from flask import Flask, jsonify, render_template, request

from simulator import simulate

logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/simulate", methods=["POST"])
def run_simulation():
    data = request.get_json(silent=True) or {}
    user_input = str(data.get("requirement", "")).strip()
    use_mcp = bool(data.get("use_mcp", False))

    if not user_input:
        return jsonify({"error": "Please provide a policy requirement description."}), 400

    result = simulate(user_input)

    if use_mcp:
        mcp_data = _fetch_mcp_enrichment(result.get("doc_search_query", user_input))
        result["mcp_docs"] = mcp_data.get("docs", [])
        result["mcp_code_samples"] = mcp_data.get("code_samples", [])
    else:
        result["mcp_docs"] = []
        result["mcp_code_samples"] = []

    return jsonify(result)


def _fetch_mcp_enrichment(query: str) -> dict:
    """Run async MCP fetch in a synchronous Flask context."""
    try:
        from mcp_client import MCPClient

        async def _run():
            async with MCPClient() as client:
                docs = await client.search_docs(query)
                samples = await client.search_code_samples(query, language="PowerShell")
            return {"docs": docs, "code_samples": samples}

        return asyncio.run(_run())
    except Exception:  # noqa: BLE001 — MCP is optional enrichment
        logger.warning("MCP enrichment failed; returning empty results.", exc_info=True)
        return {"docs": [], "code_samples": []}


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug, port=5000)

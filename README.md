# Purview Policy Simulator

An AI-powered Microsoft Purview policy simulation tool that translates natural language descriptions into concrete policy configurations with confidence scoring, expected effects analysis, and optional live Microsoft Learn documentation enrichment.

## Features

- **40+ DLP Policy Templates** — Financial (PCI-DSS, SOX, GLBA), Healthcare (HIPAA, PHI), Privacy (GDPR, CCPA, LGPD), Regional (UK DPA, PIPEDA, APPI), IP Protection, Endpoint DLP, and more
- **TF-IDF Semantic Matching** — Cosine similarity matching with keyword and framework boosting
- **Microsoft Learn MCP Integration** — Live documentation enrichment via the official Microsoft Learn MCP Server
- **Confidence Scoring** — Color-coded HIGH/MEDIUM/LOW/VERY_LOW with reasoning
- **Gap Analysis** — Identifies what's covered and what's missing for custom policy recommendations
- **Modern Fluent UI** — Chat-style interface with collapsible result cards

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Static Frontend                        │
│   index.html  │  styles.css  │  app.js                   │
│   (Chat UI, Fluent Design, Collapsible Result Cards)      │
└────────────────────────┬─────────────────────────────────┘
                         │ HTTP/REST
┌────────────────────────▼─────────────────────────────────┐
│                   FastAPI Backend                         │
│   POST /simulate  │  GET /templates  │  GET /health       │
│   GET /mcp/status │  GET /templates/categories            │
└──────┬──────────────────────────────────────┬────────────┘
       │                                      │
┌──────▼──────────┐              ┌────────────▼───────────┐
│ Simulation      │              │  MCP Client             │
│ Engine          │              │  (httpx async)          │
│                 │              │                         │
│ NLPProcessor    │              │  learn.microsoft.com    │
│ PolicyMatcher   │              │  /api/mcp               │
│ EffectsCalc     │              │  (tools/list,           │
│                 │              │   tools/call)           │
└──────┬──────────┘              └─────────────────────────┘
       │
┌──────▼──────────────────────────────────────────────────┐
│                   Knowledge Base                          │
│  DLP Templates (40+)  │  Sensitivity Labels              │
│  Retention Policies   │  Insider Risk Templates          │
│  Troubleshooting      │  Architecture Reference          │
└─────────────────────────────────────────────────────────┘
```

## Setup

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
git clone https://github.com/the-sentinental-guy/Purview-Policy-Simulator.git
cd Purview-Policy-Simulator
pip install -r requirements.txt
```

### Running the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open your browser at `http://localhost:8000`

## Usage

### Web UI

1. Open `http://localhost:8000` in your browser
2. Click example prompts in the left sidebar or type your policy description
3. (Optional) Enable **Live MS Learn Docs** toggle in Settings to enrich results with official documentation
4. Click **Simulate** or press `Ctrl+Enter`

### REST API

**Simulate a policy:**
```bash
curl -X POST http://localhost:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Prevent employees from sharing credit card numbers via email and Teams, PCI-DSS compliant",
    "use_mcp": false,
    "max_templates": 3
  }'
```

**List all templates:**
```bash
curl http://localhost:8000/templates
curl http://localhost:8000/templates?category=Financial
curl http://localhost:8000/templates/categories
```

**Check MCP status:**
```bash
curl http://localhost:8000/mcp/status
```

### Example Response

```json
{
  "query": "prevent credit card numbers via email PCI-DSS",
  "intent": "prevent",
  "entities": {
    "data_types": ["credit card"],
    "locations": ["exchange"],
    "frameworks": ["PCI-DSS"]
  },
  "template_matches": [
    {
      "template": {
        "id": "pci_dss",
        "name": "U.S. PCI Data Security Standard",
        "category": "Financial",
        "description": "...",
        "locations": ["Exchange", "SharePoint", "OneDrive", "Teams"],
        "compliance_frameworks": ["PCI-DSS"]
      },
      "confidence": {
        "score": 0.92,
        "level": "HIGH",
        "reasoning": "Strong TF-IDF match; PCI-DSS framework match; credit card keyword match"
      },
      "similarity_score": 0.72
    }
  ],
  "effects": {
    "blocked_actions": ["Block email sending containing credit card numbers to external recipients"],
    "policy_tips": ["Policy tip shown to users in Outlook/Teams before sending"],
    "deployment_recommendations": ["Enable in test mode for 2 weeks before enforcement"]
  },
  "documentation_links": [],
  "mcp_enriched": false,
  "processing_time_ms": 45.2
}
```

## MCP Configuration

The Microsoft Learn MCP Server integration uses the official public endpoint:

- **Endpoint**: `https://learn.microsoft.com/api/mcp`
- **Authentication**: None required (free, public)
- **Protocol**: Streamable HTTP (JSON-RPC 2.0)
- **Timeout**: 5 seconds per call
- **Caching**: Session-level in-memory cache

To enable MCP enrichment:
1. Toggle "Live MS Learn Docs" in the UI Settings panel, **or**
2. Set `"use_mcp": true` in the API request body

MCP provides:
- `microsoft_docs_search` — semantic search for Purview documentation
- `microsoft_docs_fetch` — fetch full documentation pages as Markdown
- `microsoft_code_sample_search` — find PowerShell cmdlets and configuration scripts

If the MCP server is unavailable, the simulator gracefully falls back to its embedded knowledge base.

## Running Tests

```bash
pytest tests/ -v
```

All 31 tests should pass covering:
- Knowledge base (templates count, structure, categories)
- MCP client (mocked responses, error handling)
- Simulation engine (NLP, matching, end-to-end simulation)
- FastAPI endpoints (all routes)

## DLP Template Categories

| Category | Count | Examples |
|---|---|---|
| Financial | 8+ | PCI-DSS, SOX, GLBA, Bank Accounts, SWIFT |
| Healthcare | 6+ | HIPAA, PHI, Medical Records, DEA Numbers |
| Privacy | 8+ | GDPR, CCPA, LGPD, SSN, Passport Numbers |
| Regional | 5+ | UK DPA, Australia Privacy Act, PIPEDA |
| IP Protection | 4+ | Source Code, Trade Secrets, Patents |
| Endpoint DLP | 4+ | USB Blocking, Print Blocking, Clipboard |
| General | 5+ | General PII, Confidential Docs, Customer Data |


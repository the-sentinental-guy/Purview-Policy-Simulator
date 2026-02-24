# Microsoft Purview Policy Simulator

A production-quality FastAPI web application that simulates Microsoft Purview DLP policy matching using NLP and TF-IDF analysis. Describe your data protection scenario in plain English and instantly see which DLP templates match, what effects they will have, and relevant Microsoft Learn documentation.

## Features

- **59+ DLP Policy Templates** across 6 categories: Financial, Healthcare, Privacy/PII, Regional Compliance, Intellectual Property, General
- **NLP Analysis** — extracts intent, data types, locations, compliance frameworks, and risk scenarios from natural-language queries
- **TF-IDF Matching Engine** — scikit-learn TF-IDF vectorizer with bonus scoring for compliance, data type, and location alignment
- **Confidence Scoring** — HIGH / MEDIUM / LOW / VERY_LOW with explainability
- **Effects Simulation** — blocked actions, audit trail, user/admin notifications, false positive risk, deployment recommendations, license dependencies
- **MCP Integration** — optional Microsoft Docs real-time enrichment via MCP endpoint
- **Modern Web UI** — Fluent Design sidebar + card-based results with tabbed policy config, effects, and references views
- **REST API** — `/health`, `/templates`, `/simulate` endpoints

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python run.py
# Open http://localhost:8000
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/templates` | List all 59+ templates by category |
| POST | `/simulate` | Run a simulation query |

### Example `/simulate` request

```json
{
  "query": "Prevent credit card numbers from being emailed externally",
  "mcp_enabled": false
}
```

## File Structure

```
├── requirements.txt
├── setup.py
├── run.py
├── pytest.ini
├── simulator/
│   ├── app.py              # FastAPI application
│   ├── config.py
│   ├── mcp_client.py       # Microsoft Docs MCP integration
│   ├── engine/
│   │   ├── nlp_processor.py  # NLP intent/entity extraction
│   │   ├── matcher.py        # TF-IDF template matching
│   │   ├── effects.py        # Effects generation
│   │   └── simulator.py      # Orchestration engine
│   ├── knowledge_base/
│   │   ├── dlp_templates.py       # 59+ DLP policy templates
│   │   ├── sensitivity_labels.py
│   │   ├── retention_policies.py
│   │   ├── insider_risk.py
│   │   ├── sensitive_info_types.py
│   │   ├── conditions_actions.py
│   │   ├── troubleshooting.py
│   │   ├── architecture.py
│   │   └── documentation_refs.py
│   ├── models/
│   │   ├── policy.py
│   │   ├── simulation.py
│   │   ├── confidence.py
│   │   └── effects.py
│   └── static/             # Web UI (HTML/CSS/JS)
└── tests/                  # 41 pytest tests
```

## Running Tests

```bash
python -m pytest tests/ -v
```

All 41 tests pass covering: API endpoints, NLP processor, TF-IDF matcher, effects generator, simulation engine, and MCP client.

## Policy Categories

| Category | Templates | Key Regulations |
|----------|-----------|-----------------|
| Financial | 11 | PCI DSS, SOX, GLBA, SWIFT |
| Healthcare | 9 | HIPAA, HITECH, DEA |
| Privacy/PII | 8 | GDPR, CCPA, COPPA, BIPA |
| Regional Compliance | 9 | UK GDPR, Australian Privacy Act, PIPEDA, LGPD, PDPA, FERPA |
| Intellectual Property | 7 | Trade Secrets Act, DTSA, NDA |
| General | 15 | SOX, FLSA, FCRA, NIST |

## License

MIT

# Microsoft Purview Policy Simulator

![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/flask-3.x-lightgrey?logo=flask&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

An interactive web application for simulating Microsoft Purview compliance policies. Describe your data-protection requirement in plain English and get instant recommendations — matched templates, confidence scores, gap analysis, and live documentation links — without needing access to the Purview portal.

![Purview Policy Simulator UI](https://github.com/user-attachments/assets/62da92ce-d365-4b6c-9386-4374b7d4253f)

---

## Features

| # | Capability |
|---|-----------|
| 1 | **53+ policy templates** across DLP, Information Protection, Insider Risk Management, and Retention |
| 2 | **TF-IDF + cosine similarity** semantic matching (with scikit-learn) with keyword fallback |
| 3 | **Microsoft Learn MCP Server integration** for live, up-to-date documentation links |
| 4 | **Intent and entity extraction** from natural language (detects policy type, data categories, regions, industries) |
| 5 | **Multi-template combination recommendations** when a single template is insufficient |
| 6 | **Gap analysis** that flags coverage holes and suggests complementary policies |
| 7 | **Modern Fluent Design web UI** with a collapsible left sidebar, quick-prompt chips, and dark/light theming |
| 8 | **Real-time simulation** with 0–100% confidence scoring and human-readable reasoning |

---

## Quick Start

```bash
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

---

## Installation

### Prerequisites

- Python 3.10 or later

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/the-sentinental-guy/Purview-Policy-Simulator.git
cd Purview-Policy-Simulator

# 2. (Optional but recommended) Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the application
python app.py
```

Open your browser at **http://127.0.0.1:5000**.

> **Note:** `scikit-learn` is an optional dependency. If installed, the simulator uses TF-IDF cosine similarity for richer semantic matching. If absent it falls back to keyword scoring only.

---

## Usage Examples

Type (or paste) a scenario into the chat box and click **Run Simulation**. Below are three representative queries and what to expect.

### Example 1 — HIPAA / Healthcare DLP

**Query:**
```
We need to prevent employees from emailing patient health records outside the organization.
```

**Expected output:**
- ✅ **Matched template:** U.S. HIPAA DLP Policy (confidence ~88%)
- 📋 **Workloads:** Exchange, SharePoint, OneDrive, Teams
- 🔎 **Sensitive info types:** U.S. / U.K. Drug Enforcement Agency (DEA) Number, International Classification of Diseases (ICD-10), etc.
- ⚙️ **Default action:** Block external sharing, notify user and compliance officer
- 💡 **Gap analysis:** Consider pairing with an Insider Risk departing-user template if offboarding scenarios are in scope

---

### Example 2 — GDPR for EU Operations

**Query:**
```
Our company processes personal data for EU customers and we need GDPR-compliant controls on storage and sharing.
```

**Expected output:**
- ✅ **Matched template:** GDPR DLP Policy (confidence ~85%)
- 📋 **Workloads:** Exchange, SharePoint, OneDrive, Teams, Devices
- 🔎 **Sensitive info types:** EU passport/national ID numbers, IBAN, IP addresses, etc.
- ⚙️ **Default action:** Restrict sharing, apply encryption, log to audit trail
- 💡 **Gap analysis:** Retention policy for right-to-erasure compliance recommended

---

### Example 3 — Source Code / Intellectual Property

**Query:**
```
Protect proprietary source code and trade secrets from being uploaded to personal cloud storage.
```

**Expected output:**
- ✅ **Matched template:** Source Code / IP Protection DLP (confidence ~82%)
- 📋 **Workloads:** Devices (Endpoint DLP), SharePoint, OneDrive
- 🔎 **Entities detected:** `source code`, `trade secret`, `intellectual property`
- ⚙️ **Custom config:** Keyword dictionary with programming-language terms + Endpoint DLP block rule for cloud-egress
- 💡 **Combination:** Pair with Sensitivity Label "Confidential – Engineering" for automatic classification

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Browser (UI)                         │
│  ┌──────────────┐  ┌────────────────────────────────────┐  │
│  │  Left Sidebar │  │  Main Content (Chat + Results)      │  │
│  │  - Prompts    │  │  - Simulation Summary               │  │
│  │  - Settings   │  │  - Template Matches                 │  │
│  │  - MCP Toggle │  │  - Custom Configs                   │  │
│  └──────────────┘  │  - Doc Links (MCP)                  │  │
│                    └────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                           │ HTTP POST /api/simulate
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask Application                        │
│  ┌───────────────┐  ┌─────────────────┐  ┌─────────────┐  │
│  │  Simulator    │  │  Knowledge Base  │  │  MCP Client │  │
│  │  Engine       │  │  53+ Templates   │  │             │  │
│  │  - TF-IDF     │  │  - DLP           │  │  tools/list │  │
│  │  - Keyword    │  │  - Info Prot.    │  │  tools/call │  │
│  │  - Intent     │  │  - Insider Risk  │  │             │  │
│  │  - Entities   │  │  - Retention     │  └──────┬──────┘  │
│  └───────────────┘  └─────────────────┘         │         │
└─────────────────────────────────────────────────│─────────┘
                                                   │ HTTPS
                                                   ▼
                                     ┌─────────────────────┐
                                     │  Microsoft Learn    │
                                     │  MCP Server         │
                                     │  learn.microsoft.com│
                                     │  /api/mcp           │
                                     └─────────────────────┘
```

---

## MCP Integration

### What is the MCP Server?

The **Microsoft Learn MCP Server** is a Model Context Protocol (MCP) endpoint hosted at `https://learn.microsoft.com/api/mcp`. It exposes Microsoft documentation as callable tools, enabling the simulator to surface live, accurate documentation links alongside every simulation result.

### Enabling MCP

Toggle the **"Use MCP"** checkbox in the left sidebar before running a simulation. When enabled, each matched template result will include a **Docs** section with links fetched directly from Microsoft Learn.

### Protocol

- **Transport:** JSON-RPC 2.0 over HTTPS POST
- **Authentication:** None required
- **Content-Type:** `application/json`

### Available Tools

| Tool | Description |
|------|-------------|
| `microsoft_docs_search` | Full-text search across Microsoft Learn documentation |
| `microsoft_docs_fetch` | Retrieve the content of a specific documentation page |
| `microsoft_docs_code_samples` | Retrieve code samples related to a topic |

### Example MCP Request / Response

**Request:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "microsoft_docs_search",
    "arguments": {
      "query": "DLP policy HIPAA Purview",
      "top": 3
    }
  }
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "## Results\n1. [Configure DLP for HIPAA](https://learn.microsoft.com/...)\n2. ..."
      }
    ]
  }
}
```

---

## Knowledge Base

The knowledge base (`knowledge_base.py`) contains **53+ policy templates** organized into the following categories:

### DLP Templates (23 templates)

| Sub-category | Templates |
|---|---|
| Financial | 4 (PCI-DSS, U.S. Financial, ABA Routing, SWIFT) |
| Healthcare | 2 (HIPAA, U.K. Health) |
| Privacy / PII | 5 (U.S. PII, GDPR, Canada PII, Australia PII, Japan PII) |
| Regional | 5 (U.K. Financial, France CNIL, Germany BDSG, India PDP, Brazil LGPD) |
| IP Protection | 3 (Source Code, Trade Secrets, Engineering Documents) |
| Endpoint | 4 (Removable Media, Cloud Egress, Print/Screenshot, Browser Upload) |

### Information Protection (6 templates)

Six sensitivity label templates covering: Public, General, Confidential, Highly Confidential, External Sharing, and Encrypted Email.

### Insider Risk Management (6 templates)

Data theft by departing users, disgruntled employee signals, privileged user risks, contractor off-boarding, mass download, and anomalous data exfiltration.

### Data Lifecycle Management (5 templates)

General retention, legal hold, records management, regulatory archive, and auto-apply retention labels.

### Communication Compliance (1 template)

Regulatory monitoring in Microsoft Teams and Exchange.

---

## Simulation Engine

Every query goes through a six-step pipeline in `simulator.py`:

### Step 1 — Keyword Scoring

Each template defines a list of keywords and phrases. The engine scans the query using word-boundary-aware regex, awarding partial scores for individual keywords and bonus scores for exact phrase matches.

### Step 2 — TF-IDF Cosine Similarity *(optional)*

If `scikit-learn` is installed, the engine builds a TF-IDF matrix from all template descriptions and computes the cosine similarity between the query vector and each template vector. This catches synonyms and paraphrases that keyword matching would miss.

### Step 3 — Hybrid Score Calculation

Keyword score and TF-IDF score are combined with configurable weights (default: 60 % keyword / 40 % TF-IDF) into a single normalized confidence value.

### Step 4 — Intent and Entity Extraction

A lightweight NLP pass extracts:
- **Intent** — e.g., `prevent_sharing`, `classify_data`, `monitor_communication`
- **Entities** — data categories (`PII`, `PHI`, `source code`), regions (`EU`, `U.S.`), industries (`healthcare`, `finance`), and workloads (`Exchange`, `Teams`, `Devices`)

Extracted intent and entities can boost or suppress individual template scores.

### Step 5 — Multi-Template Combination

When the top-scoring template does not cover all detected entities, the engine searches for complementary templates and returns them as a **combination recommendation** with an aggregate confidence score.

### Step 6 — Gap Analysis and Confidence Reasoning

The engine compares detected entities against covered entities in the matched templates. Any uncovered entities become **gap flags**, and the confidence score is penalized proportionally. A plain-English reasoning string is generated explaining exactly why the score is what it is.

---

## Testing

```bash
python -m pytest tests/ -v
# 44 tests: 24 simulator tests + 20 MCP client tests
```

The test suite covers:
- Template matching accuracy across all policy categories
- Confidence score bounds and edge cases
- Intent and entity extraction correctness
- MCP client request/response handling (fully mocked — no network required)
- Gap analysis and combination logic

---

## Project Structure

```
Purview-Policy-Simulator/
├── app.py              # Flask application
├── simulator.py        # Simulation engine (TF-IDF + keyword matching)
├── mcp_client.py       # Microsoft Learn MCP Server client
├── knowledge_base.py   # 53+ policy templates and configurations
├── requirements.txt    # Dependencies
├── templates/
│   └── index.html      # Fluent Design web UI
└── tests/
    ├── test_simulator.py    # Simulator engine tests
    └── test_mcp_client.py   # MCP client tests (mocked)
```

---

## Configuration

The application reads the following environment variables at startup:

| Variable | Default | Description |
|---|---|---|
| `FLASK_DEBUG` | `0` | Set to `1` to enable Flask debug mode and auto-reload |
| `FLASK_HOST` | `127.0.0.1` | Interface to bind (use `0.0.0.0` to expose on all interfaces) |
| `FLASK_PORT` | `5000` | TCP port the application listens on |

Example:
```bash
FLASK_DEBUG=1 python app.py
```

---

## Contributing

Contributions are welcome! To add a new policy template:

1. Open `knowledge_base.py` and add an entry to the appropriate template list following the existing schema.
2. Add corresponding test cases in `tests/test_simulator.py`.
3. Run the full test suite (`python -m pytest tests/ -v`) to verify no regressions.
4. Open a pull request with a clear description of the template and its coverage area.

Please keep pull requests focused — one template category or feature per PR.

---

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

> **Disclaimer:** This tool is intended for learning, planning, and pre-deployment exploration only. It is not affiliated with or endorsed by Microsoft. Always validate policy configurations in a test tenant before deploying to production.

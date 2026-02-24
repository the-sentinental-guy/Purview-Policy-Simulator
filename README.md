# Microsoft Purview Policy Simulator

A self-contained web application that simulates Microsoft Purview data-protection and data-loss-prevention (DLP) policy scenarios — without needing to visit the Purview portal.

![Purview Policy Simulator UI](https://github.com/user-attachments/assets/62da92ce-d365-4b6c-9386-4374b7d4253f)

---

## Features

| # | Capability |
|---|-----------|
| 1 | **Natural-language input** — describe your policy requirement in plain English (with optional examples) |
| 2 | **Template matching** — the simulator checks its built-in knowledge base to determine whether a current Purview policy template covers your scenario |
| 3 | **Custom policy guidance** — when no template fits, the simulator recommends the most relevant custom configurations (keyword dictionaries, custom SITs, trainable classifiers, etc.) |
| 4 | **Confidence scoring** — every result includes a 0–100% confidence score indicating how certain the simulator is that the suggested configuration will meet your requirement |
| 5 | **Expected effects** — each matched template and custom configuration describes the exact effects you should expect after deploying the policy in the Purview portal |

---

## Knowledge Base Coverage

The simulator currently covers the following Purview policy areas:

- **DLP** — U.S. Financial (PCI-DSS), U.S. PII, HIPAA, GDPR, Source Code / IP, External Email Sharing, Endpoint DLP
- **Information Protection** — Confidential and Highly Confidential sensitivity labels
- **Data Lifecycle Management** — General retention and legal-hold policies
- **Communication Compliance** — Regulatory monitoring in Teams and Exchange
- **Insider Risk Management** — Data theft by departing users

---

## Quick Start

### Prerequisites

- Python 3.10 or later

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/the-sentinental-guy/Purview-Policy-Simulator.git
cd Purview-Policy-Simulator

# 2. (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the application
python app.py
```

Open your browser at **http://127.0.0.1:5000**.

---

## Usage

1. Type your data-protection requirement in the text area (or click a **Quick example** chip to load a pre-built scenario).
2. Click **Run Simulation**.
3. Review the results:
   - **Simulation Summary** — one-line verdict with overall confidence score and matched keywords.
   - **Matched Policy Templates** — expand each card to see workloads, sensitive information types, default actions, and expected deployment effects.
   - **Recommended Custom Configurations** — step-by-step implementation guidance when a custom policy is needed.

---

## Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

---

## Project Structure

```
.
├── app.py              # Flask web application (routes)
├── simulator.py        # Core simulation engine (matching + scoring)
├── knowledge_base.py   # Purview policy templates and custom configurations
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Single-page frontend (HTML + CSS + vanilla JS)
└── tests/
    └── test_simulator.py  # Pytest test suite
```

---

## Architecture

```
Browser  ──POST /api/simulate──►  Flask (app.py)
                                        │
                                   simulator.py
                                   (keyword scoring,
                                    confidence calc)
                                        │
                                  knowledge_base.py
                                  (POLICY_TEMPLATES,
                                   CUSTOM_CONFIGURATIONS)
```

The simulator performs **keyword-based matching** with word-boundary awareness and phrase detection. Confidence is derived from the template's base confidence value, adjusted up or down based on the ratio of keywords matched to total keywords in the template. No external API calls are required — the tool runs entirely offline.

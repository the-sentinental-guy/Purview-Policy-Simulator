# Microsoft Purview Policy Simulator

[![CI](https://github.com/the-sentinental-guy/Purview-Policy-Simulator/actions/workflows/ci.yml/badge.svg)](https://github.com/the-sentinental-guy/Purview-Policy-Simulator/actions/workflows/ci.yml)
[![Docker](https://github.com/the-sentinental-guy/Purview-Policy-Simulator/actions/workflows/deploy.yml/badge.svg)](https://github.com/the-sentinental-guy/Purview-Policy-Simulator/actions/workflows/deploy.yml)

A **public web tool** that lets you simulate how Microsoft Purview data-access policies evaluate access requests — no local Python setup required.

| | |
|---|---|
| **Backend** | Python 3.12 · FastAPI · Pydantic v2 |
| **Frontend** | Vanilla HTML / CSS / JS (no build step) |
| **Container** | Docker multi-stage build · ~170 MB image |
| **Cloud** | Azure Container Apps (Bicep template included) |
| **CI/CD** | GitHub Actions (test + lint on PRs; Docker push + Azure deploy on `main`) |

---

## ✨ Features

- **Policy evaluation engine** — explicit Deny wins, default deny, wildcard subjects/resources, parent-scope inheritance
- **REST API** (`POST /api/simulate`) with OpenAPI/Swagger documentation
- **Interactive web UI** — paste JSON, click Run, see which policies matched and why
- **Rate limiting** — 60 requests / minute per IP (configurable)
- **CORS** — configurable per-origin allow-list
- **Healthcheck** endpoint — `/api/health` for load balancers and probes
- **Production Dockerfile** — multi-stage, non-root user, HEALTHCHECK directive

---

## 🚀 Quick Start (Docker)

> Run the simulator locally with a single command — no Python installation required.

```bash
# Option 1: Docker Compose (recommended)
docker compose up

# Option 2: Docker directly
docker build -t purview-simulator .
docker run -p 8000:8000 purview-simulator
```

Then open **http://localhost:8000** in your browser.

The OpenAPI docs are available at **http://localhost:8000/api/docs**.

---

## 🧪 Local Development (without Docker)

### Prerequisites

- Python 3.11 or 3.12

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/the-sentinental-guy/Purview-Policy-Simulator.git
cd Purview-Policy-Simulator

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate       # Linux / macOS
# .venv\Scripts\activate        # Windows

# 3. Install dependencies
pip install -r requirements-dev.txt

# 4. Run the development server
uvicorn app.main:app --reload --port 8000
```

Open **http://localhost:8000**.

### Run tests

```bash
pytest
```

---

## 🔌 API Reference

### `GET /api/health`

Liveness / readiness probe.

```json
{ "status": "ok", "version": "1.0.0" }
```

### `POST /api/simulate`

Evaluate a set of Purview policies against a subject / resource / action.

**Request body** (JSON):

```json
{
  "subject": {
    "id": "alice@contoso.com",
    "subject_type": "User",
    "display_name": "Alice"
  },
  "resource": {
    "resource_path": "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<account>",
    "resource_type": "AzureStorage",
    "collection": "Finance"
  },
  "action": "Microsoft.Purview/accounts/data/read",
  "policies": [
    {
      "id": "pol-001",
      "name": "Finance Read Access",
      "enabled": true,
      "statements": [
        {
          "effect": "Allow",
          "actions": ["Microsoft.Purview/accounts/data/read"],
          "subjects": [{ "id": "alice@contoso.com", "subject_type": "User" }],
          "resources": [{ "resource_path": "*", "resource_type": "AzureStorage" }]
        }
      ]
    }
  ]
}
```

**Response** (JSON):

```json
{
  "access_granted": true,
  "effective_effect": "Allow",
  "matched_policies": [
    {
      "policy_id": "pol-001",
      "policy_name": "Finance Read Access",
      "statement_index": 0,
      "effect": "Allow"
    }
  ],
  "evaluation_notes": [
    "Policy 'Finance Read Access' statement[0] matched (effect: Allow).",
    "All matching statements are Allow – access granted."
  ]
}
```

**Supported actions:**

| Value | Description |
|---|---|
| `Microsoft.Purview/accounts/data/read` | Read data assets |
| `Microsoft.Purview/accounts/data/modify` | Modify data assets |
| `Microsoft.Purview/accounts/scan/read` | Read scan results |
| `Microsoft.Purview/accounts/devops/read` | DevOps read |
| `Microsoft.Purview/accounts/devops/modify` | DevOps modify |

**Evaluation rules:**

1. **Explicit Deny wins** — a single `Deny` statement overrides all `Allow` statements.
2. **Default deny** — if no policy matches, access is denied.
3. **Wildcard subject** — `"id": "*"` matches any identity.
4. **Wildcard resource** — `"resource_path": "*"` matches any resource path.
5. **Scope inheritance** — a policy on `/subscriptions/sub1` also covers `/subscriptions/sub1/resourceGroups/rg/...`.

Full interactive docs: **`/api/docs`** (Swagger UI) or **`/api/redoc`** (ReDoc).

---

## ☁️ Cloud Deployment

### Azure Container Apps (Bicep)

A Bicep template is provided in `infra/azure/`.

#### Prerequisites

- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed and logged in
- An Azure subscription

#### One-time setup

```bash
# 1. Create a resource group
az group create --name rg-purview-simulator --location eastus

# 2. Deploy the infrastructure
az deployment group create \
  --resource-group rg-purview-simulator \
  --template-file infra/azure/main.bicep \
  --parameters infra/azure/parameters.json \
  --parameters containerImage=ghcr.io/the-sentinental-guy/purview-policy-simulator:main

# 3. Get the public URL
az deployment group show \
  --resource-group rg-purview-simulator \
  --name main \
  --query properties.outputs.appUrl.value -o tsv
```

The template provisions:
- **Log Analytics workspace** (30-day retention)
- **Azure Container App Environment**
- **Azure Container App** with HTTP ingress, health probes, and autoscaling (0–3 replicas)

#### Environment variables

| Variable | Default | Description |
|---|---|---|
| `CORS_ORIGINS` | `*` | Comma-separated list of allowed CORS origins |
| `PORT` | `8000` | Port the app listens on (set automatically by ACA) |

### GitHub Actions (automatic deployment)

Configure these **repository secrets** to enable automatic deployment to Azure on every push to `main`:

| Secret | Description |
|---|---|
| `AZURE_CREDENTIALS` | JSON output of `az ad sp create-for-rbac --sdk-auth` |
| `AZURE_RESOURCE_GROUP` | Name of the target resource group |
| `AZURE_CONTAINER_APP_NAME` | Name of the Azure Container App |

The Docker image is always pushed to **GitHub Container Registry** (`ghcr.io`) on every push to `main`, regardless of Azure secrets being configured.

---

## 🏗️ Project Structure

```
├── app/
│   ├── main.py                  # FastAPI application
│   ├── simulator/
│   │   ├── models.py            # Pydantic data models
│   │   └── policy_evaluator.py  # Policy evaluation engine
│   └── static/                  # Frontend (HTML/CSS/JS)
│       ├── index.html
│       ├── css/styles.css
│       └── js/app.js
├── tests/
│   ├── test_policy_evaluator.py # Unit tests for the engine
│   └── test_api.py              # Integration tests for the API
├── infra/
│   └── azure/
│       ├── main.bicep           # Azure Container Apps Bicep template
│       └── parameters.json      # Default deployment parameters
├── .github/
│   └── workflows/
│       ├── ci.yml               # CI: test on Python 3.11 + 3.12
│       └── deploy.yml           # CD: Docker build/push + Azure deploy
├── Dockerfile                   # Multi-stage production image
├── docker-compose.yaml          # One-line local deployment
├── requirements.txt             # Runtime dependencies
└── requirements-dev.txt         # Dev/test dependencies
```

---

## 🔒 Security

- Container runs as a **non-root user** (`appuser`)
- **Rate limiting**: 60 req/min per IP (global default via slowapi)
- **CORS**: configurable allow-list via `CORS_ORIGINS` environment variable
- All secrets are passed as environment variables (never baked into the image)
- Dependency versions are pinned in `requirements.txt`

---

## 📄 License

This project is provided as-is for educational and demonstration purposes. Not affiliated with Microsoft Corporation.

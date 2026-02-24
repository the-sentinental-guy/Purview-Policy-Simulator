# Purview Policy Simulator

A command-line tool that simulates Microsoft Purview policy scenarios. Describe your data protection or data loss prevention requirement in plain English and the simulator will tell you whether it can be achieved with an existing policy template or if a custom policy is needed.

## Features

- **Natural language input** – describe your policy requirement in plain English, with optional examples.
- **Template matching** – the simulator checks its knowledge base of built-in Purview policy templates and returns the best matches.
- **Custom policy guidance** – when no template fully covers the scenario, the simulator recommends specific configurations and options for a custom policy.
- **Confidence scoring** – every recommendation includes a confidence level indicating how well it matches the requirement.
- **Expected effects** – each recommendation lists the effects the user should expect after deploying the policy in the Purview portal.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/the-sentinental-guy/Purview-Policy-Simulator.git
cd Purview-Policy-Simulator

# (Optional) create a virtual environment
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the simulator with a requirement
python -m purview_simulator "Prevent credit card numbers from being shared via email"

# Or start the interactive mode
python -m purview_simulator
```

## Usage

### One-shot mode

Pass your requirement as a command-line argument:

```bash
python -m purview_simulator "Block health records from being shared externally in Teams"
```

### Interactive mode

Run without arguments to enter an interactive prompt where you can test multiple scenarios:

```bash
python -m purview_simulator
```

Type `quit` or `exit` to leave the interactive mode.

## Running Tests

```bash
pip install -r requirements.txt
python -m pytest tests/ -v
```

## Project Structure

```
purview_simulator/
├── __init__.py          # Package metadata
├── __main__.py          # Entry point for `python -m purview_simulator`
├── cli.py               # Command-line interface and result display
├── engine.py            # Simulation engine (parsing, scoring, recommendations)
└── knowledge_base.py    # Purview policy templates, info types and actions
tests/
├── test_engine.py       # Tests for the simulation engine
└── test_knowledge_base.py  # Tests for knowledge base integrity
```

## How It Works

1. **Parsing** – the engine scans your natural-language requirement for keywords that map to sensitive information types (e.g. credit card, SSN), workload locations (e.g. Exchange, Teams, devices), and desired actions (e.g. block, encrypt, audit).
2. **Scoring** – each built-in Purview policy template is scored against your requirement based on overlapping info types, locations, actions, and direct template hints.
3. **Recommendation** – templates that score above the confidence threshold are presented as recommendations. If no template crosses the threshold, a custom policy configuration is synthesised from the detected elements.
4. **Expected effects** – every recommendation includes a list of real-world effects the user should expect when the policy is deployed.

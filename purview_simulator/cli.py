"""
Command-line interface for the Purview Policy Simulator.

Run with:
    python -m purview_simulator.cli
"""

from __future__ import annotations

import sys
import textwrap

from purview_simulator.engine import SimulationResult, run_simulation

# ANSI colour helpers (disabled when stdout is not a terminal)
_USE_COLOUR = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

def _c(code: str, text: str) -> str:
    if _USE_COLOUR:
        return f"\033[{code}m{text}\033[0m"
    return text

def _bold(t: str) -> str:
    return _c("1", t)

def _green(t: str) -> str:
    return _c("32", t)

def _yellow(t: str) -> str:
    return _c("33", t)

def _red(t: str) -> str:
    return _c("31", t)

def _cyan(t: str) -> str:
    return _c("36", t)


def _confidence_bar(confidence: float) -> str:
    """Return a text-based confidence bar."""
    filled = int(confidence * 20)
    bar = "█" * filled + "░" * (20 - filled)
    pct = f"{confidence * 100:.0f}%"
    if confidence >= 0.75:
        return _green(f"[{bar}] {pct}")
    if confidence >= 0.50:
        return _yellow(f"[{bar}] {pct}")
    return _red(f"[{bar}] {pct}")


def _wrap(text: str, indent: int = 4, width: int = 80) -> str:
    return textwrap.fill(text, width=width, initial_indent=" " * indent,
                         subsequent_indent=" " * indent)


def display_result(result: SimulationResult) -> None:
    """Pretty-print a simulation result to stdout."""
    print()
    print(_bold("=" * 70))
    print(_bold("  PURVIEW POLICY SIMULATOR – RESULTS"))
    print(_bold("=" * 70))
    print()

    print(_bold("Requirement:"))
    print(_wrap(result.original_requirement, indent=2))
    print()

    # Detected elements
    parsed = result.parsed
    if parsed.detected_info_types or parsed.detected_locations or parsed.detected_actions:
        print(_bold("Detected elements in your requirement:"))
        if parsed.detected_info_types:
            from purview_simulator.knowledge_base import SENSITIVE_INFO_TYPES
            names = [SENSITIVE_INFO_TYPES[s]["name"] for s in parsed.detected_info_types
                     if s in SENSITIVE_INFO_TYPES]
            print(f"  Sensitive info types : {', '.join(names)}")
        if parsed.detected_locations:
            from purview_simulator.knowledge_base import POLICY_LOCATIONS
            names = [POLICY_LOCATIONS[l]["name"] for l in parsed.detected_locations
                     if l in POLICY_LOCATIONS]
            print(f"  Locations/workloads  : {', '.join(names)}")
        if parsed.detected_actions:
            from purview_simulator.knowledge_base import POLICY_ACTIONS
            names = [POLICY_ACTIONS[a]["name"] for a in parsed.detected_actions
                     if a in POLICY_ACTIONS]
            print(f"  Desired actions      : {', '.join(names)}")
        print()

    # Template achievability verdict
    if result.achievable_with_template:
        print(_green(_bold("✔ This scenario CAN be achieved using an existing policy template.")))
    else:
        print(_yellow(_bold(
            "⚠ No single template fully covers this scenario. "
            "A custom policy is recommended."
        )))
    print()

    # Recommendations
    for idx, rec in enumerate(result.recommendations, 1):
        kind = _cyan("[TEMPLATE]") if rec.policy_type == "template" else _yellow("[CUSTOM]")
        print(_bold(f"  Recommendation #{idx} {kind}"))
        print(f"    Name       : {rec.policy_name}")
        print(f"    Confidence : {_confidence_bar(rec.confidence)}")
        print(f"    Description: {rec.description}")
        print()

        if rec.configurations:
            print(_bold("    Configurations:"))
            for cfg in rec.configurations:
                print(f"      • {cfg}")
            print()

        if rec.expected_effects:
            print(_bold("    Expected Effects:"))
            for eff in rec.expected_effects:
                print(f"      → {eff}")
            print()

    # Custom config suggestions (only when template is not sufficient)
    if result.custom_config_suggestions:
        print(_bold("-" * 70))
        print(_bold("  Suggested Custom Configuration Steps:"))
        for i, s in enumerate(result.custom_config_suggestions, 1):
            print(f"    {i}. {s}")
        print()

    print(_bold("=" * 70))
    print()


def interactive_loop() -> None:
    """Run an interactive prompt loop."""
    print()
    print(_bold("=" * 70))
    print(_bold("  Welcome to the Purview Policy Simulator"))
    print(_bold("=" * 70))
    print()
    print("  Describe your Microsoft Purview policy requirement in plain English.")
    print("  You may include examples or specific scenarios.")
    print("  Type 'quit' or 'exit' to leave.\n")

    while True:
        try:
            user_input = input(_bold("Your requirement> ")).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        result = run_simulation(user_input)
        display_result(result)


def main() -> None:
    """Entry point for the CLI."""
    if len(sys.argv) > 1:
        requirement = " ".join(sys.argv[1:])
        result = run_simulation(requirement)
        display_result(result)
    else:
        interactive_loop()


if __name__ == "__main__":
    main()

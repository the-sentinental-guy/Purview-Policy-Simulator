"""
Simulation engine for the Purview Policy Simulator.

This module provides the core logic that:
1. Parses natural-language policy requirements.
2. Matches requirements against known Purview policy templates.
3. Recommends custom configurations when no template fully matches.
4. Computes a confidence score for each recommendation.
5. Presents expected effects for every recommended configuration.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional

from purview_simulator.knowledge_base import (
    CUSTOM_POLICY_OPTIONS,
    POLICY_ACTIONS,
    POLICY_LOCATIONS,
    POLICY_TEMPLATES,
    SENSITIVE_INFO_TYPES,
)


@dataclass
class ParsedRequirement:
    """Structured representation of a user's natural-language requirement."""

    raw_text: str
    detected_info_types: List[str] = field(default_factory=list)
    detected_locations: List[str] = field(default_factory=list)
    detected_actions: List[str] = field(default_factory=list)
    detected_template_hints: List[str] = field(default_factory=list)


@dataclass
class PolicyRecommendation:
    """A single policy recommendation returned by the simulator."""

    policy_name: str
    policy_type: str  # "template" or "custom"
    description: str
    confidence: float  # 0.0 – 1.0
    matched_info_types: List[str] = field(default_factory=list)
    matched_locations: List[str] = field(default_factory=list)
    matched_actions: List[str] = field(default_factory=list)
    configurations: List[str] = field(default_factory=list)
    expected_effects: List[str] = field(default_factory=list)


@dataclass
class SimulationResult:
    """Complete result of a simulation run."""

    original_requirement: str
    parsed: ParsedRequirement
    achievable_with_template: bool
    recommendations: List[PolicyRecommendation] = field(default_factory=list)
    custom_config_suggestions: List[str] = field(default_factory=list)


def _normalize(text: str) -> str:
    """Lower-case and collapse whitespace."""
    return re.sub(r"\s+", " ", text.lower().strip())


def _keyword_in_text(keyword: str, text: str) -> bool:
    """Check if *keyword* appears in *text* as a whole-word match."""
    pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"
    return re.search(pattern, text) is not None


def parse_requirement(text: str) -> ParsedRequirement:
    """Parse a natural-language requirement into structured data.

    Scans the input for keywords that correspond to sensitive information
    types, policy locations, and policy actions defined in the knowledge base.
    """
    norm = _normalize(text)
    parsed = ParsedRequirement(raw_text=text)

    for sit_id, sit in SENSITIVE_INFO_TYPES.items():
        for kw in sit["keywords"]:
            if _keyword_in_text(kw, norm):
                if sit_id not in parsed.detected_info_types:
                    parsed.detected_info_types.append(sit_id)
                break

    for loc_id, loc in POLICY_LOCATIONS.items():
        for kw in loc["keywords"]:
            if _keyword_in_text(kw, norm):
                if loc_id not in parsed.detected_locations:
                    parsed.detected_locations.append(loc_id)
                break

    for act_id, act in POLICY_ACTIONS.items():
        for kw in act["keywords"]:
            if _keyword_in_text(kw, norm):
                if act_id not in parsed.detected_actions:
                    parsed.detected_actions.append(act_id)
                break

    for tmpl in POLICY_TEMPLATES:
        for kw in tmpl["keywords"]:
            if _keyword_in_text(kw, norm):
                if tmpl["id"] not in parsed.detected_template_hints:
                    parsed.detected_template_hints.append(tmpl["id"])
                break

    return parsed


def _score_template(parsed: ParsedRequirement, template: dict) -> float:
    """Compute a match score (0.0–1.0) between parsed requirement and a template."""
    score = 0.0
    total_weight = 0.0

    # Template hint match (high weight)
    if parsed.detected_template_hints:
        total_weight += 3.0
        if template["id"] in parsed.detected_template_hints:
            score += 3.0

    # Sensitive info type overlap
    if parsed.detected_info_types:
        total_weight += 3.0
        overlap = set(parsed.detected_info_types) & set(template["sensitive_info_types"])
        if parsed.detected_info_types:
            score += 3.0 * len(overlap) / len(parsed.detected_info_types)

    # Location overlap
    if parsed.detected_locations:
        total_weight += 2.0
        overlap = set(parsed.detected_locations) & set(template["default_locations"])
        if parsed.detected_locations:
            score += 2.0 * len(overlap) / len(parsed.detected_locations)

    # Action overlap
    if parsed.detected_actions:
        total_weight += 2.0
        overlap = set(parsed.detected_actions) & set(template["default_actions"])
        if parsed.detected_actions:
            score += 2.0 * len(overlap) / len(parsed.detected_actions)

    if total_weight == 0:
        return 0.0
    return round(score / total_weight, 2)


def _build_custom_config(parsed: ParsedRequirement) -> List[str]:
    """Build suggested custom configuration options from parsed requirement."""
    suggestions: List[str] = []

    if parsed.detected_info_types:
        cond = CUSTOM_POLICY_OPTIONS["conditions"]["content_contains"]
        sit_names = [
            SENSITIVE_INFO_TYPES[s]["name"]
            for s in parsed.detected_info_types
            if s in SENSITIVE_INFO_TYPES
        ]
        suggestions.append(
            f"{cond['name']}: Configure detection for {', '.join(sit_names)}."
        )

    external_keywords = {"external", "outside", "share externally", "leak"}
    if any(kw in _normalize(parsed.raw_text) for kw in external_keywords):
        cond = CUSTOM_POLICY_OPTIONS["conditions"]["content_shared_external"]
        suggestions.append(f"{cond['name']}: {cond['description']}")

    if parsed.detected_actions:
        for act_id in parsed.detected_actions:
            if act_id in POLICY_ACTIONS:
                act = POLICY_ACTIONS[act_id]
                suggestions.append(f"Action – {act['name']}: {act['description']}")

    override_keywords = {"override", "justification", "allow exception"}
    if any(kw in _normalize(parsed.raw_text) for kw in override_keywords):
        opt = CUSTOM_POLICY_OPTIONS["user_overrides"]["require_justification"]
        suggestions.append(f"User Override – {opt['name']}: {opt['description']}")

    alert_keywords = {"alert", "incident", "report", "notify"}
    if any(kw in _normalize(parsed.raw_text) for kw in alert_keywords):
        opt = CUSTOM_POLICY_OPTIONS["incident_reports"]["severity_high"]
        suggestions.append(f"Incident Report – {opt['name']}: {opt['description']}")

    return suggestions


def _recommendation_from_template(template: dict, score: float,
                                  parsed: ParsedRequirement) -> PolicyRecommendation:
    """Create a PolicyRecommendation from a template match."""
    matched_info = [s for s in parsed.detected_info_types
                    if s in template["sensitive_info_types"]]
    matched_locs = [l for l in parsed.detected_locations
                    if l in template["default_locations"]]
    matched_acts = [a for a in parsed.detected_actions
                    if a in template["default_actions"]]

    configs = []
    for sit_id in template["sensitive_info_types"]:
        sit = SENSITIVE_INFO_TYPES.get(sit_id)
        if sit:
            configs.append(f"Detect: {sit['name']}")
    for loc_id in template["default_locations"]:
        loc = POLICY_LOCATIONS.get(loc_id)
        if loc:
            configs.append(f"Location: {loc['name']}")
    for act_id in template["default_actions"]:
        act = POLICY_ACTIONS.get(act_id)
        if act:
            configs.append(f"Action: {act['name']}")

    return PolicyRecommendation(
        policy_name=template["name"],
        policy_type="template",
        description=template["description"],
        confidence=score,
        matched_info_types=matched_info,
        matched_locations=matched_locs,
        matched_actions=matched_acts,
        configurations=configs,
        expected_effects=list(template["expected_effects"]),
    )


def _custom_recommendation(parsed: ParsedRequirement,
                           best_template_score: float) -> Optional[PolicyRecommendation]:
    """Build a custom policy recommendation when no template is a strong match."""
    configs = _build_custom_config(parsed)
    if not configs:
        return None

    effects: List[str] = []
    if parsed.detected_info_types:
        names = [SENSITIVE_INFO_TYPES[s]["name"] for s in parsed.detected_info_types
                 if s in SENSITIVE_INFO_TYPES]
        effects.append(f"Content containing {', '.join(names)} will be detected.")
    if parsed.detected_locations:
        loc_names = [POLICY_LOCATIONS[l]["name"] for l in parsed.detected_locations
                     if l in POLICY_LOCATIONS]
        effects.append(f"Policy will be enforced across: {', '.join(loc_names)}.")
    for act_id in parsed.detected_actions:
        act = POLICY_ACTIONS.get(act_id)
        if act:
            effects.append(f"{act['name']}: {act['description']}")
    if not effects:
        effects.append("Policy will monitor and protect content based on configured rules.")

    confidence = round(min(0.85, 0.4 + 0.1 * len(configs)), 2)

    return PolicyRecommendation(
        policy_name="Custom Policy Configuration",
        policy_type="custom",
        description="A custom policy tailored to your specific requirements. This policy "
                    "combines multiple conditions and actions to achieve your goal.",
        confidence=confidence,
        matched_info_types=list(parsed.detected_info_types),
        matched_locations=list(parsed.detected_locations),
        matched_actions=list(parsed.detected_actions),
        configurations=configs,
        expected_effects=effects,
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

TEMPLATE_MATCH_THRESHOLD = 0.60


def run_simulation(requirement_text: str) -> SimulationResult:
    """Run a full simulation for a natural-language policy requirement.

    Returns a ``SimulationResult`` that includes:
    * Whether the scenario is achievable with an existing template.
    * Ranked policy recommendations (template and/or custom).
    * Confidence scores and expected effects for each recommendation.
    """
    parsed = parse_requirement(requirement_text)

    scored_templates = []
    for tmpl in POLICY_TEMPLATES:
        sc = _score_template(parsed, tmpl)
        if sc > 0:
            scored_templates.append((tmpl, sc))

    scored_templates.sort(key=lambda x: x[1], reverse=True)

    recommendations: List[PolicyRecommendation] = []
    best_score = scored_templates[0][1] if scored_templates else 0.0

    achievable = best_score >= TEMPLATE_MATCH_THRESHOLD

    for tmpl, sc in scored_templates[:3]:
        recommendations.append(_recommendation_from_template(tmpl, sc, parsed))

    custom_suggestions: List[str] = []
    if not achievable:
        custom_rec = _custom_recommendation(parsed, best_score)
        if custom_rec:
            recommendations.append(custom_rec)
            custom_suggestions = list(custom_rec.configurations)

    return SimulationResult(
        original_requirement=requirement_text,
        parsed=parsed,
        achievable_with_template=achievable,
        recommendations=recommendations,
        custom_config_suggestions=custom_suggestions,
    )

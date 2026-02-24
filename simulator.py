"""
Purview Policy Simulator Engine
Analyzes natural language requirements and maps them to Purview policy templates and configurations.
"""

from __future__ import annotations

import re
from typing import Any

from knowledge_base import CUSTOM_CONFIGURATIONS, POLICY_TEMPLATES

# Keywords that trigger specific custom configuration recommendations
_KW_KEYWORD_DICT = ["code", "proprietary", "internal", "specific", "custom"]
_KW_TRAINABLE = ["document", "contract", "report", "complex", "legal", "hr", "employee"]
_KW_ADAPTIVE = ["risk", "insider", "departing", "employee", "threat"]


def _normalize(text: str) -> str:
    """Lowercase and strip punctuation for consistent matching."""
    return re.sub(r"[^\w\s]", " ", text.lower())


def _keyword_score(text: str, keywords: list[str]) -> tuple[int, list[str]]:
    """
    Return the number of keyword matches and the list of matched keywords.
    Handles multi-word keywords by checking phrase presence.
    """
    normalized = _normalize(text)
    matched = []
    for kw in keywords:
        kw_lower = kw.lower()
        # Check for exact phrase match (with word boundaries for single words)
        if " " in kw_lower:
            if kw_lower in normalized:
                matched.append(kw)
        else:
            if re.search(rf"\b{re.escape(kw_lower)}\b", normalized):
                matched.append(kw)
    return len(matched), matched


def _calculate_confidence(base_confidence: int, match_count: int, total_keywords: int) -> int:
    """
    Adjust the template's base confidence based on match ratio.
    A higher keyword match ratio slightly boosts or reduces confidence.
    """
    if total_keywords == 0:
        return base_confidence
    ratio = match_count / total_keywords
    # Scale: 0.0 ratio → -15 pts, 0.5 → 0 pts, 1.0 → +5 pts
    adjustment = int((ratio - 0.3) * 20)
    return max(10, min(99, base_confidence + adjustment))


def _build_custom_recommendation(
    matched_templates: list[dict[str, Any]], user_input: str
) -> list[dict[str, Any]]:
    """
    When no exact template fits, build a custom policy recommendation
    by combining the most relevant configurations.
    """
    recommendations = []

    # Always suggest Custom SIT if there's no strong template match
    sit_config = next(c for c in CUSTOM_CONFIGURATIONS if c["id"] == "custom_sit")
    recommendations.append(sit_config)

    # Suggest keyword dictionary for specific terminology
    normalized = _normalize(user_input)
    if any(w in normalized for w in _KW_KEYWORD_DICT):
        kw_config = next(c for c in CUSTOM_CONFIGURATIONS if c["id"] == "custom_keyword_dict")
        recommendations.append(kw_config)

    # Suggest trainable classifier for complex content scenarios
    if any(w in normalized for w in _KW_TRAINABLE):
        tc_config = next(c for c in CUSTOM_CONFIGURATIONS if c["id"] == "trainable_classifier")
        recommendations.append(tc_config)

    # Suggest adaptive protection for insider/risk scenarios
    if any(w in normalized for w in _KW_ADAPTIVE):
        ap_config = next(c for c in CUSTOM_CONFIGURATIONS if c["id"] == "adaptive_protection")
        recommendations.append(ap_config)

    # Always offer custom policy tips as a UX enhancement
    pt_config = next(c for c in CUSTOM_CONFIGURATIONS if c["id"] == "policy_tips_customization")
    recommendations.append(pt_config)

    return recommendations


def simulate(user_input: str) -> dict[str, Any]:
    """
    Main simulation function.

    Parameters
    ----------
    user_input : str
        The user's natural language description of their policy requirement.

    Returns
    -------
    dict with keys:
        - matched_templates : list of matched policy templates with scores
        - requires_custom   : bool
        - custom_configs    : list of recommended custom configurations (if needed)
        - overall_confidence: int (0-100)
        - summary           : str human-readable summary
        - matched_keywords  : list of keywords matched across all templates
    """
    if not user_input or not user_input.strip():
        return {
            "matched_templates": [],
            "requires_custom": False,
            "custom_configs": [],
            "overall_confidence": 0,
            "summary": "Please describe your policy requirement to begin the simulation.",
            "matched_keywords": [],
        }

    scored_templates = []
    all_matched_keywords: set[str] = set()

    for template in POLICY_TEMPLATES:
        score, matched_kws = _keyword_score(user_input, template["keywords"])
        if score > 0:
            confidence = _calculate_confidence(template["confidence"], score, len(template["keywords"]))
            scored_templates.append(
                {
                    **template,
                    "match_score": score,
                    "confidence": confidence,
                    "matched_keywords": matched_kws,
                }
            )
            all_matched_keywords.update(matched_kws)

    # Sort by match_score descending, then by confidence descending
    scored_templates.sort(key=lambda t: (t["match_score"], t["confidence"]), reverse=True)

    # Keep top 4 results
    top_templates = scored_templates[:4]

    # Determine if template is sufficient or custom policy is needed
    requires_custom = False
    custom_configs: list[dict[str, Any]] = []

    if not top_templates:
        requires_custom = True
        custom_configs = _build_custom_recommendation([], user_input)
        overall_confidence = 35
        summary = (
            "No direct template match found for your requirement. "
            "A custom policy configuration is recommended. "
            "The configurations below provide a starting point based on your description."
        )
    elif top_templates[0]["match_score"] == 1 and top_templates[0]["confidence"] < 80:
        # Weak single-keyword match
        requires_custom = True
        custom_configs = _build_custom_recommendation(top_templates, user_input)
        overall_confidence = top_templates[0]["confidence"]
        summary = (
            f"Your requirement partially matches the '{top_templates[0]['name']}' template, "
            "but a custom policy configuration would better address your specific needs. "
            "Review the custom configuration options below."
        )
    elif top_templates[0]["template_available"] and top_templates[0]["confidence"] >= 80:
        requires_custom = False
        overall_confidence = top_templates[0]["confidence"]
        summary = (
            f"Your requirement can be addressed using the built-in "
            f"'{top_templates[0]['name']}' policy template with "
            f"{overall_confidence}% confidence. "
            "Review the matched templates and their expected effects below."
        )
    else:
        requires_custom = True
        custom_configs = _build_custom_recommendation(top_templates, user_input)
        overall_confidence = top_templates[0]["confidence"]
        summary = (
            f"Your requirement most closely matches '{top_templates[0]['name']}', "
            "but requires a custom policy configuration for full coverage. "
            "The recommended configurations are listed below."
        )

    return {
        "matched_templates": top_templates,
        "requires_custom": requires_custom,
        "custom_configs": custom_configs,
        "overall_confidence": overall_confidence,
        "summary": summary,
        "matched_keywords": sorted(all_matched_keywords),
    }

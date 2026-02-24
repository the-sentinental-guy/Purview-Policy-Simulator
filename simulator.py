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

_TFIDF_THRESHOLD = 0.05       # Minimum TF-IDF cosine similarity to include a template
_TFIDF_BOOST_MULTIPLIER = 15  # Confidence boost = int(tfidf_score * _TFIDF_BOOST_MULTIPLIER)
_MAX_SEARCH_KEYWORDS = 6      # Max keywords included in the fallback doc_search_query

# TF-IDF support (optional; falls back gracefully if scikit-learn is not installed)
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity as _cosine_similarity
    _TFIDF_AVAILABLE = True
except ImportError:
    _TFIDF_AVAILABLE = False

# Build TF-IDF corpus once at import time (no-op when sklearn is unavailable)
_TFIDF_VECTORIZER: Any = None
_TFIDF_MATRIX: Any = None

def _build_tfidf_index() -> None:
    """Pre-compute the TF-IDF matrix for all policy template descriptions."""
    global _TFIDF_VECTORIZER, _TFIDF_MATRIX
    if not _TFIDF_AVAILABLE:
        return
    corpus = [
        t["description"] + " " + " ".join(t["keywords"])
        for t in POLICY_TEMPLATES
    ]
    _TFIDF_VECTORIZER = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    _TFIDF_MATRIX = _TFIDF_VECTORIZER.fit_transform(corpus)

_build_tfidf_index()


def _tfidf_scores(user_input: str) -> list[float]:
    """Return cosine similarity scores (0-1) between user_input and each template."""
    if not _TFIDF_AVAILABLE or _TFIDF_VECTORIZER is None or _TFIDF_MATRIX is None:
        return [0.0] * len(POLICY_TEMPLATES)
    user_vec = _TFIDF_VECTORIZER.transform([user_input])
    scores = _cosine_similarity(user_vec, _TFIDF_MATRIX)[0]
    return list(scores)


# Intent and entity vocabularies
_INTENT_WORDS = [
    "protect", "prevent", "detect", "monitor", "retain", "classify",
    "investigate", "block", "encrypt", "audit",
]

_ENTITY_DATA_TYPES = [
    "credit card", "SSN", "passport", "PHI", "PII", "HIPAA",
    "source code", "financial", "health", "medical", "personal data",
    "trade secret", "salary", "email",
]
_ENTITY_WORKLOADS = [
    "Exchange", "Teams", "SharePoint", "OneDrive", "endpoint",
    "Windows", "device", "USB", "browser", "print",
]
_ENTITY_FRAMEWORKS = [
    "PCI", "GDPR", "HIPAA", "SOX", "CCPA", "LGPD", "PIPEDA",
    "DPA", "APPI", "FINRA", "SEC",
]
_ENTITY_RISK_SCENARIOS = [
    "departing", "insider", "exfiltration", "leakage", "theft",
    "disgruntled", "termination",
]

# Maps entity workload names to canonical Purview workload strings (lowercase)
_WORKLOAD_CANONICAL_MAP = {
    "Teams": "microsoft teams",
    "Exchange": "exchange online",
    "SharePoint": "sharepoint online",
    "OneDrive": "onedrive for business",
    "endpoint": "endpoints",
    "Windows": "windows 10/11 endpoints",
    "USB": "endpoints",
    "browser": "endpoints",
    "device": "endpoints",
}


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


def _extract_intent(text: str) -> list[str]:
    """Return intent words found in the normalized text."""
    normalized = _normalize(text)
    return [w for w in _INTENT_WORDS if re.search(rf"\b{re.escape(w)}\b", normalized)]


def _extract_entities(text: str) -> dict[str, list[str]]:
    """Extract named entities (data types, workloads, frameworks, risk scenarios) from text."""
    normalized = _normalize(text)

    def _match(vocab: list[str]) -> list[str]:
        found = []
        for term in vocab:
            t = term.lower()
            if " " in t:
                if t in normalized:
                    found.append(term)
            else:
                if re.search(rf"\b{re.escape(t)}\b", normalized):
                    found.append(term)
        return found

    return {
        "data_types": _match(_ENTITY_DATA_TYPES),
        "workloads": _match(_ENTITY_WORKLOADS),
        "frameworks": _match(_ENTITY_FRAMEWORKS),
        "risk_scenarios": _match(_ENTITY_RISK_SCENARIOS),
    }


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
        - matched_templates   : list of matched policy templates with scores
        - requires_custom     : bool
        - custom_configs      : list of recommended custom configurations (if needed)
        - overall_confidence  : int (0-100)
        - summary             : str human-readable summary
        - matched_keywords    : list of keywords matched across all templates
        - intents             : list of detected intent words
        - entities            : extracted entity dict
        - coverage_gaps       : list of gap descriptions (populated when requires_custom)
        - confidence_reasoning: explanation of the confidence score
        - combination_note    : note when multiple templates complement each other
        - doc_search_query    : suggested MCP documentation search query
    """
    if not user_input or not user_input.strip():
        return {
            "matched_templates": [],
            "requires_custom": False,
            "custom_configs": [],
            "overall_confidence": 0,
            "summary": "Please describe your policy requirement to begin the simulation.",
            "matched_keywords": [],
            "intents": [],
            "entities": {"data_types": [], "workloads": [], "frameworks": [], "risk_scenarios": []},
            "coverage_gaps": [],
            "confidence_reasoning": "No input provided.",
            "combination_note": "",
            "doc_search_query": "",
        }

    intents = _extract_intent(user_input)
    entities = _extract_entities(user_input)
    tfidf_scores = _tfidf_scores(user_input)

    scored_templates = []
    all_matched_keywords: set[str] = set()

    for idx, template in enumerate(POLICY_TEMPLATES):
        score, matched_kws = _keyword_score(user_input, template["keywords"])
        tfidf_score = tfidf_scores[idx]
        if score > 0 or tfidf_score > _TFIDF_THRESHOLD:
            confidence = _calculate_confidence(template["confidence"], score, len(template["keywords"]))
            tfidf_boost = int(tfidf_score * _TFIDF_BOOST_MULTIPLIER)
            confidence = max(10, min(99, confidence + tfidf_boost))
            scored_templates.append(
                {
                    **template,
                    "match_score": score,
                    "confidence": confidence,
                    "matched_keywords": matched_kws,
                    "_tfidf_score": round(tfidf_score, 4),
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

    # --- Gap analysis ---
    coverage_gaps: list[str] = []
    if requires_custom:
        covered_workloads: set[str] = set()
        for t in top_templates:
            for wl in t.get("workloads", []):
                covered_workloads.add(wl.lower())

        for mentioned in entities["workloads"]:
            canonical = _WORKLOAD_CANONICAL_MAP.get(mentioned, mentioned).lower()
            if not any(canonical in wl or wl in canonical for wl in covered_workloads):
                coverage_gaps.append(
                    f"Workload '{mentioned}' is mentioned but not fully covered by the matched templates."
                )

        for framework in entities["frameworks"]:
            if not any(
                framework.lower() in kw.lower()
                for t in top_templates
                for kw in t.get("keywords", [])
            ):
                coverage_gaps.append(
                    f"Regulatory framework '{framework}' is mentioned but may not be fully addressed."
                )

        for scenario in entities["risk_scenarios"]:
            if not any(
                scenario.lower() in kw.lower()
                for t in top_templates
                for kw in t.get("keywords", [])
            ):
                coverage_gaps.append(
                    f"Risk scenario '{scenario}' may require additional custom configuration."
                )

    # --- Confidence reasoning ---
    best = top_templates[0] if top_templates else None
    if best:
        kw_detail = f"{best['match_score']} of {len(best['keywords'])} keywords matched"
        tfidf_detail = (
            f"TF-IDF similarity: {best['_tfidf_score']:.2f}"
            if _TFIDF_AVAILABLE
            else "TF-IDF: unavailable (sklearn not installed)"
        )
        template_detail = (
            "template has built-in support"
            if best.get("template_available")
            else "no built-in template; custom config required"
        )
        confidence_reasoning = f"{kw_detail}; {tfidf_detail}; {template_detail}."
    else:
        confidence_reasoning = "No template matched; confidence based on custom configuration baseline."

    # --- Multi-template combination note ---
    combination_note = ""
    if len(top_templates) >= 2:
        names = [t["name"] for t in top_templates]
        combination_note = (
            f"Combining {len(top_templates)} templates provides broader coverage: "
            + ", ".join(f"'{n}'" for n in names)
            + ". Each addresses a distinct aspect of your requirement."
        )

    # --- doc_search_query ---
    if top_templates and top_templates[0].get("doc_search_query"):
        doc_search_query = top_templates[0]["doc_search_query"]
    elif all_matched_keywords:
        doc_search_query = "Microsoft Purview " + " ".join(sorted(all_matched_keywords)[:_MAX_SEARCH_KEYWORDS])
    else:
        doc_search_query = "Microsoft Purview policy configuration"

    return {
        "matched_templates": top_templates,
        "requires_custom": requires_custom,
        "custom_configs": custom_configs,
        "overall_confidence": overall_confidence,
        "summary": summary,
        "matched_keywords": sorted(all_matched_keywords),
        "intents": intents,
        "entities": entities,
        "coverage_gaps": coverage_gaps,
        "confidence_reasoning": confidence_reasoning,
        "combination_note": combination_note,
        "doc_search_query": doc_search_query,
    }

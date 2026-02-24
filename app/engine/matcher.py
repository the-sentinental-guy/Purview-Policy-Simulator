"""Policy matcher: finds the best DLP template matches for a natural-language query."""
from typing import List

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.knowledge_base.dlp_templates import get_dlp_templates
from app.models.confidence import ConfidenceScore
from app.models.policy import PolicyTemplate
from app.models.simulation import TemplateMatch
from .nlp_processor import NLPProcessor


class PolicyMatcher:
    """Matches a natural-language query against the DLP template knowledge base."""

    def __init__(self) -> None:
        self._templates: List[PolicyTemplate] = get_dlp_templates()
        self._vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            stop_words="english",
            lowercase=True,
        )
        self._matrix = self._build_index()

    # ------------------------------------------------------------------
    # Index construction
    # ------------------------------------------------------------------

    def _template_document(self, template: PolicyTemplate) -> str:
        """Combine a template's textual fields into a single indexable document."""
        parts = [
            template.name,
            template.description,
            " ".join(template.keywords),
            " ".join(template.compliance_frameworks),
            " ".join(template.tags),
            " ".join(template.sensitive_info_types),
        ]
        return " ".join(parts)

    def _build_index(self):
        """Build the TF-IDF matrix from all template documents."""
        docs = [self._template_document(t) for t in self._templates]
        return self._vectorizer.fit_transform(docs)

    # ------------------------------------------------------------------
    # Matching
    # ------------------------------------------------------------------

    def find_matches(
        self,
        query: str,
        nlp_processor: NLPProcessor,
        max_results: int = 3,
    ) -> List[TemplateMatch]:
        """Return the top-N template matches for the given query."""
        query_vec = nlp_processor.get_query_vector(query, self._vectorizer)
        similarities = cosine_similarity(query_vec, self._matrix).flatten()

        query_lower = query.lower()
        entities = nlp_processor.extract_entities(query)
        query_frameworks = {f.lower() for f in entities.get("frameworks", [])}

        scored: List[tuple] = []
        for idx, template in enumerate(self._templates):
            base_sim = float(similarities[idx])

            # Keyword overlap boost
            kw_matches = [
                kw for kw in template.keywords if kw.lower() in query_lower
            ]
            kw_boost = min(len(kw_matches) * 0.04, 0.20)

            # Framework overlap boost
            tmpl_frameworks = {f.lower() for f in template.compliance_frameworks}
            fw_matches = list(tmpl_frameworks & query_frameworks)
            fw_boost = min(len(fw_matches) * 0.08, 0.24)

            # Entity location overlap boost
            query_locs = {loc.lower() for loc in entities.get("locations", [])}
            tmpl_locs = {loc.lower() for loc in template.locations}
            loc_boost = min(len(query_locs & tmpl_locs) * 0.03, 0.09)

            boosted = min(base_sim + kw_boost + fw_boost + loc_boost, 1.0)
            scored.append((boosted, base_sim, kw_matches, fw_matches, template))

        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:max_results]

        results: List[TemplateMatch] = []
        for boosted_score, _, kw_matches, fw_matches, template in top:
            if boosted_score < 0.01:
                continue
            confidence = self._calculate_confidence(
                similarity=boosted_score,
                keyword_matches=kw_matches,
                framework_matches=fw_matches,
                query=query,
                template=template,
            )
            results.append(
                TemplateMatch(
                    template=template,
                    confidence=confidence,
                    similarity_score=round(boosted_score, 4),
                    matched_keywords=kw_matches,
                    matched_frameworks=fw_matches,
                )
            )
        return results

    # ------------------------------------------------------------------
    # Confidence scoring
    # ------------------------------------------------------------------

    def _calculate_confidence(
        self,
        similarity: float,
        keyword_matches: List[str],
        framework_matches: List[str],
        query: str,
        template: PolicyTemplate,
    ) -> ConfidenceScore:
        """Produce a ConfidenceScore with human-readable reasoning."""
        factors: List[str] = []

        # Base similarity contribution
        if similarity >= 0.75:
            factors.append(f"Very high semantic similarity ({similarity:.0%})")
        elif similarity >= 0.50:
            factors.append(f"High semantic similarity ({similarity:.0%})")
        elif similarity >= 0.30:
            factors.append(f"Moderate semantic similarity ({similarity:.0%})")
        else:
            factors.append(f"Low semantic similarity ({similarity:.0%})")

        if keyword_matches:
            factors.append(
                f"{len(keyword_matches)} keyword{'s' if len(keyword_matches) > 1 else ''} matched: "
                + ", ".join(f'"{k}"' for k in keyword_matches[:3])
            )

        if framework_matches:
            factors.append(
                f"Compliance framework match: {', '.join(framework_matches)}"
            )

        if template.category.lower() in query.lower():
            factors.append(f"Template category '{template.category}' mentioned explicitly")

        # Compute a composite score
        kw_factor = min(len(keyword_matches) * 0.05, 0.20)
        fw_factor = min(len(framework_matches) * 0.10, 0.20)
        composite = min(similarity * 0.6 + kw_factor + fw_factor, 1.0)

        level_map = [
            (0.85, "HIGH"),
            (0.60, "MEDIUM"),
            (0.30, "LOW"),
        ]
        level = "VERY_LOW"
        for threshold, lbl in level_map:
            if composite >= threshold:
                level = lbl
                break

        reasoning = (
            f"Template '{template.name}' scored {composite:.0%} confidence. "
            + (" ".join(factors) if factors else "Matched via semantic similarity.")
        )

        return ConfidenceScore(
            score=round(composite, 4),
            level=level,
            reasoning=reasoning,
            factors=factors,
        )

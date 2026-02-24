import asyncio
import logging
from datetime import datetime, timezone

from simulator.engine.nlp_processor import NLPProcessor
from simulator.engine.matcher import TemplateMatcher
from simulator.engine.effects import EffectsGenerator
from simulator.models.simulation import SimulationResult, TemplateMatch
from simulator.models.confidence import ConfidenceScorer
from simulator.mcp_client import MCPClient
from simulator.knowledge_base.documentation_refs import get_docs_for_category

logger = logging.getLogger(__name__)


class SimulationEngine:
    def __init__(self):
        self.nlp = NLPProcessor()
        self.matcher = TemplateMatcher()
        self.effects_gen = EffectsGenerator()
        self.confidence_scorer = ConfidenceScorer()
        self.mcp_client = MCPClient()

    async def simulate(self, query: str, mcp_enabled: bool = True) -> SimulationResult:
        # Step 1: NLP analysis
        nlp_result = self.nlp.process(query)

        # Step 2: Find matching templates
        matches_raw = self.matcher.match(query, nlp_result, top_k=5)

        # Step 3: Generate effects and confidence for each match
        template_matches = []
        for template, raw_score in matches_raw[:5]:
            keyword_count = sum(
                1 for kw in nlp_result.get("keywords", [])
                if kw in template.get("search_text", "").lower()
            )
            category_match = any(
                comp in template.get("category", "").lower()
                for comp in nlp_result.get("compliance", [])
            )
            score, level = self.confidence_scorer.score(raw_score, keyword_count, category_match)

            effects = self.effects_gen.generate(template, nlp_result)
            explanation = self._build_explanation(template, nlp_result, level)

            template_matches.append(TemplateMatch(
                template=template,
                confidence_score=round(score, 3),
                confidence_level=level,
                effects=effects,
                explanation=explanation,
            ))

        # Step 4: Optionally fetch MCP docs
        mcp_refs = []
        if mcp_enabled:
            try:
                mcp_refs = await asyncio.wait_for(
                    self.mcp_client.microsoft_docs_search(query),
                    timeout=5.0
                )
            except Exception:
                pass

        # Fallback to static refs if MCP unavailable
        if not mcp_refs and template_matches:
            top_category = template_matches[0].template.get("category", "General")
            mcp_refs = get_docs_for_category(top_category)

        # Step 5: Build summary
        summary = self._build_summary(query, template_matches, nlp_result)

        return SimulationResult(
            query=query,
            matches=template_matches,
            nlp_analysis=nlp_result,
            mcp_references=mcp_refs,
            summary=summary,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def _build_explanation(self, template: dict, nlp_result: dict, level: str) -> str:
        parts = []
        cat = template.get("category", "General")
        name = template.get("name", "Policy Template")
        parts.append(f"**{name}** ({cat} category) matches your query with {level} confidence.")

        matched_compliance = [
            c for c in nlp_result.get("compliance", [])
            if c.replace("_", " ") in template.get("search_text", "").lower()
            or c.upper() in template.get("regulatory_references", [])
        ]
        if matched_compliance:
            parts.append(f"Regulatory alignment: {', '.join(c.upper() for c in matched_compliance)}.")

        locs = template.get("locations", [])
        if locs:
            parts.append(f"This policy covers: {', '.join(locs)}.")

        return " ".join(parts)

    def _build_summary(self, query: str, matches: list, nlp_result: dict) -> str:
        if not matches:
            return (
                "No matching policies found. "
                "Try rephrasing your query with more specific data types or compliance frameworks."
            )

        top = matches[0]
        n = len(matches)
        return (
            f"Found {n} matching policy template(s) for your scenario. "
            f"Top match: **{top.template.get('name')}** with {top.confidence_level} confidence "
            f"({top.confidence_score:.0%}). "
            f"Detected intent: {', '.join(nlp_result.get('intent', ['protect']))}. "
            f"Key data types identified: "
            f"{', '.join(nlp_result.get('data_types', [])) or 'general sensitive data'}."
        )

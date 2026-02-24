"""Core policy simulator: orchestrates NLP, matching, and effects calculation."""
import time
from typing import Any, Dict, List, Optional

from app.knowledge_base.troubleshooting import get_troubleshooting_guide
from app.models.simulation import (
    CustomConfiguration,
    GapAnalysis,
    SimulationRequest,
    SimulationResponse,
    TemplateMatch,
)
from .effects import EffectsCalculator
from .matcher import PolicyMatcher
from .nlp_processor import NLPProcessor


# Confidence threshold below which a custom configuration is also generated
_CUSTOM_CONFIG_THRESHOLD = 0.70


class PolicySimulator:
    """Orchestrates the full simulation pipeline for a natural-language policy query."""

    def __init__(self) -> None:
        self._nlp = NLPProcessor()
        self._matcher = PolicyMatcher()
        self._effects_calc = EffectsCalculator()
        self._troubleshooting = get_troubleshooting_guide()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def simulate(self, request: SimulationRequest) -> SimulationResponse:
        """Run the full simulation and return a SimulationResponse."""
        start_ms = time.monotonic() * 1000

        query = request.query
        intent = self._nlp.extract_intent(query)
        entities = self._nlp.extract_entities(query)

        template_matches = self._matcher.find_matches(
            query=query,
            nlp_processor=self._nlp,
            max_results=request.max_templates,
        )

        effects = self._effects_calc.calculate_effects(
            template_matches=template_matches,
            query=query,
            intent=intent,
        )

        custom_config: Optional[CustomConfiguration] = None
        top_score = template_matches[0].confidence.score if template_matches else 0.0
        if top_score < _CUSTOM_CONFIG_THRESHOLD:
            custom_config = self._build_custom_configuration(query, entities, intent)

        troubleshooting_tips = self._get_troubleshooting_tips(template_matches)

        elapsed_ms = time.monotonic() * 1000 - start_ms

        return SimulationResponse(
            query=query,
            intent=intent,
            entities=entities,
            template_matches=template_matches,
            custom_configuration=custom_config,
            effects=effects,
            documentation_links=[],
            troubleshooting_tips=troubleshooting_tips,
            mcp_enriched=False,
            processing_time_ms=round(elapsed_ms, 2),
        )

    # ------------------------------------------------------------------
    # Custom configuration
    # ------------------------------------------------------------------

    def _build_custom_configuration(
        self,
        query: str,
        entities: Dict[str, List[str]],
        intent: str,
    ) -> CustomConfiguration:
        """Build a bespoke policy configuration when no strong template match exists."""
        locations = entities.get("locations", []) or [
            "Exchange", "SharePoint", "OneDrive", "Teams"
        ]
        sensitive_info_types = entities.get("data_types", []) or [
            "Sensitive Information Type (custom)"
        ]
        frameworks = entities.get("frameworks", [])

        actions = self._default_actions_for_intent(intent)

        steps = [
            "Note: This is a suggested configuration. Verify all settings against official Microsoft documentation before deploying.",
            "Open the Microsoft Purview compliance portal (compliance.microsoft.com).",
            "Navigate to Data loss prevention > Policies > Create policy.",
            "Choose 'Custom policy' as the template.",
            f"Set the policy name to reflect the intent: '{intent.capitalize()} – Custom Policy'.",
            f"Add the following locations: {', '.join(locations)}.",
            "Define conditions using the sensitive information types identified below.",
            "Configure the recommended actions listed below.",
            "Enable simulation mode and monitor for 14 days before enforcing.",
            "Review matches in the DLP activity explorer and adjust thresholds as needed.",
        ]

        gap_analysis = self._build_gap_analysis(entities, frameworks)

        return CustomConfiguration(
            title=f"⚠️ Suggested Starting Point — Custom DLP Policy – {intent.capitalize()} Sensitive Data",
            steps=steps,
            locations=locations,
            sensitive_info_types=sensitive_info_types,
            actions=actions,
            gap_analysis=gap_analysis,
        )

    def _default_actions_for_intent(self, intent: str) -> List[str]:
        """Return sensible default actions based on the extracted intent."""
        mapping: Dict[str, List[str]] = {
            "protect": [
                "Block sharing outside the organisation",
                "Notify user with policy tip",
                "Alert compliance administrator",
            ],
            "prevent": [
                "Block sharing outside the organisation",
                "Require business justification for override",
                "Alert security team",
            ],
            "detect": [
                "Generate DLP alert on detection",
                "Notify compliance administrator",
                "Log match in activity explorer",
            ],
            "monitor": [
                "Audit all access without blocking",
                "Send daily digest to compliance team",
                "Log to SIEM via activity explorer",
            ],
            "retain": [
                "Apply retention label to matched content",
                "Prevent deletion for the retention period",
                "Notify records manager on policy match",
            ],
            "classify": [
                "Apply sensitivity label to matched content",
                "Notify user with classification policy tip",
                "Log classification action",
            ],
            "investigate": [
                "Preserve content for eDiscovery hold",
                "Generate incident report",
                "Notify compliance officer",
            ],
        }
        return mapping.get(intent, mapping["protect"])

    def _build_gap_analysis(
        self, entities: Dict[str, List[str]], frameworks: List[str]
    ) -> GapAnalysis:
        covered: List[str] = []
        missing: List[str] = []
        recommendations: List[str] = []

        if entities.get("data_types"):
            covered.append(f"Data types identified: {', '.join(entities['data_types'])}")
        else:
            missing.append("No specific sensitive information types identified in the query")
            recommendations.append(
                "Specify the data types to protect (e.g., credit card numbers, SSNs, PHI)"
            )

        if entities.get("locations"):
            covered.append(f"Locations specified: {', '.join(entities['locations'])}")
        else:
            missing.append("No specific Microsoft 365 locations defined")
            recommendations.append(
                "Define the locations to cover (Exchange, SharePoint, Teams, Devices)"
            )

        if frameworks:
            covered.append(f"Compliance frameworks referenced: {', '.join(frameworks)}")
        else:
            missing.append("No compliance framework specified")
            recommendations.append(
                "Reference a compliance framework (e.g., PCI-DSS, HIPAA, GDPR) to leverage "
                "pre-built sensitive information types"
            )

        recommendations.append(
            "Start with a simulation mode deployment to measure match rates before enforcing"
        )

        return GapAnalysis(covered=covered, missing=missing, recommendations=recommendations)

    # ------------------------------------------------------------------
    # Troubleshooting
    # ------------------------------------------------------------------

    def _get_troubleshooting_tips(self, matches: List[TemplateMatch]) -> List[str]:
        """Extract the most relevant troubleshooting tips for the matched templates."""
        tips: List[str] = []
        dlp_issues: List[Any] = self._troubleshooting.get("dlp_issues", [])

        # Always include the first two general DLP tips
        for issue in dlp_issues[:2]:
            solutions: List[str] = issue.get("solutions", [])
            if solutions:
                tips.append(solutions[0])

        # Add severity-specific tip for high-severity matches
        for match in matches:
            if match.template.severity == "high" and len(tips) < 5:
                tips.append(
                    f"For high-severity policy '{match.template.name}': deploy in simulation "
                    "mode for at least 14 days and review matches before enabling enforcement."
                )
                break

        # Tip about false positives when confidence is not high
        if matches and matches[0].confidence.score < 0.70:
            for issue in dlp_issues:
                if "false_positive" in issue.get("id", ""):
                    solutions = issue.get("solutions", [])
                    if solutions and solutions[0] not in tips:
                        tips.append(solutions[0])
                    break

        return tips[:5]

"""Effects calculator: derives realistic policy effects from matched templates."""
from typing import Dict, List

from app.models.effects import SimulationEffects
from app.models.simulation import TemplateMatch


class EffectsCalculator:
    """Calculates the observable effects of applying matched DLP policies."""

    # Default per-severity deployment recommendations
    _SEVERITY_RECOMMENDATIONS: Dict[str, List[str]] = {
        "high": [
            "Deploy in simulation mode for a minimum of 14 days before enforcing.",
            "Alert compliance and security teams for every policy match.",
            "Require manager approval for any user override.",
            "Schedule a quarterly review of blocked-action reports.",
        ],
        "medium": [
            "Run the policy in simulation mode for 7 days before enforcing.",
            "Enable user-facing policy tips to promote awareness.",
            "Review false-positive rates after the first 30 days.",
            "Notify the data owner when sensitive content is detected.",
        ],
        "low": [
            "Monitor alerts in audit-only mode initially.",
            "Communicate the policy to end users via policy tips.",
            "Review match rates monthly and adjust thresholds as needed.",
        ],
    }

    def calculate_effects(
        self,
        template_matches: List[TemplateMatch],
        query: str,
        intent: str,
    ) -> SimulationEffects:
        """Build a SimulationEffects object from matched templates and intent."""
        if not template_matches:
            return self._default_effects(intent)

        # Use the highest-confidence match as the primary driver
        primary = template_matches[0]
        template = primary.template
        severity = template.severity.lower()

        blocked_actions = self._blocked_actions(template, intent)
        audited_actions = self._audited_actions(template)
        notifications = self._notifications(template, severity)
        policy_tips = self._policy_tips(template)
        incident_reports = self._incident_reports(template, severity)
        user_experience = self._user_experience(intent, severity)
        admin_experience = self._admin_experience(severity, template.name)
        false_positive_risk = self._false_positive_risk(primary.confidence.score)
        deployment_recs = list(
            self._SEVERITY_RECOMMENDATIONS.get(severity, self._SEVERITY_RECOMMENDATIONS["medium"])
        )

        # Merge additional actions from secondary matches without duplication
        for match in template_matches[1:]:
            for action in self._blocked_actions(match.template, intent):
                if action not in blocked_actions:
                    blocked_actions.append(action)

        return SimulationEffects(
            blocked_actions=blocked_actions,
            audited_actions=audited_actions,
            notifications=notifications,
            user_experience=user_experience,
            admin_experience=admin_experience,
            false_positive_risk=false_positive_risk,
            deployment_recommendations=deployment_recs,
            policy_tips=policy_tips,
            incident_reports=incident_reports,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _blocked_actions(self, template, intent: str) -> List[str]:
        actions = [a for a in template.actions if "block" in a.lower() or "restrict" in a.lower()]
        if not actions and intent in ("protect", "prevent"):
            actions = [
                f"Block sharing of {template.name.lower()} content outside the organisation",
                "Prevent upload to unsanctioned cloud storage",
            ]
        return actions or [f"Block external sharing of content matched by '{template.name}'"]

    def _audited_actions(self, template) -> List[str]:
        return [
            f"Log all access to content matched by '{template.name}'",
            "Record user identity, timestamp, and action in the audit log",
            "Capture content evidence for DLP incident review",
        ]

    def _notifications(self, template, severity: str) -> List[str]:
        notifs = [
            f"Notify compliance administrator when '{template.name}' content is detected",
            "Send email digest of DLP matches to the security team (daily)",
        ]
        if severity == "high":
            notifs.append("Page the on-call security analyst for critical policy violations")
        return notifs

    def _policy_tips(self, template) -> List[str]:
        return [
            (
                f"Policy tip shown to user: 'This content may contain {template.category.lower()} "
                "data protected by your organisation's DLP policy.'"
            ),
            "User may provide a business justification to override the policy tip.",
        ]

    def _incident_reports(self, template, severity: str) -> List[str]:
        reports = [
            f"DLP incident report created for each '{template.name}' policy match",
            "Incident includes sender, recipients, subject, and matched sensitive information type",
        ]
        if severity == "high":
            reports.append(
                "High-severity incidents are escalated to the compliance officer automatically"
            )
        return reports

    def _user_experience(self, intent: str, severity: str) -> str:
        if intent in ("protect", "prevent") and severity == "high":
            return (
                "Users are blocked from sharing the sensitive content and receive a policy tip "
                "explaining why the action was prevented. An override requires manager approval."
            )
        if intent == "monitor":
            return (
                "Users see a policy tip advising that the content may be sensitive. "
                "They can proceed after acknowledging the tip; the action is logged."
            )
        return (
            "Users receive an informational policy tip when sensitive content is detected. "
            "They may provide a business justification to continue."
        )

    def _admin_experience(self, severity: str, template_name: str) -> str:
        return (
            f"Compliance administrators see '{template_name}' incidents in the DLP activity "
            "explorer and can review matched content, user actions, and override justifications. "
            f"{'Real-time alerts are sent for every match.' if severity == 'high' else 'Daily digest alerts are configured.'}"
        )

    def _false_positive_risk(self, confidence_score: float) -> str:
        if confidence_score >= 0.80:
            return "Low"
        if confidence_score >= 0.55:
            return "Medium"
        return "High"

    def _default_effects(self, intent: str) -> SimulationEffects:
        return SimulationEffects(
            blocked_actions=["Block sharing of sensitive content outside the organisation"],
            audited_actions=["Log all detected sensitive content access"],
            notifications=["Notify compliance administrator on policy match"],
            user_experience="Users receive a policy tip when sensitive content is detected.",
            admin_experience="Compliance administrators receive alerts for policy matches.",
            false_positive_risk="Medium",
            deployment_recommendations=self._SEVERITY_RECOMMENDATIONS["medium"],
            policy_tips=["Policy tip: 'This content may be sensitive. Please review before sharing.'"],
            incident_reports=["DLP incident report generated for each policy match"],
        )

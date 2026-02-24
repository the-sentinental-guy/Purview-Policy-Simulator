from typing import Dict, Any


class EffectsGenerator:
    def generate(self, template: Dict[str, Any], nlp_result: Dict[str, Any]) -> Dict[str, Any]:
        actions = template.get("actions", {})
        locations = template.get("locations", [])
        conditions = template.get("conditions", {})
        category = template.get("category", "General")

        blocked_actions = []
        audited_actions = []

        if actions.get("block_sharing"):
            blocked_actions.append("Share document externally")
            blocked_actions.append("Forward email to external recipients")
        if actions.get("restrict_access"):
            blocked_actions.append("Open/view without proper permissions")
        if actions.get("block_download"):
            blocked_actions.append("Download to unmanaged device")
        if actions.get("block_paste"):
            blocked_actions.append("Paste sensitive content to unapproved apps")

        audited_actions.append("Access to protected content")
        if actions.get("generate_incident_report"):
            audited_actions.append("Policy match generates incident report")
        audited_actions.append("User override attempts (if allowed)")

        user_notification = {
            "enabled": actions.get("notify_user", False),
            "message": template.get("user_notification", {}).get(
                "message", "This content appears to contain sensitive information."
            ),
            "policy_tip": template.get("user_notification", {}).get(
                "policy_tip", "Please review sharing permissions before proceeding."
            ),
            "override_allowed": template.get("user_notification", {}).get("override_allowed", False),
        }

        admin_notification = {
            "incident_report": actions.get("generate_incident_report", False),
            "severity": template.get("incident_report", {}).get("severity", "Medium"),
            "send_to": template.get("incident_report", {}).get("send_to", ["compliance@company.com"]),
            "alert_dashboard": True,
        }

        sensitive_count = conditions.get("content_count", {}).get("min", 1)
        if sensitive_count >= 5:
            fp_risk = "LOW"
        elif sensitive_count >= 2:
            fp_risk = "LOW"
        else:
            fp_risk = "MEDIUM"

        if category in ["Intellectual Property", "Executive Communications"]:
            fp_risk = "HIGH"

        deployment_recommendations = [
            "Start in simulation/test mode before enforcing",
            "Review false positive reports weekly for first month",
            f"Scope initially to pilot group of {locations[0] if locations else 'Exchange'} users",
            "Configure exception groups for authorized users (Legal, Finance, HR)",
            "Set up incident review workflow in Microsoft Purview compliance portal",
        ]

        dependencies = [
            "Microsoft Purview compliance license (E3/E5 or add-on)",
            "DLP policy deployed via Microsoft Purview compliance portal",
        ]
        if "Teams" in locations:
            dependencies.append("Teams DLP license (Microsoft 365 E5 Compliance)")
        if "endpoints" in nlp_result.get("locations", []) or "Endpoints" in locations:
            dependencies.append("Microsoft Defender for Endpoint (MDE) for endpoint DLP")
        if actions.get("encrypt"):
            dependencies.append("Azure Information Protection / Microsoft Purview Information Protection")

        coverage_map = {
            1: "~10-20% of org users (pilot)",
            2: "~30-50% of org users (expanded)",
            3: "~60-80% of org users (broad)",
            4: "~90-100% of org users (full rollout)",
        }
        coverage = coverage_map.get(len(locations), "~50-70% of workloads")

        user_experience = {
            "policy_tip_shown": user_notification["enabled"],
            "blocked_dialog": bool(blocked_actions),
            "can_override": user_notification["override_allowed"],
            "email_notification": actions.get("notify_user", False),
            "affected_apps": locations,
        }

        admin_experience = {
            "incident_dashboard": admin_notification["incident_report"],
            "severity_level": admin_notification["severity"],
            "dlp_alerts": True,
            "activity_explorer": True,
            "content_explorer": True,
        }

        return {
            "blocked_actions": blocked_actions,
            "audited_actions": audited_actions,
            "notifications": {
                "user": user_notification,
                "admin": admin_notification,
            },
            "user_experience": user_experience,
            "admin_experience": admin_experience,
            "false_positive_risk": fp_risk,
            "deployment_recommendations": deployment_recommendations,
            "dependencies": dependencies,
            "estimated_coverage": coverage,
        }

"""Insider risk management knowledge base for Microsoft Purview Policy Simulator."""
from typing import Any, Dict, List


def get_insider_risk_templates() -> List[Dict[str, Any]]:
    """Return a list of insider risk policy templates."""
    return [
        {
            "id": "data_theft_departing_users",
            "name": "Data Theft by Departing Users",
            "description": (
                "Detects potential data theft activities by employees who have submitted "
                "resignation notices or whose employment is being terminated. Monitors "
                "unusual file downloads, USB transfers, email forwards to personal accounts, "
                "and cloud storage uploads in the period leading up to departure."
            ),
            "triggering_events": [
                "HR connector resignation date",
                "HR connector termination date",
                "Azure AD account deletion",
                "Manager-submitted offboarding ticket",
            ],
            "risk_indicators": [
                "Downloading files from SharePoint/OneDrive",
                "Copying files to USB or removable media",
                "Emailing files to personal email address",
                "Uploading files to personal cloud storage",
                "Printing sensitive documents",
                "Accessing files outside normal working hours",
            ],
            "investigation_steps": [
                "Review alert timeline for anomalous volume spikes",
                "Examine file activity logs for sensitive content",
                "Check network egress logs for large transfers",
                "Review DLP policy matches correlated with the user",
                "Escalate to case for HR and legal review if confirmed",
            ],
            "keywords": [
                "departing user", "resignation", "termination", "offboarding",
                "data theft", "exfiltration", "leaving employee",
            ],
            "severity": "high",
            "recommended_settings": {
                "lookback_window_days": 90,
                "alert_threshold": "medium",
                "include_cloud_storage": True,
                "include_removable_media": True,
                "include_print_activity": True,
                "sequence_detection": True,
            },
        },
        {
            "id": "general_data_leaks",
            "name": "General Data Leaks",
            "description": (
                "Identifies potential unintentional or intentional data leaks by any employee "
                "without a specific triggering HR event. Uses baseline behaviour modelling to "
                "detect anomalous sharing, downloading, or uploading activity across email, "
                "cloud storage, and endpoint devices."
            ),
            "triggering_events": [
                "DLP policy match",
                "Cumulative anomaly detection",
                "Risk score threshold breach",
            ],
            "risk_indicators": [
                "Mass download of SharePoint documents",
                "Sharing sensitive files with external users",
                "Uploading to non-sanctioned cloud services",
                "Obfuscating file names before transfer",
                "Disabling DLP policy tips",
            ],
            "investigation_steps": [
                "Identify files involved and their sensitivity labels",
                "Determine destination of leaked data",
                "Assess whether activity matches a business justification",
                "Check for correlated DLP alerts",
                "Document findings and take remediation action",
            ],
            "keywords": [
                "data leak", "data loss", "general leak", "accidental disclosure",
                "unauthorised sharing", "oversharing",
            ],
            "severity": "medium",
            "recommended_settings": {
                "lookback_window_days": 30,
                "alert_threshold": "high",
                "include_cloud_storage": True,
                "include_removable_media": True,
                "include_print_activity": False,
                "sequence_detection": False,
            },
        },
        {
            "id": "data_leaks_priority_users",
            "name": "Data Leaks by Priority Users",
            "description": (
                "Applies enhanced monitoring to a defined set of high-value or high-risk users "
                "such as executives, privileged IT administrators, and employees with access to "
                "particularly sensitive intellectual property or regulated data. Lower alert "
                "thresholds generate alerts on activity volumes that would not trigger alerts "
                "for standard users."
            ),
            "triggering_events": [
                "Priority user group membership",
                "DLP policy match",
                "Anomalous activity baseline deviation",
            ],
            "risk_indicators": [
                "Any unusual file transfer for priority user",
                "Access to sensitive repositories outside role",
                "Bulk email attachments to external recipients",
                "Repeated DLP overrides",
            ],
            "investigation_steps": [
                "Verify user membership in priority user group",
                "Review full activity timeline",
                "Compare activity against peer baseline",
                "Engage HR and legal for priority user investigations",
                "Apply enhanced evidence collection",
            ],
            "keywords": [
                "priority user", "executive", "privileged user", "high value target",
                "VIP", "administrator", "sensitive role",
            ],
            "severity": "high",
            "recommended_settings": {
                "lookback_window_days": 90,
                "alert_threshold": "low",
                "include_cloud_storage": True,
                "include_removable_media": True,
                "include_print_activity": True,
                "sequence_detection": True,
                "priority_user_group_required": True,
            },
        },
        {
            "id": "data_leaks_disgruntled_users",
            "name": "Data Leaks by Disgruntled Users",
            "description": (
                "Detects potential data leakage from employees exhibiting signals associated "
                "with disgruntlement, such as demotion, performance improvement plan placement, "
                "or negative workplace communication patterns. Combines HR connector signals "
                "with behavioural anomaly detection."
            ),
            "triggering_events": [
                "HR connector performance improvement plan event",
                "HR connector demotion event",
                "Negative sentiment communication detection",
            ],
            "risk_indicators": [
                "Sudden increase in file downloads",
                "Accessing files unrelated to current role",
                "Sending bulk emails to personal account",
                "Searching for competitor companies internally",
                "Disabling endpoint protection features",
            ],
            "investigation_steps": [
                "Correlate HR event trigger with activity timeline",
                "Review communication patterns for sentiment signals",
                "Examine file access logs for scope creep",
                "Determine if data accessed is sensitive or proprietary",
                "Coordinate with HR before contacting the employee",
            ],
            "keywords": [
                "disgruntled", "unhappy employee", "performance plan", "PIP",
                "demotion", "sabotage", "malicious insider",
            ],
            "severity": "high",
            "recommended_settings": {
                "lookback_window_days": 60,
                "alert_threshold": "medium",
                "include_cloud_storage": True,
                "include_removable_media": True,
                "include_print_activity": True,
                "sequence_detection": True,
                "hr_connector_required": True,
            },
        },
        {
            "id": "security_policy_violations_general",
            "name": "Security Policy Violations (General)",
            "description": (
                "Monitors all employees for actions that violate the organisation's security "
                "policies, including disabling endpoint security controls, installing "
                "unauthorised software, bypassing network security tools, or accessing "
                "prohibited websites and services."
            ),
            "triggering_events": [
                "Endpoint security alert",
                "DLP policy match",
                "Risk score threshold breach",
            ],
            "risk_indicators": [
                "Disabling antivirus or endpoint detection",
                "Installing unauthorised applications",
                "Accessing dark web or anonymous proxies",
                "Bypassing VPN or network controls",
                "Tampering with audit log settings",
            ],
            "investigation_steps": [
                "Identify specific policy violated and associated control",
                "Determine if violation was intentional or accidental",
                "Review frequency and pattern of violations",
                "Assess business impact and data exposure",
                "Remediate with IT security team and document",
            ],
            "keywords": [
                "policy violation", "security bypass", "unauthorised software",
                "endpoint tampering", "audit log", "compliance violation",
            ],
            "severity": "medium",
            "recommended_settings": {
                "lookback_window_days": 30,
                "alert_threshold": "medium",
                "include_cloud_storage": False,
                "include_removable_media": True,
                "include_print_activity": False,
                "sequence_detection": False,
            },
        },
        {
            "id": "security_policy_violations_departing",
            "name": "Security Policy Violations by Departing Users",
            "description": (
                "Applies heightened monitoring for security policy violations committed by "
                "employees in the offboarding window. Combines departure HR signals with "
                "security violation detection to identify users who may be attempting to "
                "cover their tracks or undermine controls before leaving."
            ),
            "triggering_events": [
                "HR connector resignation or termination date",
                "Azure AD account deletion notice",
                "Endpoint security policy violation",
            ],
            "risk_indicators": [
                "Disabling audit logging or security tools",
                "Deleting files or wiping devices before departure",
                "Accessing systems after access should have been revoked",
                "Exporting security configuration data",
                "Bulk deletion of emails or documents",
            ],
            "investigation_steps": [
                "Cross-reference departure date with violation timeline",
                "Check for evidence of anti-forensic activity",
                "Review access log completeness for gaps",
                "Preserve evidence before account deprovisioning",
                "Escalate to legal if wilful destruction is suspected",
            ],
            "keywords": [
                "departing user", "offboarding", "security violation", "anti-forensic",
                "log deletion", "account revocation", "termination",
            ],
            "severity": "high",
            "recommended_settings": {
                "lookback_window_days": 90,
                "alert_threshold": "low",
                "include_cloud_storage": True,
                "include_removable_media": True,
                "include_print_activity": True,
                "sequence_detection": True,
                "hr_connector_required": True,
            },
        },
        {
            "id": "patient_data_misuse",
            "name": "Patient Data Misuse",
            "description": (
                "Designed for healthcare organisations to detect inappropriate access to or "
                "sharing of patient health records and personally identifiable health information. "
                "Monitors for access patterns inconsistent with a clinician's patient caseload "
                "and flags sharing of protected health information (PHI) outside authorised channels."
            ),
            "triggering_events": [
                "EHR system access outside assigned patient list",
                "DLP policy match on PHI content types",
                "Bulk PHI file download event",
            ],
            "risk_indicators": [
                "Accessing patient records not in assigned caseload",
                "Downloading bulk patient record exports",
                "Emailing PHI to non-clinical external address",
                "Printing patient records in high volume",
                "Accessing records of public figures or colleagues",
            ],
            "investigation_steps": [
                "Verify clinician-patient relationship for accessed records",
                "Determine if access aligns with documented care duties",
                "Check for HIPAA minimum necessary standard compliance",
                "Review destination of any shared PHI",
                "Coordinate with Privacy Officer for HIPAA breach assessment",
            ],
            "keywords": [
                "patient data", "PHI", "health records", "EHR", "HIPAA",
                "protected health information", "medical records", "healthcare",
            ],
            "severity": "high",
            "recommended_settings": {
                "lookback_window_days": 30,
                "alert_threshold": "medium",
                "include_cloud_storage": True,
                "include_removable_media": True,
                "include_print_activity": True,
                "sequence_detection": False,
                "healthcare_connector_recommended": True,
            },
        },
        {
            "id": "risky_browser_usage",
            "name": "Risky Browser Usage",
            "description": (
                "Monitors employee browsing activity on managed devices for access to websites "
                "and categories associated with insider risk, including dark web markets, "
                "competitor intelligence portals, job boards, and known data-broker or "
                "credential-theft sites. Uses Microsoft Defender for Endpoint browser signals."
            ),
            "triggering_events": [
                "Microsoft Defender for Endpoint browser activity signal",
                "Risk score threshold breach",
                "Cumulative risky site visit detection",
            ],
            "risk_indicators": [
                "Visiting dark web or Tor-related sites",
                "Accessing known data-broker websites",
                "Frequent visits to competitor career pages",
                "Uploading documents to public paste sites",
                "Accessing personal file-sharing services during business hours",
            ],
            "investigation_steps": [
                "Review browsing history timeline for patterns",
                "Identify specific URLs and site categories visited",
                "Correlate with file activity to detect related exfiltration",
                "Assess whether activity violates acceptable use policy",
                "Document findings and apply appropriate remediation",
            ],
            "keywords": [
                "browser usage", "web browsing", "dark web", "risky sites",
                "job boards", "data broker", "paste sites", "Defender for Endpoint",
            ],
            "severity": "medium",
            "recommended_settings": {
                "lookback_window_days": 30,
                "alert_threshold": "medium",
                "include_cloud_storage": False,
                "include_removable_media": False,
                "include_print_activity": False,
                "sequence_detection": False,
                "defender_for_endpoint_required": True,
            },
        },
        {
            "id": "cumulative_exfiltration_detection",
            "name": "Cumulative Exfiltration Detection",
            "description": (
                "Detects slow, deliberate data exfiltration that individually falls below alert "
                "thresholds but, when accumulated over a rolling time window, represents a "
                "significant data loss event. Particularly effective against users who are "
                "aware of monitoring thresholds and deliberately pace their activities."
            ),
            "triggering_events": [
                "Cumulative volume threshold breach over rolling window",
                "Consistent low-level anomaly pattern",
                "Sequence detection across multiple egress channels",
            ],
            "risk_indicators": [
                "Daily small-volume file transfers that accumulate over weeks",
                "Consistent after-hours access patterns",
                "Gradual increase in external email attachments",
                "Repeated small USB copy operations",
                "Slow upload to cloud storage spread across days",
            ],
            "investigation_steps": [
                "Aggregate activity across the full detection window",
                "Build a timeline of cumulative data volume",
                "Identify all egress channels used",
                "Assess total data volume and sensitivity",
                "Review for signs of deliberate threshold evasion",
            ],
            "keywords": [
                "cumulative exfiltration", "slow exfiltration", "data exfiltration",
                "threshold evasion", "low and slow", "rolling window",
            ],
            "severity": "high",
            "recommended_settings": {
                "lookback_window_days": 90,
                "alert_threshold": "low",
                "include_cloud_storage": True,
                "include_removable_media": True,
                "include_print_activity": True,
                "sequence_detection": True,
                "cumulative_window_days": 30,
            },
        },
    ]


def get_triggering_events() -> List[Dict[str, Any]]:
    """Return a list of insider risk triggering events and their sources."""
    return [
        # ── HR CONNECTOR EVENTS ───────────────────────────────────────────────
        {
            "id": "hr_resignation_date",
            "name": "HR Connector – Resignation Date",
            "source": "HR Connector",
            "description": (
                "Signals received from the HR system connector indicating that an employee "
                "has submitted a formal resignation. Activates monitoring windows for "
                "data theft by departing users and security policy violation templates."
            ),
            "data_fields": ["employee_id", "resignation_date", "last_working_day"],
            "policies_triggered": [
                "data_theft_departing_users",
                "security_policy_violations_departing",
            ],
            "setup_requirements": [
                "HR Connector configured in Microsoft Purview compliance portal",
                "HR system CSV export or API integration",
                "Scheduled daily refresh of HR data",
            ],
        },
        {
            "id": "hr_termination_date",
            "name": "HR Connector – Termination Date",
            "source": "HR Connector",
            "description": (
                "Signals from the HR system that an employee's contract has been terminated "
                "by the organisation. Triggers immediate monitoring escalation for the user "
                "and can be used to alert on access after the termination effective date."
            ),
            "data_fields": ["employee_id", "termination_date", "termination_reason"],
            "policies_triggered": [
                "data_theft_departing_users",
                "security_policy_violations_departing",
            ],
            "setup_requirements": [
                "HR Connector configured with termination feed",
                "Same-day HR system updates recommended",
                "Azure AD deprovisioning coordination",
            ],
        },
        {
            "id": "hr_performance_plan",
            "name": "HR Connector – Performance Improvement Plan",
            "source": "HR Connector",
            "description": (
                "Indicates that an employee has been placed on a formal performance improvement "
                "plan. Used as a disgruntlement signal to activate enhanced monitoring under "
                "data leaks by disgruntled users templates."
            ),
            "data_fields": ["employee_id", "pip_start_date", "pip_type"],
            "policies_triggered": ["data_leaks_disgruntled_users"],
            "setup_requirements": [
                "HR Connector with PIP event feed configured",
                "HR system must export PIP events with employee ID",
            ],
        },
        {
            "id": "hr_demotion",
            "name": "HR Connector – Demotion Event",
            "source": "HR Connector",
            "description": (
                "Signals that an employee has been demoted in role or responsibility level. "
                "Acts as a disgruntlement indicator triggering enhanced activity monitoring."
            ),
            "data_fields": ["employee_id", "previous_role", "new_role", "effective_date"],
            "policies_triggered": ["data_leaks_disgruntled_users"],
            "setup_requirements": [
                "HR Connector with job change event feed",
                "Role level mapping configured in the connector",
            ],
        },
        # ── DLP EVENTS ────────────────────────────────────────────────────────
        {
            "id": "dlp_policy_match",
            "name": "DLP Policy Match",
            "source": "Microsoft Purview DLP",
            "description": (
                "A DLP policy alert fires when a user attempts to share, send, or transfer "
                "content matching a sensitive information type or label condition. DLP matches "
                "are used as triggering events for general data leak and priority user policies."
            ),
            "data_fields": ["user_id", "policy_name", "sensitive_info_types", "location", "timestamp"],
            "policies_triggered": [
                "general_data_leaks",
                "data_leaks_priority_users",
                "patient_data_misuse",
            ],
            "setup_requirements": [
                "DLP policies deployed across relevant workloads",
                "Insider risk management DLP integration enabled",
                "Alert aggregation settings configured",
            ],
        },
        {
            "id": "dlp_high_severity_alert",
            "name": "DLP High-Severity Alert",
            "source": "Microsoft Purview DLP",
            "description": (
                "High-severity DLP alerts generated when a user triggers a DLP rule with "
                "a block or encrypt action on highly sensitive content. These alerts have "
                "elevated weight in the insider risk scoring model."
            ),
            "data_fields": ["user_id", "policy_name", "action_taken", "content_type", "timestamp"],
            "policies_triggered": [
                "general_data_leaks",
                "data_leaks_priority_users",
                "cumulative_exfiltration_detection",
            ],
            "setup_requirements": [
                "DLP high-severity alert threshold configured",
                "Insider risk DLP signal integration turned on",
            ],
        },
        # ── AZURE AD SIGNALS ──────────────────────────────────────────────────
        {
            "id": "azure_ad_account_deletion",
            "name": "Azure AD – Account Deletion",
            "source": "Azure Active Directory",
            "description": (
                "Azure AD signals indicating that a user account has been deleted or "
                "scheduled for deletion. Triggers an immediate monitoring window to capture "
                "any last-minute data activity before the account is fully deprovisioned."
            ),
            "data_fields": ["user_id", "deletion_timestamp", "account_type"],
            "policies_triggered": [
                "data_theft_departing_users",
                "security_policy_violations_departing",
            ],
            "setup_requirements": [
                "Microsoft Purview connector to Azure AD configured",
                "Azure AD audit logs enabled",
            ],
        },
        {
            "id": "azure_ad_risky_sign_in",
            "name": "Azure AD – Risky Sign-In",
            "source": "Azure Active Directory Identity Protection",
            "description": (
                "Identity Protection signals indicating unusual or risky authentication "
                "events such as anonymous IP usage, atypical travel, or leaked credentials. "
                "Combined with file activity these signals contribute to insider risk scores."
            ),
            "data_fields": ["user_id", "sign_in_risk_level", "risk_detail", "timestamp"],
            "policies_triggered": ["general_data_leaks", "security_policy_violations_general"],
            "setup_requirements": [
                "Azure AD Identity Protection P2 licence",
                "Insider risk integration with Identity Protection enabled",
            ],
        },
        {
            "id": "azure_ad_privilege_escalation",
            "name": "Azure AD – Privilege Escalation",
            "source": "Azure Active Directory",
            "description": (
                "Signals from Azure AD Privileged Identity Management (PIM) or audit logs "
                "indicating that a user has been granted elevated permissions outside normal "
                "approval workflows, potentially indicating insider threat activity."
            ),
            "data_fields": ["user_id", "role_assigned", "assignment_type", "approver", "timestamp"],
            "policies_triggered": [
                "security_policy_violations_general",
                "data_leaks_priority_users",
            ],
            "setup_requirements": [
                "Azure AD PIM configured",
                "Audit log streaming to Microsoft Purview enabled",
            ],
        },
    ]


def get_risk_indicators() -> Dict[str, Any]:
    """Return categorised risk indicators used in insider risk policy scoring."""
    return {
        "file_activity": {
            "description": "Indicators related to file operations across Microsoft 365 workloads and endpoints.",
            "indicators": [
                {
                    "id": "sharepoint_download_volume",
                    "name": "SharePoint/OneDrive Download Volume",
                    "description": "Unusually high volume of file downloads from SharePoint or OneDrive.",
                    "weight": "high",
                    "workloads": ["SharePoint", "OneDrive"],
                },
                {
                    "id": "file_copy_removable_media",
                    "name": "File Copy to Removable Media",
                    "description": "Files copied to USB drives or other removable storage devices.",
                    "weight": "high",
                    "workloads": ["Devices"],
                },
                {
                    "id": "file_rename_obfuscation",
                    "name": "File Rename Obfuscation",
                    "description": (
                        "Files renamed to obscure content type (e.g., renaming .docx to .jpg) "
                        "before transfer, suggesting deliberate evasion."
                    ),
                    "weight": "high",
                    "workloads": ["Devices", "SharePoint", "OneDrive"],
                },
                {
                    "id": "bulk_file_deletion",
                    "name": "Bulk File Deletion",
                    "description": "Mass deletion of files from SharePoint, OneDrive, or local storage.",
                    "weight": "high",
                    "workloads": ["SharePoint", "OneDrive", "Devices"],
                },
                {
                    "id": "sensitive_file_access_out_of_role",
                    "name": "Sensitive File Access Outside Role",
                    "description": "Access to document libraries or SharePoint sites unrelated to the user's job role.",
                    "weight": "medium",
                    "workloads": ["SharePoint", "OneDrive"],
                },
            ],
        },
        "email_activity": {
            "description": "Indicators related to email communications and attachments in Exchange Online.",
            "indicators": [
                {
                    "id": "email_to_personal_account",
                    "name": "Email Sent to Personal Email Account",
                    "description": "Emails with attachments sent from corporate account to known personal email domains.",
                    "weight": "high",
                    "workloads": ["Exchange"],
                },
                {
                    "id": "bulk_email_external",
                    "name": "Bulk Email with Attachments to External Recipients",
                    "description": "Large number of emails with attachments sent to external recipients within a short window.",
                    "weight": "high",
                    "workloads": ["Exchange"],
                },
                {
                    "id": "sensitive_email_forwarding_rule",
                    "name": "Auto-Forward Rule to External Address",
                    "description": "Creation of inbox rules that automatically forward emails to an external address.",
                    "weight": "high",
                    "workloads": ["Exchange"],
                },
                {
                    "id": "email_with_sensitive_labels",
                    "name": "Emailing Sensitivity-Labelled Content",
                    "description": "Sending emails containing documents with high-sensitivity labels to external recipients.",
                    "weight": "medium",
                    "workloads": ["Exchange"],
                },
            ],
        },
        "cloud_storage_activity": {
            "description": "Indicators related to uploads to cloud storage services.",
            "indicators": [
                {
                    "id": "upload_personal_cloud_storage",
                    "name": "Upload to Personal Cloud Storage",
                    "description": (
                        "Files uploaded to personal cloud storage services such as personal "
                        "Dropbox, Google Drive, or iCloud from a managed device."
                    ),
                    "weight": "high",
                    "workloads": ["Devices"],
                },
                {
                    "id": "upload_non_sanctioned_service",
                    "name": "Upload to Non-Sanctioned File-Sharing Service",
                    "description": "Files uploaded to services not approved by the organisation's IT policy.",
                    "weight": "high",
                    "workloads": ["Devices"],
                },
                {
                    "id": "public_link_creation",
                    "name": "Public Sharing Link Creation",
                    "description": "Creation of anonymous or anyone-with-link sharing links for sensitive documents.",
                    "weight": "medium",
                    "workloads": ["SharePoint", "OneDrive"],
                },
            ],
        },
        "endpoint_activity": {
            "description": "Indicators from Microsoft Defender for Endpoint on managed devices.",
            "indicators": [
                {
                    "id": "antivirus_disabled",
                    "name": "Antivirus or EDR Disabled",
                    "description": "User disables Windows Defender or endpoint detection and response agent.",
                    "weight": "high",
                    "workloads": ["Devices"],
                },
                {
                    "id": "unauthorised_app_install",
                    "name": "Unauthorised Application Installation",
                    "description": "Installation of software not in the approved application catalogue.",
                    "weight": "medium",
                    "workloads": ["Devices"],
                },
                {
                    "id": "risky_browser_visit",
                    "name": "Risky Browser Site Visit",
                    "description": "Navigation to website categories flagged as high-risk (dark web, data brokers).",
                    "weight": "medium",
                    "workloads": ["Devices"],
                },
                {
                    "id": "print_sensitive_document",
                    "name": "Print Sensitive Document",
                    "description": "Printing of documents classified as confidential or higher sensitivity.",
                    "weight": "medium",
                    "workloads": ["Devices"],
                },
            ],
        },
        "communication_activity": {
            "description": "Indicators related to Microsoft Teams messages and other communications.",
            "indicators": [
                {
                    "id": "teams_sensitive_content_share",
                    "name": "Sensitive Content Shared in Teams",
                    "description": "Sharing of files or messages containing sensitive information types via Teams channels or chats.",
                    "weight": "medium",
                    "workloads": ["Teams"],
                },
                {
                    "id": "negative_sentiment_message",
                    "name": "Negative Sentiment Communication",
                    "description": (
                        "Messages containing language associated with frustration, threats, "
                        "or intent to harm the organisation detected through communication analysis."
                    ),
                    "weight": "medium",
                    "workloads": ["Teams", "Exchange"],
                },
                {
                    "id": "competitor_mention",
                    "name": "Competitor Mention in Internal Communication",
                    "description": "References to named competitor organisations in internal messages or emails.",
                    "weight": "low",
                    "workloads": ["Teams", "Exchange"],
                },
            ],
        },
    }


def get_investigation_workflow() -> Dict[str, Any]:
    """Return the insider risk investigation workflow: alerts → cases → actions."""
    return {
        "overview": (
            "Microsoft Purview Insider Risk Management uses a three-stage investigation workflow: "
            "alerts are generated by policy matches, analysts triage alerts and escalate significant "
            "ones to cases, and case owners take remediation actions. Role-based access controls "
            "separate triage, investigation, and administrative functions."
        ),
        "stages": {
            "alerts": {
                "description": (
                    "Alerts are automatically generated when a user's activity matches the "
                    "conditions and thresholds defined in an insider risk policy. Each alert "
                    "includes a risk score, contributing indicators, and a timeline view."
                ),
                "statuses": ["Needs review", "Active", "Dismissed", "Resolved"],
                "triage_actions": [
                    "Review alert details and risk score",
                    "Examine contributing risk indicators",
                    "View user activity timeline",
                    "Check correlated DLP and sensitivity label events",
                    "Dismiss alert if false positive with documented reason",
                    "Escalate to case if further investigation is warranted",
                ],
                "roles_required": ["Insider Risk Management Analysts", "Insider Risk Management Investigators"],
                "sla_guidance": {
                    "high_severity": "Review within 24 hours",
                    "medium_severity": "Review within 72 hours",
                    "low_severity": "Review within 7 days",
                },
            },
            "cases": {
                "description": (
                    "Cases are opened when an alert requires in-depth investigation beyond "
                    "initial triage. Cases provide access to the full user activity log, "
                    "content explorer for evidence review, and collaboration tools for "
                    "working with HR, legal, and other stakeholders."
                ),
                "statuses": ["Active", "Under investigation", "Pending review", "Closed – benign", "Closed – confirmed violation"],
                "investigation_actions": [
                    "Review full user activity across all workloads",
                    "Use Content Explorer to inspect specific files involved",
                    "Add notes and evidence attachments to the case",
                    "Assign case to specific investigator",
                    "Share case with HR or legal collaborators",
                    "Request additional evidence (e-discovery hold)",
                    "Escalate to Advanced eDiscovery for legal hold",
                ],
                "evidence_sources": [
                    "Activity explorer timeline",
                    "File and email content (Content Explorer)",
                    "Azure AD sign-in logs",
                    "Endpoint activity logs",
                    "DLP policy match details",
                    "HR connector event data",
                ],
                "roles_required": ["Insider Risk Management Investigators"],
            },
            "actions": {
                "description": (
                    "Once an investigation is complete, case owners can take a range of "
                    "remediation and administrative actions directly from the case interface "
                    "or by coordinating with other teams."
                ),
                "remediation_actions": [
                    {
                        "action": "Send notice to user",
                        "description": "Send a customisable email notice to the user informing them of the policy violation.",
                        "automation": "Supported via notice templates",
                    },
                    {
                        "action": "Escalate to Advanced eDiscovery",
                        "description": "Place a legal hold on the user's content and escalate the case to the eDiscovery team.",
                        "automation": "Supported with case transfer",
                    },
                    {
                        "action": "Revoke access",
                        "description": "Coordinate with IT to revoke the user's access to specific resources or systems.",
                        "automation": "Manual – requires IT team coordination",
                    },
                    {
                        "action": "Terminate session",
                        "description": "Force sign-out of all active sessions using Azure AD Conditional Access.",
                        "automation": "Supported via Azure AD integration",
                    },
                    {
                        "action": "Add to restricted activities group",
                        "description": "Add the user to an Azure AD group that enforces additional DLP restrictions.",
                        "automation": "Supported via adaptive protection",
                    },
                    {
                        "action": "Refer to HR",
                        "description": "Formally refer the case findings to the HR team for disciplinary review.",
                        "automation": "Manual – documented in case notes",
                    },
                    {
                        "action": "Refer to legal",
                        "description": "Escalate to legal counsel, particularly when criminal activity is suspected.",
                        "automation": "Manual – documented in case notes",
                    },
                    {
                        "action": "Close case as benign",
                        "description": "Close the case with a documented finding that the activity was benign or a false positive.",
                        "automation": "Supported with closure reason templates",
                    },
                ],
                "adaptive_protection": {
                    "description": (
                        "Adaptive Protection integrates Insider Risk Management risk levels with "
                        "DLP and Conditional Access policies, automatically applying stricter "
                        "controls to users with elevated insider risk scores without manual intervention."
                    ),
                    "risk_levels": ["Minor", "Moderate", "Elevated"],
                    "supported_policies": ["DLP", "Conditional Access"],
                    "requirements": [
                        "Insider Risk Management licence",
                        "DLP policies configured with adaptive protection conditions",
                        "Conditional Access policies configured for risky users",
                    ],
                },
                "roles_required": [
                    "Insider Risk Management Investigators",
                    "Insider Risk Management Admins",
                ],
            },
        },
        "rbac_roles": {
            "Insider Risk Management": "Full access to all insider risk features including policy management.",
            "Insider Risk Management Admins": "Create and manage policies, configure settings, view analytics.",
            "Insider Risk Management Analysts": "Triage and manage alerts, view cases, limited activity access.",
            "Insider Risk Management Investigators": "Full case access including content and evidence review.",
            "Insider Risk Management Auditors": "Read-only access to all insider risk data for audit purposes.",
        },
        "privacy_controls": {
            "anonymisation": (
                "By default, display names in the insider risk management portal are anonymised "
                "using pseudonyms. Authorised investigators can de-anonymise users when required "
                "for confirmed investigations."
            ),
            "notice_templates": (
                "Organisations can configure employee notice templates that are displayed "
                "or sent when monitoring is active, supporting transparency obligations."
            ),
            "audit_log": (
                "All actions taken within Insider Risk Management are logged in the Microsoft "
                "Purview audit log for compliance and accountability purposes."
            ),
        },
    }

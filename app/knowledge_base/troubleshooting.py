"""Troubleshooting guide knowledge base for Microsoft Purview Policy Simulator."""
from typing import Any, Dict, List


def get_troubleshooting_guide() -> Dict[str, Any]:
    """Return a comprehensive troubleshooting guide organised by issue category."""
    return {
        "dlp_issues": _get_dlp_issues(),
        "label_issues": _get_label_issues(),
        "policy_conflicts": _get_policy_conflicts(),
        "insider_risk_issues": _get_insider_risk_issues(),
        "retention_issues": _get_retention_issues(),
        "performance_issues": _get_performance_issues(),
    }


def _get_dlp_issues() -> List[Dict[str, Any]]:
    """Return common DLP issues with symptoms, causes, and solutions."""
    return [
        {
            "id": "dlp_policy_not_matching",
            "title": "DLP Policy Not Matching Expected Content",
            "symptoms": [
                "Sensitive content is shared without triggering a policy tip or alert",
                "DLP reports show zero matches for a recently created policy",
                "Test emails containing credit card numbers are not blocked",
            ],
            "causes": [
                "Policy is in simulation (test) mode and not enforcing actions",
                "Policy has not yet propagated to all workloads (up to 24 hours)",
                "Sensitive information type confidence threshold is set too high",
                "Policy scope excludes the location where the content resides",
                "User performing the test is in an excluded group or role",
                "Content does not meet the minimum instance count requirement",
            ],
            "solutions": [
                "Verify policy mode is set to 'Turn it on right away' in the compliance portal",
                "Wait up to 24 hours after policy creation before testing",
                "Lower the confidence threshold on the sensitive information type rule",
                "Review policy locations and ensure Exchange/SharePoint/Teams are included",
                "Check policy exceptions for user or group exclusions",
                "Reduce the minimum instance count to 1 for initial testing",
                "Use the DLP policy simulation feature to validate matches before enforcement",
            ],
            "diagnostics": [
                "Review the DLP activity explorer for the relevant time period",
                "Use the 'Test your DLP policy' feature in the compliance portal",
                "Check the policy details page for propagation status indicators",
                "Run a Content Search in eDiscovery to verify the content is discoverable",
            ],
            "references": [
                "Create, test, and tune a DLP policy – Microsoft Learn",
                "DLP policy conditions, exceptions, and actions reference",
            ],
        },
        {
            "id": "dlp_false_positives",
            "title": "DLP Policy Generating Excessive False Positives",
            "symptoms": [
                "Users receive frequent policy tips for content that is not sensitive",
                "High volume of DLP alerts that are consistently dismissed",
                "Business processes are being blocked inappropriately",
                "Users bypass policy tips routinely without justification",
            ],
            "causes": [
                "Sensitive information type pattern is too broad",
                "Confidence level is set too low, generating low-accuracy matches",
                "Policy applies to locations where non-sensitive data resides",
                "Instance count is set to 1, triggering on incidental matches",
                "No exclusion for internal-only sharing scenarios",
            ],
            "solutions": [
                "Increase the confidence threshold for sensitive information types (recommended: high confidence)",
                "Increase the minimum instance count to require multiple occurrences",
                "Add exceptions for trusted domains or internal sharing scenarios",
                "Use trainable classifiers instead of keyword-only rules for better accuracy",
                "Enable user override with justification to reduce friction for legitimate activity",
                "Scope the policy to specific SharePoint sites or groups rather than all locations",
                "Run the policy in simulation mode for 30 days to measure false positive rate",
            ],
            "diagnostics": [
                "Export DLP alert data and analyse dismissed-to-acted ratio",
                "Review activity explorer to identify patterns in false positive content",
                "Use the policy simulation report to preview match rates before enforcement",
            ],
            "references": [
                "Fine-tuning DLP policies to reduce false positives – Microsoft Learn",
                "Sensitive information type accuracy tuning guide",
            ],
        },
        {
            "id": "dlp_endpoint_not_enforcing",
            "title": "DLP Endpoint Policies Not Enforcing on Devices",
            "symptoms": [
                "Files can be copied to USB drives despite an endpoint DLP policy",
                "No endpoint DLP alerts appear in the activity explorer",
                "Policy tip is not displayed when users attempt restricted actions",
            ],
            "causes": [
                "Microsoft Defender for Endpoint is not onboarded or is not reporting",
                "Endpoint DLP is not enabled in the compliance portal settings",
                "Device is not enrolled in Microsoft Intune or is not Azure AD joined",
                "Windows version does not meet the minimum requirement (Windows 10 20H2+)",
                "The onboarding package has not been deployed to the device",
                "DLP policy does not include the Devices location",
            ],
            "solutions": [
                "Verify devices are onboarded to Microsoft Defender for Endpoint",
                "Enable Endpoint DLP in the compliance portal under Settings > Endpoint DLP",
                "Ensure devices are Azure AD joined or hybrid Azure AD joined",
                "Check the device list in Defender for Endpoint for onboarding status",
                "Deploy the Endpoint DLP onboarding package via Intune or Group Policy",
                "Add the Devices location to the DLP policy scope",
                "Confirm Windows version is 10 1809 or later (20H2+ recommended)",
            ],
            "diagnostics": [
                "Check device onboarding status in Microsoft Defender for Endpoint",
                "Review the Endpoint DLP diagnostics page in the compliance portal",
                "Test with a known sensitive file on an onboarded device",
                "Check Windows Event Viewer for DLP-related events",
            ],
            "references": [
                "Get started with Endpoint data loss prevention – Microsoft Learn",
                "Onboard devices to Microsoft Defender for Endpoint",
            ],
        },
        {
            "id": "dlp_teams_not_applying",
            "title": "DLP Policy Not Applying in Microsoft Teams",
            "symptoms": [
                "Sensitive files shared in Teams channels are not blocked",
                "No DLP policy tips appear in Teams messages",
                "Sensitive information sent in Teams chat is not detected",
            ],
            "causes": [
                "Teams DLP requires a specific licence (Microsoft 365 E5 or Compliance E5)",
                "Policy does not include the Teams Chat and Channel Messages location",
                "Policy has not propagated to Teams (allow up to 24 hours)",
                "Chat messages in private channels are treated differently to regular channels",
                "Guest or external user activities may fall outside standard DLP scope",
            ],
            "solutions": [
                "Verify the Microsoft 365 E5 Compliance or equivalent licence is assigned",
                "Edit the DLP policy to include 'Teams chat and channel messages' in locations",
                "Wait up to 24 hours after policy update for Teams propagation",
                "Test with internal users in a standard Teams channel before private channels",
                "Review Microsoft documentation for Teams DLP known limitations",
            ],
            "diagnostics": [
                "Check licence assignment in the Microsoft 365 admin centre",
                "Review DLP policy location settings in the compliance portal",
                "Test with a message containing a known sensitive information type",
                "Review the activity explorer filtered to Teams location",
            ],
            "references": [
                "Data loss prevention policies for Microsoft Teams – Microsoft Learn",
                "Teams DLP supported conditions and actions reference",
            ],
        },
    ]


def _get_label_issues() -> List[Dict[str, Any]]:
    """Return sensitivity label deployment, sync, and compatibility issues."""
    return [
        {
            "id": "labels_not_appearing_in_office",
            "title": "Sensitivity Labels Not Appearing in Office Applications",
            "symptoms": [
                "The Sensitivity button is missing from the Home ribbon in Word, Excel, or Outlook",
                "Users cannot apply labels to documents or emails",
                "Labels appear in the compliance portal but not in Office apps",
            ],
            "causes": [
                "The Microsoft Information Protection (MIP) unified labelling client is not installed",
                "Azure Information Protection add-in is enabled and conflicts with built-in labelling",
                "Label policy has not been published to the user or their group",
                "Office application version does not support built-in sensitivity labels",
                "Label policy propagation is still in progress (up to 24 hours)",
            ],
            "solutions": [
                "Ensure Office 365 ProPlus version 1910 or later is installed for built-in labelling",
                "Disable the Azure Information Protection add-in if present in Office COM add-ins",
                "Verify the label policy includes the affected user or their group",
                "Publish the sensitivity label policy in the compliance portal",
                "Wait up to 24 hours after policy publication before testing",
                "Force a policy sync by running: Start-MIPNetworkUpload -OutlookType MSIP_OutlookContext",
                "Check the HKCU registry path for cached label data",
            ],
            "diagnostics": [
                "Run the Microsoft Support and Recovery Assistant (SARA) tool",
                "Check Office telemetry or ULS logs for labelling errors",
                "Verify policy in the Microsoft Purview compliance portal > Information Protection > Label policies",
                "Use the AIP Scanner diagnostics for server-side issues",
            ],
            "references": [
                "Get started with sensitivity labels – Microsoft Learn",
                "Known issues with sensitivity labels in Office apps",
            ],
        },
        {
            "id": "label_sync_delays",
            "title": "Sensitivity Label Policy Sync Delays",
            "symptoms": [
                "New or updated labels take more than a few hours to appear for users",
                "Label changes made in the compliance portal are not reflected in Office apps",
                "Different users in the same policy see different label sets",
            ],
            "causes": [
                "Normal propagation time is up to 24 hours for label policies",
                "Client-side label cache has not been refreshed",
                "Network proxy or firewall is blocking label policy download endpoints",
                "User's Office client has not authenticated recently",
            ],
            "solutions": [
                "Allow up to 24 hours for initial label policy propagation",
                "Force a label refresh by signing out of Office and signing back in",
                "Delete the local label cache: %LocalAppData%\\Microsoft\\MSIP",
                "Verify network access to *.protection.outlook.com and *.aadrm.com",
                "Use PowerShell to check current label policy state: Get-LabelPolicy",
                "Re-publish the label policy to trigger a forced update",
            ],
            "diagnostics": [
                "Run the AIP Client diagnostics: Start-AIPScan -Diagnostic",
                "Check the Office Protected Service connectivity",
                "Review Microsoft Purview compliance portal for policy publication timestamp",
            ],
            "references": [
                "Sensitivity label policy deployment and update timelines – Microsoft Learn",
                "Troubleshooting sensitivity label issues",
            ],
        },
        {
            "id": "label_client_compatibility",
            "title": "Sensitivity Label Client Compatibility Issues",
            "symptoms": [
                "Labels work in Word but not in Outlook, or vice versa",
                "Labels applied on Windows are not visible on macOS or mobile",
                "Encrypted files cannot be opened by certain users or on certain devices",
                "Co-authoring is broken on labelled and encrypted files",
            ],
            "causes": [
                "Office app versions differ across platforms, causing feature gaps",
                "macOS and iOS have different built-in label feature parity to Windows",
                "Encryption settings use permissions not supported by the recipient's client",
                "Co-authoring for encrypted files requires specific Office versions and settings",
                "Legacy AIP client behaviour differs from built-in labelling behaviour",
            ],
            "solutions": [
                "Standardise Office versions across the organisation where possible",
                "Review the sensitivity label feature matrix for each platform (Microsoft Learn)",
                "Enable co-authoring for encrypted files in compliance portal settings",
                "Test label behaviour on each target platform before broad deployment",
                "Use label analytics to identify which apps and platforms are applying labels",
                "Configure label protection settings compatible with the broadest range of clients",
            ],
            "diagnostics": [
                "Review the sensitivity label analytics dashboard in the compliance portal",
                "Test label application and opening on each target platform",
                "Use the Information Protection viewer app for file inspection on Windows",
            ],
            "references": [
                "Sensitivity labels in Office apps – platform feature matrix",
                "Co-authoring for files encrypted with sensitivity labels",
            ],
        },
        {
            "id": "auto_labelling_not_applying",
            "title": "Auto-Labelling Policies Not Applying Labels",
            "symptoms": [
                "Documents in SharePoint are not being auto-labelled",
                "Emails are not receiving automatic sensitivity labels",
                "Auto-labelling simulation shows expected matches but enforcement is not working",
            ],
            "causes": [
                "Auto-labelling policy is still in simulation mode",
                "Policy has not been published or has not propagated",
                "Content does not meet the conditions defined in the auto-label policy",
                "User-applied label with higher priority overrides the auto-label",
                "SharePoint site is not included in the auto-label policy scope",
                "Throughput limits: auto-labelling processes content over time, not immediately",
            ],
            "solutions": [
                "Switch the auto-labelling policy from simulation to enforcement mode",
                "Review the simulation results to confirm condition matches",
                "Verify policy location includes the relevant SharePoint sites or Exchange",
                "Check label priority – user-applied labels of equal or higher priority take precedence",
                "Allow several days for existing content to be processed after policy activation",
                "Use the 'Run policy now' option for SharePoint to process existing content",
            ],
            "diagnostics": [
                "Review auto-labelling simulation report in the compliance portal",
                "Check policy status and propagation in Information Protection > Auto-labelling",
                "Use Content Search to identify unprocessed content",
            ],
            "references": [
                "Automatically apply a sensitivity label to content – Microsoft Learn",
                "Auto-labelling simulation mode and reporting",
            ],
        },
    ]


def _get_policy_conflicts() -> List[Dict[str, Any]]:
    """Return policy conflict resolution guidance."""
    return [
        {
            "id": "dlp_policy_priority_conflict",
            "title": "Multiple DLP Policies Applying Conflicting Actions",
            "symptoms": [
                "A user receives a block action when only a notify action was expected",
                "Policy tips from multiple policies appear simultaneously confusing users",
                "Audit logs show conflicting actions for a single activity",
            ],
            "causes": [
                "Multiple DLP policies match the same content and user",
                "Policies are ordered by priority and the most restrictive rule wins",
                "A lower-priority policy with a block action overrides a higher-priority notify-only policy",
                "Organisation-wide policies interact with team-specific policies unexpectedly",
            ],
            "solutions": [
                "Review policy priority order in the compliance portal – lower number = higher priority",
                "Understand that the most restrictive action applies when multiple rules match",
                "Consolidate overlapping policies into a single policy with ordered rules",
                "Use policy conditions to narrow scope and prevent unintended overlap",
                "Use the 'Stop processing more rules' option in a rule to prevent lower-priority rules from applying",
                "Test policy priority scenarios with the DLP policy simulation tool",
            ],
            "resolution_framework": {
                "principle": "Most restrictive action wins across policies; within a single policy, first matching rule wins unless 'stop processing' is set.",
                "steps": [
                    "Identify all policies that match the content scenario",
                    "List the actions from each matching policy rule",
                    "Determine the most restrictive combination of actions",
                    "Adjust policy priority or rule ordering to achieve desired outcome",
                    "Document intended behaviour for each policy",
                ],
            },
            "references": [
                "DLP policy priority and conflict resolution – Microsoft Learn",
                "Order and precedence of DLP policies",
            ],
        },
        {
            "id": "retention_label_vs_policy_conflict",
            "title": "Retention Label and Retention Policy Conflict",
            "symptoms": [
                "Content is being retained longer than the retention policy specifies",
                "Content subject to a delete policy is not being deleted",
                "Manually applied retention labels appear to override site-wide policies",
            ],
            "causes": [
                "Retention labels take precedence over retention policies when applied explicitly",
                "A longer-retention label overrides a shorter-retention or delete policy",
                "An item is subject to multiple retention policies with different retention periods",
                "A record declaration on a label makes content immutable regardless of policies",
            ],
            "solutions": [
                "Understand the retention conflict resolution principles: explicit overrides implicit, longer retention wins, delete is deferred if retention applies",
                "Audit retention labels applied to content in scope using Content Explorer",
                "Remove conflicting manual retention labels from content if the policy is intended to be authoritative",
                "Review the conflict resolution table in Microsoft documentation",
                "For records, understand that retention cannot be shortened once declared",
            ],
            "resolution_framework": {
                "principle": (
                    "Retention always wins over deletion. Among retention settings, "
                    "the longest retention period applies. Explicit labels take precedence "
                    "over implicit policies. Records cannot be deleted until retention expires."
                ),
                "priority_order": [
                    "1. Retention label explicitly applied by user or auto-label",
                    "2. Retention label applied by default label policy",
                    "3. Retention policy applied to location",
                    "4. No retention – default behaviour applies",
                ],
            },
            "references": [
                "Principles of retention – Microsoft Learn",
                "How retention settings work with content in place",
            ],
        },
        {
            "id": "sensitivity_label_conflict",
            "title": "Sensitivity Label Inheritance and Override Conflicts",
            "symptoms": [
                "Container labels (SharePoint/Teams) are being overridden by document labels",
                "Email labels do not match attachment labels, causing user confusion",
                "Label downgrade protection is blocking legitimate business workflows",
            ],
            "causes": [
                "Document sensitivity labels take precedence over container labels for the document",
                "Label policy settings allow label downgrade without justification",
                "Mandatory labelling requires a label but the default label is inappropriate",
                "Auto-labelling is applying a different label to what users expect",
            ],
            "solutions": [
                "Configure label downgrade justification requirement in the label policy",
                "Set appropriate default labels at the site and document library level",
                "Align container label policies with document label policies for consistency",
                "Educate users on label inheritance and when to override",
                "Review auto-labelling conditions to ensure they align with manual labelling expectations",
                "Use label analytics to identify inconsistent labelling patterns",
            ],
            "resolution_framework": {
                "principle": "Document labels control document protection; container labels control access to the container. They operate independently.",
                "email_attachment_rule": "Email inherits the highest-sensitivity label of its attachments if the label policy is configured to do so.",
            },
            "references": [
                "Sensitivity label priority and conflict resolution",
                "Using sensitivity labels with Microsoft Teams, Microsoft 365 Groups, and SharePoint sites",
            ],
        },
        {
            "id": "conditional_access_dlp_conflict",
            "title": "Conditional Access Policies Conflicting with DLP Enforcement",
            "symptoms": [
                "Users blocked by Conditional Access cannot receive DLP policy tips",
                "Adaptive Protection risk-based restrictions overlap with existing Conditional Access blocks",
                "Guest users are blocked from accessing content they need due to combined policy effects",
            ],
            "causes": [
                "Conditional Access blocks authentication before DLP can evaluate content",
                "Adaptive Protection insider risk levels feed into Conditional Access, compounding restrictions",
                "Multiple policy layers interact in ways not anticipated during design",
            ],
            "solutions": [
                "Map out the full policy stack for a given user scenario before deploying",
                "Use named locations and trusted IP ranges in Conditional Access to reduce friction for managed devices",
                "Test Adaptive Protection integration in audit mode before enabling enforcement",
                "Coordinate DLP and Conditional Access policy owners to align on intent",
                "Use sign-in logs and Conditional Access insights to diagnose access issues",
            ],
            "references": [
                "Adaptive Protection with Conditional Access – Microsoft Learn",
                "Conditional Access overview and deployment guide",
            ],
        },
    ]


def _get_insider_risk_issues() -> List[Dict[str, Any]]:
    """Return common insider risk management issues."""
    return [
        {
            "id": "no_alerts_generated",
            "title": "Insider Risk Policies Not Generating Alerts",
            "symptoms": [
                "No alerts appear in the insider risk management alerts queue",
                "Users with known risky activity are not generating alerts",
                "Policy was created successfully but has been active for days with no results",
            ],
            "causes": [
                "Policy requires a triggering event (e.g., HR connector data) that has not been received",
                "Risk indicators are not enabled in the global insider risk settings",
                "Users are not included in the policy scope",
                "Insufficient licence to generate alerts (requires Microsoft 365 E5 or Compliance add-on)",
                "Audit logging is not enabled for the relevant workloads",
                "Lookback period has not elapsed – initial analytics can take up to 48 hours",
            ],
            "solutions": [
                "Enable the required risk indicators in Settings > Insider Risk Management > Policy indicators",
                "Verify audit logging is enabled via Search > Audit in the compliance portal",
                "Confirm HR connector is configured and data is flowing if using HR-triggered templates",
                "Check that users are in the policy scope (not excluded)",
                "Verify Microsoft 365 E5 or equivalent licence is assigned to in-scope users",
                "Allow 48 hours after policy creation for baseline analysis to complete",
            ],
            "diagnostics": [
                "Review policy analytics in the insider risk management overview",
                "Check HR connector status in Data Connectors",
                "Verify audit log search returns results for the target users and activities",
                "Review policy configuration for scope and indicator selection",
            ],
            "references": [
                "Get started with insider risk management – Microsoft Learn",
                "Insider risk management settings – policy indicators",
            ],
        },
        {
            "id": "hr_connector_not_syncing",
            "title": "HR Connector Not Syncing Data",
            "symptoms": [
                "HR connector shows as connected but no triggering events are generated",
                "Resignation or termination events are not creating monitoring windows",
                "Connector status page shows errors or stale data",
            ],
            "causes": [
                "HR data CSV file format does not match the required schema",
                "The service account used for the connector lacks the required permissions",
                "The scheduled data import job has failed or stopped running",
                "Date formats in the HR export do not match the expected format (YYYY-MM-DD)",
                "Employee IDs in the HR export do not match Azure AD UPNs",
            ],
            "solutions": [
                "Verify the HR CSV schema matches the required format in Microsoft documentation",
                "Check that date fields use the ISO 8601 format (YYYY-MM-DD)",
                "Ensure employee IDs map to Azure AD user principal names",
                "Re-run the import script and check for error output",
                "Review the connector logs in the Data Connectors section of the compliance portal",
                "Re-authenticate the connector service account if tokens have expired",
                "Validate the CSV with a small test file (10 rows) before importing the full file",
            ],
            "diagnostics": [
                "Review Data Connectors > HR Connector > Sync history",
                "Check Azure AD audit logs for the service account used",
                "Validate the CSV file against the schema documentation",
                "Run a manual import and check for error messages",
            ],
            "references": [
                "Set up a connector to import HR data – Microsoft Learn",
                "HR connector data schema reference",
            ],
        },
        {
            "id": "case_evidence_not_available",
            "title": "Case Evidence Not Available for Investigators",
            "symptoms": [
                "Content Explorer in a case shows no files or emails",
                "Investigators cannot view the user activity that triggered the alert",
                "Evidence collection returns 'No results found' for a known active case",
            ],
            "causes": [
                "Investigator role does not have sufficient permissions to view content",
                "Content has been deleted or moved before evidence was collected",
                "Audit retention period for the activity has expired",
                "The compliance portal has not finished indexing the content",
            ],
            "solutions": [
                "Assign the Insider Risk Management Investigators role to the user",
                "Place a preservation hold on the mailbox and OneDrive before the investigation expires",
                "Use Advanced eDiscovery to collect and preserve evidence from the case",
                "Check that the 'Privacy – Show anonymized versions' setting is correctly configured",
                "Request audit log export for activities beyond the standard retention period",
            ],
            "diagnostics": [
                "Verify role assignments in the compliance portal RBAC settings",
                "Check the case status and evidence collection log",
                "Use the Advanced eDiscovery custodian workflow to ensure evidence is preserved",
            ],
            "references": [
                "Investigate insider risk management activities – Microsoft Learn",
                "Evidence collection and content explorer in insider risk cases",
            ],
        },
    ]


def _get_retention_issues() -> List[Dict[str, Any]]:
    """Return common retention policy issues."""
    return [
        {
            "id": "content_deleted_before_retention_expires",
            "title": "Content Being Deleted Before Retention Period Expires",
            "symptoms": [
                "Files in SharePoint are deleted despite an active retention policy",
                "Emails are purged from Exchange before the retention period ends",
                "Users can delete content that should be preserved",
            ],
            "causes": [
                "Retention policy has not propagated to the relevant location",
                "Content is in a location not covered by the retention policy",
                "User permissions allow deletion and preservation is not configured at item level",
                "The Preservation Hold library is not functioning correctly in SharePoint",
                "Retention policy excludes the user or group that owns the content",
            ],
            "solutions": [
                "Verify the retention policy includes the specific SharePoint site or Exchange mailbox",
                "Check that the retention policy mode is 'Retain and delete' or 'Retain only'",
                "Confirm the Preservation Hold library is enabled on the SharePoint site",
                "Wait up to 7 days for retention policies to propagate to all SharePoint sites",
                "Use the Content Search tool to verify the policy is applied to the content",
                "For Exchange, verify the Managed Folder Assistant is processing the mailbox",
            ],
            "diagnostics": [
                "Run: Get-RetentionCompliancePolicy | Select Name, Mode, Status",
                "Check the Site Collection Features for 'In-Place Records Management'",
                "Review the Preservation Hold library in the SharePoint site",
                "Search the compliance audit log for deletion events on retained content",
            ],
            "references": [
                "How retention works for SharePoint and OneDrive – Microsoft Learn",
                "How retention works for Exchange – Microsoft Learn",
            ],
        },
        {
            "id": "retention_label_not_auto_applying",
            "title": "Retention Labels Not Auto-Applying to Content",
            "symptoms": [
                "Documents in SharePoint do not receive the expected auto-applied retention label",
                "Emails matching keyword conditions are not auto-labelled",
                "Auto-apply policy shows as published but no labels are applied",
            ],
            "causes": [
                "Auto-apply policy has not propagated (allow up to 7 days for SharePoint)",
                "Content does not match the specified conditions (keyword, SIT, or trainable classifier)",
                "The auto-apply policy scope does not include the relevant location",
                "A higher-priority retention label already applied to the content takes precedence",
                "Trainable classifier requires sufficient training data to reach confidence threshold",
            ],
            "solutions": [
                "Allow 7 days for SharePoint auto-labelling to process existing content",
                "Validate conditions using Content Search before configuring the auto-apply policy",
                "Expand the policy scope to include all relevant SharePoint sites and mailboxes",
                "Review and remove higher-priority conflicting labels if applicable",
                "Review trainable classifier accuracy and provide additional training examples",
                "Use the 'Run policy now' option to trigger immediate processing",
            ],
            "diagnostics": [
                "Check the auto-apply policy status in Records Management > Label policies",
                "Run a Content Search with the same conditions used in the auto-apply policy",
                "Review the retention label analytics report",
            ],
            "references": [
                "Automatically apply a retention label – Microsoft Learn",
                "Auto-apply retention label policy configuration reference",
            ],
        },
        {
            "id": "records_cannot_be_deleted",
            "title": "Declared Records Cannot Be Deleted When Expected",
            "symptoms": [
                "Files marked as records cannot be deleted even after the retention period expires",
                "Disposition review is required but reviewers are not receiving notifications",
                "Records in SharePoint show as locked indefinitely",
            ],
            "causes": [
                "Record declaration locks content until explicitly unlocked by an authorised user",
                "Disposition review workflow has not been configured correctly",
                "Reviewers do not have the necessary permissions to approve disposition",
                "The retention period trigger (event-based) has not been initiated",
            ],
            "solutions": [
                "Configure disposition review in the retention label settings before deployment",
                "Assign the Disposition Management role to the appropriate reviewers",
                "For event-based retention, ensure the retention event has been created and associated",
                "Unlock the regulatory record using: Unlock-SensitivityLabeledItem if appropriate",
                "Review the disposition review queue in Records Management > Disposition",
            ],
            "diagnostics": [
                "Check the disposition review queue in the compliance portal",
                "Verify reviewer role assignments",
                "Review the retention event log for event-based label triggers",
            ],
            "references": [
                "Disposition reviews – Microsoft Learn",
                "Event-based retention overview",
            ],
        },
    ]


def _get_performance_issues() -> List[Dict[str, Any]]:
    """Return performance impact mitigation guidance."""
    return [
        {
            "id": "dlp_policy_impacting_email_flow",
            "title": "DLP Policies Impacting Email Delivery Latency",
            "symptoms": [
                "Email delivery is delayed by several minutes after DLP policy deployment",
                "Users report Outlook is slow when composing emails with attachments",
                "Mail flow rules are queuing messages for longer than expected",
            ],
            "causes": [
                "DLP policy is scanning large attachments in email flow",
                "Multiple DLP rules are applied sequentially to each message",
                "Complex regular expressions in custom sensitive information types are slow to evaluate",
                "The number of active DLP policies exceeds recommended limits",
            ],
            "solutions": [
                "Optimise custom sensitive information type regular expressions for performance",
                "Consolidate multiple DLP policies for Exchange into a single policy with ordered rules",
                "Set appropriate file size limits for DLP scanning in Exchange transport rules",
                "Exclude low-risk senders or domains from DLP evaluation where appropriate",
                "Monitor Exchange mail flow latency using the Exchange admin centre transport reports",
                "Use the 'Not to' condition to exclude internal-only traffic from heavy scanning",
            ],
            "benchmarks": {
                "recommended_max_policies_per_workload": 50,
                "recommended_max_rules_per_policy": 100,
                "scan_size_limit_recommendation_mb": 30,
            },
            "references": [
                "DLP policy performance best practices – Microsoft Learn",
                "Exchange Online mail flow best practices",
            ],
        },
        {
            "id": "sharepoint_crawl_performance",
            "title": "Sensitivity Label Scanning Impacting SharePoint Performance",
            "symptoms": [
                "SharePoint search crawl is slower after deploying auto-labelling policies",
                "Large document libraries take days to be processed by auto-labelling",
                "SharePoint site performance degrades after enabling Information Protection",
            ],
            "causes": [
                "Auto-labelling requires re-crawling all existing content in SharePoint",
                "Trainable classifiers require more processing resources than keyword-based rules",
                "A very large number of files are being processed simultaneously",
                "Information Protection scanner is competing with normal SharePoint activity",
            ],
            "solutions": [
                "Schedule auto-labelling 'Run policy now' during off-peak hours",
                "Prioritise auto-labelling on high-risk sites first, then expand progressively",
                "Use keyword-based conditions before trainable classifiers for better performance",
                "Monitor SharePoint health in the Microsoft 365 admin centre service health dashboard",
                "Break very large auto-labelling policies into smaller scoped policies",
            ],
            "benchmarks": {
                "auto_label_processing_rate_approx_files_per_day": 25000,
                "recommended_initial_scope": "Start with up to 10 high-priority sites",
            },
            "references": [
                "Auto-labelling for SharePoint performance considerations – Microsoft Learn",
                "Microsoft 365 compliance scalability and performance guidance",
            ],
        },
        {
            "id": "endpoint_dlp_performance",
            "title": "Endpoint DLP Causing Performance Issues on Devices",
            "symptoms": [
                "Devices are slow after enabling Endpoint DLP",
                "File copy operations have noticeable latency",
                "Users report high CPU usage from MsSense.exe (Defender for Endpoint sensor)",
            ],
            "causes": [
                "Endpoint DLP scans file contents on write operations",
                "Too many file types are included in the monitoring scope",
                "A large number of sensitive information types are configured for endpoint scanning",
                "Antivirus and DLP scanning are both running on the same file simultaneously",
            ],
            "solutions": [
                "Limit endpoint DLP to specific high-risk file types (e.g., .docx, .xlsx, .pdf)",
                "Reduce the number of sensitive information types evaluated on endpoints",
                "Ensure antivirus exclusions are correctly configured to avoid double-scanning",
                "Use the 'Audit only' mode for new policies before switching to enforcement",
                "Upgrade device hardware that does not meet Defender for Endpoint recommended specs",
                "Tune the Endpoint DLP sensitivity to reduce background scanning frequency",
            ],
            "benchmarks": {
                "recommended_max_sit_per_endpoint_policy": 10,
                "minimum_recommended_ram_gb": 8,
                "minimum_recommended_os": "Windows 10 20H2",
            },
            "references": [
                "Endpoint DLP performance tuning – Microsoft Learn",
                "Microsoft Defender for Endpoint hardware requirements",
            ],
        },
        {
            "id": "compliance_portal_slow",
            "title": "Microsoft Purview Compliance Portal Performance",
            "symptoms": [
                "Content Search queries take a very long time to return results",
                "Activity Explorer is slow to load or times out",
                "Large eDiscovery exports fail or take excessively long",
            ],
            "causes": [
                "Content Search scope is too broad (all locations, no date range filter)",
                "Activity Explorer query spans a very large date range with many users",
                "eDiscovery export size exceeds portal thresholds",
                "Many simultaneous Content Searches are running",
            ],
            "solutions": [
                "Narrow Content Search scope with date ranges, specific locations, and precise keywords",
                "Filter Activity Explorer by specific user, activity type, and date range",
                "Use eDiscovery export limits: keep individual exports under 2 TB",
                "Stagger large Content Search operations across different time windows",
                "Use the Compliance portal PowerShell SDK for large-scale data operations",
                "Monitor Microsoft 365 service health for any platform-wide performance incidents",
            ],
            "references": [
                "Content Search limits and performance – Microsoft Learn",
                "eDiscovery export best practices and limits",
            ],
        },
    ]

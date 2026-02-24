"""Architecture reference knowledge base for Microsoft Purview Policy Simulator."""
from typing import Any, Dict, List


def get_architecture_reference() -> Dict[str, Any]:
    """Return a comprehensive architecture reference for Microsoft Purview."""
    return {
        "overview": _get_overview(),
        "data_classification_pipeline": _get_data_classification_pipeline(),
        "service_dependencies": _get_service_dependencies(),
        "deployment_checklist": _get_deployment_checklist(),
        "configuration_checklist": _get_configuration_checklist(),
        "integration_points": _get_integration_points(),
    }


def _get_overview() -> Dict[str, Any]:
    """Return the Purview architecture overview."""
    return {
        "description": (
            "Microsoft Purview is a unified data governance, risk, and compliance platform that "
            "spans information protection, data loss prevention, insider risk management, records "
            "management, eDiscovery, and audit capabilities. It operates as a cloud-native service "
            "hosted in Microsoft 365, with enforcement agents deployed into Microsoft 365 workloads "
            "and on-premises environments through connectors and the Information Protection scanner."
        ),
        "core_pillars": {
            "know_your_data": (
                "Data discovery, classification, and labelling using sensitive information types, "
                "trainable classifiers, and sensitivity labels to understand where sensitive data "
                "lives across on-premises, cloud, and third-party environments."
            ),
            "protect_your_data": (
                "Sensitivity labels with encryption, access control, and content marking applied "
                "to files, emails, containers, and meetings to protect data wherever it travels."
            ),
            "prevent_data_loss": (
                "Data Loss Prevention (DLP) policies that detect and respond to risky or "
                "non-compliant sharing of sensitive content across Exchange, SharePoint, OneDrive, "
                "Teams, and endpoint devices."
            ),
            "govern_your_data": (
                "Retention policies and labels, records management, and disposition review to "
                "retain content for compliance and delete it when no longer needed."
            ),
            "manage_insider_risk": (
                "Insider Risk Management policies that use behavioural analytics and machine "
                "learning to detect anomalous activity patterns indicative of insider threats."
            ),
            "discover_and_respond": (
                "eDiscovery (Standard and Premium) and audit capabilities for legal hold, "
                "content search, case management, and regulatory investigation support."
            ),
        },
        "deployment_model": {
            "cloud_native": (
                "All policy management, analytics, and portal functions run in Microsoft 365 "
                "cloud services. No on-premises policy management infrastructure is required."
            ),
            "hybrid_support": (
                "On-premises file servers and SharePoint Server environments can be connected "
                "using the Azure Information Protection (AIP) unified labelling scanner, which "
                "discovers, classifies, and labels on-premises content."
            ),
            "multi_cloud": (
                "The Microsoft Purview Data Map supports scanning and cataloguing data assets "
                "in Azure, AWS, Google Cloud, and on-premises SQL Server through registered "
                "data sources and automated scan rules."
            ),
            "endpoint": (
                "Microsoft Defender for Endpoint serves as the agent on Windows 10/11 and "
                "macOS devices for Endpoint DLP enforcement, activity monitoring, and "
                "Insider Risk Management browser signals."
            ),
        },
        "licensing_tiers": {
            "Microsoft_365_E3": [
                "Basic sensitivity labels (manual, no encryption)",
                "Basic DLP (Exchange, SharePoint, OneDrive)",
                "Basic retention policies",
                "Audit (Standard)",
                "eDiscovery (Standard)",
            ],
            "Microsoft_365_E5": [
                "All E3 capabilities",
                "Advanced sensitivity label encryption and auto-labelling",
                "Endpoint DLP",
                "Teams DLP",
                "Insider Risk Management",
                "Communication Compliance",
                "Advanced Audit",
                "eDiscovery (Premium)",
                "Records Management",
                "Adaptive Protection",
            ],
            "Microsoft_Purview_Compliance_E5_Add_on": (
                "Adds E5 compliance capabilities to Microsoft 365 E3 environments."
            ),
        },
    }


def _get_data_classification_pipeline() -> Dict[str, Any]:
    """Return description of the Microsoft Purview data classification pipeline."""
    return {
        "description": (
            "The Microsoft Purview data classification pipeline is a multi-stage process that "
            "discovers, analyses, classifies, and labels content across Microsoft 365 workloads "
            "and connected data sources. The pipeline operates continuously in the cloud and is "
            "also available on-premises through the AIP Scanner."
        ),
        "stages": [
            {
                "stage": 1,
                "name": "Content Discovery",
                "description": (
                    "Content is discovered from connected data sources including Exchange Online, "
                    "SharePoint Online, OneDrive for Business, Teams, Endpoint devices, and "
                    "on-premises file servers. The pipeline triggers on content creation, "
                    "modification, or upload events."
                ),
                "components": [
                    "Microsoft 365 workload connectors",
                    "AIP unified labelling scanner (on-premises)",
                    "Microsoft Defender for Endpoint (devices)",
                    "Third-party data connectors",
                ],
            },
            {
                "stage": 2,
                "name": "Content Extraction",
                "description": (
                    "Text and metadata are extracted from discovered content. Supported file "
                    "formats include Office documents, PDF, text files, images (via OCR), email "
                    "messages, and chat transcripts. Extraction feeds the classification engine."
                ),
                "supported_formats": [
                    "Microsoft Office (Word, Excel, PowerPoint)",
                    "PDF (text extraction and OCR)",
                    "Plain text and CSV",
                    "Email messages (EML, MSG)",
                    "Images (JPEG, PNG, TIFF) via OCR",
                    "ZIP archives (contents extracted recursively)",
                ],
                "ocr_support": "Available for SharePoint Online, OneDrive, Exchange Online, and Endpoint DLP.",
            },
            {
                "stage": 3,
                "name": "Classification",
                "description": (
                    "Extracted content is evaluated against configured classifiers to determine "
                    "whether it contains sensitive information. Classification uses three types "
                    "of classifiers: sensitive information types (SIT), trainable classifiers, "
                    "and exact data match (EDM)."
                ),
                "classifier_types": {
                    "sensitive_information_types": (
                        "Pattern-based classifiers using regular expressions and keyword lists. "
                        "Microsoft provides 300+ built-in SITs covering financial, health, "
                        "identity, and compliance data. Custom SITs can be created."
                    ),
                    "trainable_classifiers": (
                        "Machine learning models trained on sample content to recognise categories "
                        "of information such as source code, HR documents, or legal contracts. "
                        "Microsoft provides pre-trained classifiers and supports custom classifiers."
                    ),
                    "exact_data_match": (
                        "Database-backed matching that compares content against a specific dataset "
                        "of known sensitive values (e.g., a list of employee IDs or customer "
                        "account numbers). Provides high-precision, low-false-positive detection."
                    ),
                    "fingerprinting": (
                        "Document fingerprinting matches content against a template document, "
                        "identifying content that follows the same structure as a known "
                        "sensitive form or template."
                    ),
                },
            },
            {
                "stage": 4,
                "name": "Label Assignment",
                "description": (
                    "Content that matches classification conditions is assigned a sensitivity "
                    "label or retention label. Assignment can be automatic (via auto-labelling "
                    "policies), manual (by the user), or default (by container or policy)."
                ),
                "assignment_types": {
                    "user_applied": "User manually selects a label from the Office app or web interface.",
                    "auto_applied": "Policy automatically applies a label based on content conditions.",
                    "default_label": "A default label is applied to unlabelled content in a location.",
                    "recommended": "The system recommends a label and the user accepts or dismisses it.",
                },
            },
            {
                "stage": 5,
                "name": "Policy Enforcement",
                "description": (
                    "Once content is classified and labelled, enforcement policies evaluate "
                    "actions taken on that content. DLP policies check whether sharing, transfer, "
                    "or access activities violate policy conditions and apply configured actions "
                    "such as block, notify, encrypt, or alert."
                ),
                "enforcement_locations": [
                    "Exchange Online (email flow)",
                    "SharePoint Online (upload, share, download)",
                    "OneDrive for Business (file operations)",
                    "Microsoft Teams (messages and file sharing)",
                    "Endpoint devices (copy, print, upload)",
                    "Fabric and Power BI (report sharing)",
                ],
            },
            {
                "stage": 6,
                "name": "Audit and Analytics",
                "description": (
                    "All classification, labelling, and DLP events are written to the Microsoft "
                    "Purview audit log and made available in Activity Explorer and the DLP "
                    "reports. These signals feed into Insider Risk Management for behavioural "
                    "analytics and risk scoring."
                ),
                "analytics_surfaces": [
                    "Activity Explorer",
                    "Content Explorer",
                    "DLP reports and activity reports",
                    "Insider Risk Management analytics",
                    "Microsoft Defender XDR alerts",
                    "Microsoft Sentinel (via connector)",
                ],
            },
        ],
    }


def _get_service_dependencies() -> List[Dict[str, Any]]:
    """Return a list of services that Microsoft Purview depends on."""
    return [
        {
            "service": "Azure Active Directory (Entra ID)",
            "dependency_type": "Critical",
            "description": (
                "All Microsoft Purview authentication, authorisation, and role-based access "
                "control depends on Azure AD. User identity, group membership, and licence "
                "assignment are resolved from Azure AD. Conditional Access policies integrated "
                "with Purview also require Azure AD."
            ),
            "specific_requirements": [
                "Azure AD P1 for Conditional Access (basic)",
                "Azure AD P2 for Identity Protection and PIM integration",
                "Azure AD audit logs enabled for Insider Risk Management signals",
            ],
        },
        {
            "service": "Microsoft Exchange Online",
            "dependency_type": "Required for email DLP and retention",
            "description": (
                "Exchange Online provides the email workload for DLP policy enforcement on "
                "messages and attachments, sensitivity label application to emails, and "
                "retention policies for mailbox content. The Managed Folder Assistant (MFA) "
                "processes retention and deletion in mailboxes."
            ),
            "specific_requirements": [
                "Exchange Online Plan 1 or 2",
                "Journaling and audit logging enabled",
                "Mail flow rules (transport rules) for DLP enforcement",
            ],
        },
        {
            "service": "Microsoft SharePoint Online",
            "dependency_type": "Required for document DLP and retention",
            "description": (
                "SharePoint Online is the primary document workload for DLP policy enforcement, "
                "sensitivity label auto-labelling, and retention policy application to site "
                "content. The Preservation Hold library mechanism stores retained copies of "
                "deleted or modified content."
            ),
            "specific_requirements": [
                "SharePoint Online Plan 1 or 2",
                "In-Place Records Management site feature enabled",
                "Versioning enabled on document libraries for retention",
            ],
        },
        {
            "service": "Microsoft OneDrive for Business",
            "dependency_type": "Required for personal file DLP and retention",
            "description": (
                "OneDrive for Business extends SharePoint-based DLP and retention policies to "
                "users' personal file storage. OneDrive sync client on endpoint devices also "
                "participates in Endpoint DLP enforcement."
            ),
            "specific_requirements": [
                "OneDrive for Business Plan 1 or 2",
                "Sharing policies configured appropriately",
            ],
        },
        {
            "service": "Microsoft Teams",
            "dependency_type": "Required for Teams DLP",
            "description": (
                "Microsoft Teams chat messages, channel messages, and file shares are subject "
                "to DLP policies when the Teams location is included. Teams meetings and "
                "transcripts are also covered under certain label policies."
            ),
            "specific_requirements": [
                "Microsoft Teams (included in Microsoft 365 plans)",
                "Microsoft 365 E5 or Compliance E5 for Teams DLP",
            ],
        },
        {
            "service": "Microsoft Defender for Endpoint",
            "dependency_type": "Required for Endpoint DLP and Insider Risk browser signals",
            "description": (
                "Microsoft Defender for Endpoint (MDE) is the agent that enables Endpoint DLP "
                "enforcement on managed Windows and macOS devices. MDE also provides browser "
                "activity signals used by Insider Risk Management and the risky browser usage "
                "policy template."
            ),
            "specific_requirements": [
                "Microsoft Defender for Endpoint Plan 2 (included in E5)",
                "Devices onboarded to MDE",
                "Windows 10 20H2+ or macOS 11+",
                "Endpoint DLP enabled in compliance portal settings",
            ],
        },
        {
            "service": "Microsoft Defender for Cloud Apps",
            "dependency_type": "Optional – enhances DLP for third-party cloud apps",
            "description": (
                "Microsoft Defender for Cloud Apps (MDCA) extends DLP policies to third-party "
                "SaaS applications such as Salesforce, Box, Dropbox, and Google Workspace "
                "through the Cloud App Security broker. Required for CASB-integrated DLP."
            ),
            "specific_requirements": [
                "Microsoft Defender for Cloud Apps licence",
                "App connectors configured for target SaaS applications",
                "Microsoft Purview DLP integration with MDCA enabled",
            ],
        },
        {
            "service": "Azure Information Protection (AIP) Service",
            "dependency_type": "Critical for encryption",
            "description": (
                "The Azure Rights Management Service (Azure RMS), which underpins AIP, provides "
                "the encryption and access control capabilities for sensitivity labels. When a "
                "label with encryption is applied, Azure RMS issues a use licence that defines "
                "who can open the content and what they can do with it."
            ),
            "specific_requirements": [
                "Azure RMS service enabled in the tenant",
                "AIP super user feature configured for service accounts that need unrestricted access",
                "AIP connector for on-premises Exchange and SharePoint (if required)",
            ],
        },
        {
            "service": "Microsoft Purview Audit",
            "dependency_type": "Critical for DLP, IRM, and compliance",
            "description": (
                "Microsoft Purview Audit (formerly Office 365 Audit Log) provides the unified "
                "audit trail for all Microsoft 365 activities. DLP alerts, sensitivity label "
                "events, and Insider Risk Management signals all depend on audit log data being "
                "available and correctly retained."
            ),
            "specific_requirements": [
                "Audit logging enabled for the tenant",
                "Audit retention: 90 days (E3), 1 year (E5), 10 years (Advanced Audit add-on)",
                "Audit log search permissions assigned (View-Only Audit Logs role)",
            ],
        },
        {
            "service": "Microsoft Sentinel (optional)",
            "dependency_type": "Optional – SIEM integration",
            "description": (
                "Microsoft Sentinel can ingest Microsoft Purview DLP alerts, Insider Risk "
                "Management alerts, and audit log events via the Microsoft Purview connector "
                "and Office 365 data connector for SIEM-level correlation and automated response."
            ),
            "specific_requirements": [
                "Microsoft Sentinel workspace",
                "Microsoft Purview connector enabled in Sentinel",
                "Appropriate data ingestion costs budgeted",
            ],
        },
    ]


def _get_deployment_checklist() -> List[Dict[str, Any]]:
    """Return a step-by-step deployment checklist for Microsoft Purview."""
    return [
        {
            "phase": 1,
            "name": "Prerequisites and Licensing",
            "steps": [
                {
                    "step": 1,
                    "task": "Verify licences",
                    "detail": "Confirm Microsoft 365 E5 or Purview Compliance E5 licences are assigned to all in-scope users.",
                    "owner": "IT Admin / Licensing",
                    "validation": "Check licence assignment in Microsoft 365 admin centre > Users > Active users.",
                },
                {
                    "step": 2,
                    "task": "Enable Audit Logging",
                    "detail": "Ensure unified audit logging is turned on for the tenant.",
                    "owner": "Compliance Admin",
                    "validation": "Run: Get-AdminAuditLogConfig | Select UnifiedAuditLogIngestionEnabled",
                },
                {
                    "step": 3,
                    "task": "Assign compliance roles",
                    "detail": "Assign Compliance Administrator, DLP Compliance Management, and Records Management roles to appropriate personnel.",
                    "owner": "Global Admin",
                    "validation": "Review role assignments in the compliance portal Permission section.",
                },
                {
                    "step": 4,
                    "task": "Enable Microsoft Defender for Endpoint",
                    "detail": "Onboard devices to MDE if Endpoint DLP or Insider Risk Management is in scope.",
                    "owner": "Security Operations",
                    "validation": "Verify device onboarding status in MDE portal > Device inventory.",
                },
            ],
        },
        {
            "phase": 2,
            "name": "Data Classification Foundation",
            "steps": [
                {
                    "step": 5,
                    "task": "Run Content Explorer baseline",
                    "detail": "Use Content Explorer to understand the current volume and distribution of sensitive data before deploying policies.",
                    "owner": "Compliance Analyst",
                    "validation": "Content Explorer shows data distribution across locations and sensitive info types.",
                },
                {
                    "step": 6,
                    "task": "Configure sensitive information types",
                    "detail": "Create any required custom SITs for organisation-specific data patterns not covered by built-in types.",
                    "owner": "Compliance Admin",
                    "validation": "Test custom SITs using the 'Test' feature in the compliance portal.",
                },
                {
                    "step": 7,
                    "task": "Design sensitivity label taxonomy",
                    "detail": "Define the label hierarchy (Public, General, Confidential, Highly Confidential) aligned to organisational data classification policy.",
                    "owner": "CISO / Compliance Team",
                    "validation": "Label taxonomy reviewed and approved by information security team.",
                },
                {
                    "step": 8,
                    "task": "Create and publish sensitivity labels",
                    "detail": "Create labels in the compliance portal with appropriate encryption, marking, and scope settings. Publish via label policies to pilot users.",
                    "owner": "Compliance Admin",
                    "validation": "Pilot users can see and apply labels in Office applications.",
                },
            ],
        },
        {
            "phase": 3,
            "name": "Information Protection Policies",
            "steps": [
                {
                    "step": 9,
                    "task": "Deploy sensitivity labels organisation-wide",
                    "detail": "Expand label policy scope from pilot to all users after successful pilot validation.",
                    "owner": "Compliance Admin",
                    "validation": "All users can see the label taxonomy in Office applications.",
                },
                {
                    "step": 10,
                    "task": "Configure auto-labelling policies",
                    "detail": "Set up auto-labelling policies in simulation mode, review results, then activate enforcement.",
                    "owner": "Compliance Admin",
                    "validation": "Simulation report shows expected matches with acceptable false positive rate.",
                },
                {
                    "step": 11,
                    "task": "Deploy DLP policies in test mode",
                    "detail": "Create DLP policies for required compliance scenarios and deploy in 'Test without notifications' mode.",
                    "owner": "Compliance Admin",
                    "validation": "DLP activity explorer shows expected matches in test mode.",
                },
                {
                    "step": 12,
                    "task": "Activate DLP enforcement",
                    "detail": "Switch DLP policies from test to 'Turn it on right away' mode after reviewing test results and communicating to users.",
                    "owner": "Compliance Admin / Change Management",
                    "validation": "DLP alerts are generating for expected scenarios; false positive rate is acceptable.",
                },
            ],
        },
        {
            "phase": 4,
            "name": "Retention and Records Management",
            "steps": [
                {
                    "step": 13,
                    "task": "Map retention requirements",
                    "detail": "Document retention requirements per data category, jurisdiction, and regulatory obligation.",
                    "owner": "Legal / Records Manager",
                    "validation": "Retention schedule documented and approved by legal.",
                },
                {
                    "step": 14,
                    "task": "Create retention labels",
                    "detail": "Create retention labels for each retention schedule entry, configuring retention period and disposition behaviour.",
                    "owner": "Compliance Admin",
                    "validation": "Retention labels reflect approved retention schedule.",
                },
                {
                    "step": 15,
                    "task": "Deploy retention policies",
                    "detail": "Apply broad retention policies to Exchange, SharePoint, OneDrive, and Teams to ensure baseline data preservation.",
                    "owner": "Compliance Admin",
                    "validation": "Retention policies show as active in the compliance portal.",
                },
                {
                    "step": 16,
                    "task": "Configure disposition review",
                    "detail": "Set up disposition reviewers and review workflows for content requiring human approval before deletion.",
                    "owner": "Records Manager",
                    "validation": "Test disposition review workflow with sample content.",
                },
            ],
        },
        {
            "phase": 5,
            "name": "Insider Risk Management",
            "steps": [
                {
                    "step": 17,
                    "task": "Configure HR connector",
                    "detail": "Set up the HR data connector with resignation, termination, and optionally PIP event feeds from the HR system.",
                    "owner": "HR Operations / IT Admin",
                    "validation": "HR connector shows active status with recent sync timestamp.",
                },
                {
                    "step": 18,
                    "task": "Enable policy indicators",
                    "detail": "Select the risk indicators relevant to the organisation's risk scenarios in the Insider Risk Management settings.",
                    "owner": "Compliance Admin",
                    "validation": "Required indicators are toggled on in Settings > Policy indicators.",
                },
                {
                    "step": 19,
                    "task": "Create insider risk policies",
                    "detail": "Create policies for priority templates (e.g., data theft by departing users) using the policy wizard.",
                    "owner": "Compliance Admin",
                    "validation": "Policies show as active in the Insider Risk Management policies list.",
                },
                {
                    "step": 20,
                    "task": "Configure Adaptive Protection",
                    "detail": "Enable Adaptive Protection to integrate insider risk levels with DLP policies for dynamic enforcement.",
                    "owner": "Compliance Admin",
                    "validation": "Adaptive Protection dashboard shows risk level distribution.",
                },
            ],
        },
    ]


def _get_configuration_checklist() -> List[Dict[str, Any]]:
    """Return configuration verification steps for Microsoft Purview."""
    return [
        {
            "category": "Audit and Logging",
            "checks": [
                {
                    "check": "Unified audit log enabled",
                    "how_to_verify": "Compliance portal > Audit > Start recording user and admin activity",
                    "powershell": "Get-AdminAuditLogConfig | Select UnifiedAuditLogIngestionEnabled",
                    "expected_result": "True",
                },
                {
                    "check": "Audit retention period configured",
                    "how_to_verify": "Verify Advanced Audit licences for 1-year or 10-year retention",
                    "powershell": "Get-RetentionCompliancePolicy | Where {$_.Type -eq 'TeamsChatRetention'}",
                    "expected_result": "Retention period aligns with legal requirements",
                },
                {
                    "check": "Mailbox auditing enabled",
                    "how_to_verify": "Verify per-mailbox audit logging for high-risk accounts",
                    "powershell": "Get-Mailbox -Identity user@domain.com | Select AuditEnabled",
                    "expected_result": "True for all priority accounts",
                },
            ],
        },
        {
            "category": "Sensitivity Labels",
            "checks": [
                {
                    "check": "Labels published to all users",
                    "how_to_verify": "Compliance portal > Information Protection > Label policies",
                    "powershell": "Get-LabelPolicy | Select Name, Comment",
                    "expected_result": "At least one policy with All Users scope",
                },
                {
                    "check": "Mandatory labelling configured (if required)",
                    "how_to_verify": "Label policy settings > Require users to apply a label",
                    "powershell": "Get-LabelPolicy | Select RequireSensitivityLabelOnContent",
                    "expected_result": "True if mandatory labelling is policy requirement",
                },
                {
                    "check": "Default labels set for SharePoint sites",
                    "how_to_verify": "SharePoint admin centre > Active sites > Default sensitivity label",
                    "powershell": "Get-SPOSite | Select Url, SensitivityLabel",
                    "expected_result": "Appropriate default label applied to sensitive sites",
                },
            ],
        },
        {
            "category": "DLP Policies",
            "checks": [
                {
                    "check": "DLP policies in enforcement mode",
                    "how_to_verify": "Compliance portal > Data loss prevention > Policies > Mode column",
                    "powershell": "Get-DlpCompliancePolicy | Select Name, Mode",
                    "expected_result": "Mode = Enable (not TestWithNotifications or TestWithoutNotifications)",
                },
                {
                    "check": "Endpoint DLP enabled",
                    "how_to_verify": "Compliance portal > Settings > Endpoint DLP settings",
                    "powershell": "Get-DeviceConditionalAccessPolicy",
                    "expected_result": "Endpoint DLP settings configured and active",
                },
                {
                    "check": "DLP alert notifications configured",
                    "how_to_verify": "Each DLP policy > Alert settings > Send alert to admins",
                    "powershell": "Get-DlpComplianceRule | Select Name, AlertProperties",
                    "expected_result": "Alert recipient email addresses populated",
                },
            ],
        },
        {
            "category": "Retention Policies",
            "checks": [
                {
                    "check": "Retention policies active for all workloads",
                    "how_to_verify": "Compliance portal > Information governance > Retention policies",
                    "powershell": "Get-RetentionCompliancePolicy | Select Name, Enabled, ExchangeLocation, SharePointLocation",
                    "expected_result": "Policies active for Exchange, SharePoint, OneDrive, and Teams",
                },
                {
                    "check": "No conflicting retention policies",
                    "how_to_verify": "Review policies for overlapping scopes with different retention periods",
                    "powershell": "Get-RetentionCompliancePolicy | Select Name, RetentionDuration, RetentionAction",
                    "expected_result": "Policies align with the approved retention schedule; no unintended conflicts",
                },
            ],
        },
        {
            "category": "Insider Risk Management",
            "checks": [
                {
                    "check": "HR connector active and syncing",
                    "how_to_verify": "Compliance portal > Data connectors > HR Connector > Status",
                    "powershell": "N/A – check via portal",
                    "expected_result": "Status: Active; last sync within 24 hours",
                },
                {
                    "check": "Policy indicators enabled",
                    "how_to_verify": "Compliance portal > Insider Risk Management > Settings > Policy indicators",
                    "powershell": "N/A – check via portal",
                    "expected_result": "File activity, email activity, and device indicators enabled",
                },
                {
                    "check": "Insider risk RBAC roles assigned",
                    "how_to_verify": "Compliance portal > Permissions > Insider Risk Management roles",
                    "powershell": "Get-RoleGroupMember -Identity 'Insider Risk Management Investigators'",
                    "expected_result": "Appropriate investigators and analysts assigned",
                },
            ],
        },
        {
            "category": "Endpoint DLP",
            "checks": [
                {
                    "check": "Devices onboarded to Defender for Endpoint",
                    "how_to_verify": "Defender portal > Assets > Devices > Onboarding status",
                    "powershell": "N/A – check via Defender portal",
                    "expected_result": "All managed Windows 10/11 and macOS devices showing as active",
                },
                {
                    "check": "Endpoint DLP enabled in compliance portal",
                    "how_to_verify": "Compliance portal > Settings > Endpoint DLP",
                    "powershell": "N/A – check via portal",
                    "expected_result": "Endpoint DLP settings page is accessible and configured",
                },
            ],
        },
    ]


def _get_integration_points() -> Dict[str, Any]:
    """Return a dict of Microsoft Purview integration points by workload."""
    return {
        "exchange": {
            "description": (
                "Exchange Online integration provides DLP enforcement in email flow via transport "
                "rules, sensitivity label application to outgoing emails, and retention policy "
                "enforcement on mailbox content. Integration is native and requires no additional "
                "configuration beyond policy deployment."
            ),
            "capabilities": [
                "DLP policy enforcement on email send and receive",
                "Sensitivity label application and encryption on outbound email",
                "Auto-labelling of emails based on content conditions",
                "Retention hold and deletion of mailbox items",
                "eDiscovery and legal hold on mailboxes",
                "Communication Compliance for policy-violating messages",
            ],
            "configuration_steps": [
                "Enable DLP for Exchange in policy location settings",
                "Publish sensitivity label policies with Exchange scope",
                "Configure Managed Folder Assistant schedule for retention processing",
                "Enable mailbox auditing for all users (or targeted accounts)",
            ],
            "known_limitations": [
                "S/MIME encrypted emails cannot be inspected by DLP",
                "External sender DLP policies have limited action options",
                "Large attachment scanning may introduce mail flow latency",
            ],
        },
        "sharepoint": {
            "description": (
                "SharePoint Online integration covers DLP enforcement on document upload and "
                "sharing, sensitivity label inheritance from site to document, auto-labelling "
                "of existing content, and retention via the Preservation Hold library. "
                "SharePoint is the primary document governance workload."
            ),
            "capabilities": [
                "DLP enforcement on document upload, sharing, and external access",
                "Sensitivity label inheritance from site/library to new documents",
                "Auto-labelling of existing site content",
                "Retention and deletion of site content via Preservation Hold library",
                "Records management and immutable records declaration",
                "eDiscovery content search and hold",
            ],
            "configuration_steps": [
                "Enable DLP for SharePoint in policy location settings",
                "Configure site-level default sensitivity labels in SharePoint admin centre",
                "Enable In-Place Records Management site feature for records",
                "Ensure document library versioning is enabled for retention",
                "Configure sharing policies to align with DLP enforcement",
            ],
            "known_limitations": [
                "Existing content is processed by auto-labelling over time (not instantly)",
                "Password-protected files cannot be scanned for sensitive content",
                "Files in Personal Sites (MySite) are treated as OneDrive",
            ],
        },
        "teams": {
            "description": (
                "Microsoft Teams integration covers DLP enforcement on chat messages, channel "
                "messages, and file sharing. Sensitivity labels can be applied to Teams "
                "and Microsoft 365 Groups to govern site access and sharing settings. "
                "Teams DLP requires Microsoft 365 E5 or equivalent."
            ),
            "capabilities": [
                "DLP enforcement on chat and channel messages",
                "DLP enforcement on files shared in Teams",
                "Sensitivity labels on Teams (container-level governance)",
                "Communication Compliance for Teams messages",
                "Retention policies for Teams chat and channel messages",
                "Insider Risk Management signals from Teams activity",
            ],
            "configuration_steps": [
                "Include Teams Chat and Channel Messages in DLP policy locations",
                "Enable sensitivity labels for Teams and Microsoft 365 Groups",
                "Assign sensitivity labels to Teams during team creation",
                "Configure retention policies targeting Teams chat and channel messages",
                "Set up Communication Compliance policies for Teams if required",
            ],
            "known_limitations": [
                "DLP for Teams requires Microsoft 365 E5 or Compliance E5",
                "External federation messages may not be subject to DLP",
                "GCC and GCC High environments have different feature availability",
                "Bot and connector messages may not be subject to DLP scanning",
            ],
        },
        "devices": {
            "description": (
                "Endpoint DLP integration on Windows 10/11 and macOS devices extends DLP "
                "enforcement to activities that occur outside Microsoft 365 cloud services, "
                "including file copy to USB, print, upload to non-sanctioned cloud services, "
                "and clipboard operations. Microsoft Defender for Endpoint is the agent."
            ),
            "capabilities": [
                "DLP enforcement on copy to USB and removable media",
                "DLP enforcement on file upload to cloud services",
                "DLP enforcement on print to local and network printers",
                "DLP enforcement on clipboard operations",
                "DLP enforcement on Bluetooth file transfer",
                "Browser upload restrictions (Chrome, Edge, Firefox)",
                "Insider Risk Management browser activity signals",
                "Insider Risk Management file activity signals",
            ],
            "configuration_steps": [
                "Onboard devices to Microsoft Defender for Endpoint",
                "Enable Endpoint DLP in compliance portal Settings",
                "Add Devices location to DLP policies",
                "Configure allowed/blocked apps for each DLP action",
                "Set up unallowed browser list for cloud upload restrictions",
                "Configure printer groups for print activity control",
                "Configure removable storage device groups",
            ],
            "known_limitations": [
                "Endpoint DLP requires Windows 10 1809 (20H2 recommended) or macOS 11+",
                "Some DLP actions are not available on macOS (e.g., print restriction)",
                "Endpoint DLP scanning operates on a file-level basis, not real-time stream",
                "VDI environments have specific onboarding requirements",
            ],
        },
        "power_bi": {
            "description": (
                "Microsoft Purview integrates with Power BI (now Microsoft Fabric) to enforce "
                "sensitivity labels on reports, dashboards, and datasets. DLP policies can "
                "detect sensitive information in Power BI semantic models and apply governance "
                "controls."
            ),
            "capabilities": [
                "Sensitivity label application to Power BI items",
                "Label inheritance from data sources to reports",
                "DLP policy enforcement for Power BI content",
                "Information protection audit events for Power BI",
            ],
            "configuration_steps": [
                "Enable sensitivity labels for Power BI in the Fabric admin portal",
                "Publish sensitivity label policies with Power BI scope",
                "Configure DLP policies targeting Power BI if required",
                "Enable mandatory labelling for Power BI items if appropriate",
            ],
            "known_limitations": [
                "DLP for Power BI requires Microsoft 365 E5 Compliance or equivalent",
                "Not all Power BI item types support sensitivity labels",
                "Label inheritance from connected data sources is not always automatic",
            ],
        },
        "third_party_apps": {
            "description": (
                "Microsoft Purview extends governance to third-party SaaS applications through "
                "Microsoft Defender for Cloud Apps (MDCA). DLP policies can be applied to "
                "supported cloud apps including Salesforce, Box, Dropbox, Google Workspace, "
                "and others through the CASB integration."
            ),
            "capabilities": [
                "DLP policy enforcement on supported third-party SaaS apps",
                "Sensitivity label visibility in MDCA cloud app governance",
                "Activity monitoring for third-party app data transfers",
                "Session controls for conditional access app control scenarios",
            ],
            "configuration_steps": [
                "Connect third-party apps to MDCA using app connectors",
                "Enable Microsoft Purview DLP integration in MDCA settings",
                "Extend DLP policies to include connected app locations",
                "Configure session policies in MDCA for real-time control",
            ],
            "known_limitations": [
                "Third-party app DLP requires Microsoft Defender for Cloud Apps licence",
                "Not all third-party apps support DLP enforcement (only connected apps)",
                "Session controls require a supported identity provider and browser",
            ],
        },
        "on_premises": {
            "description": (
                "On-premises file servers and SharePoint Server environments can be connected "
                "to Microsoft Purview using the Azure Information Protection (AIP) unified "
                "labelling scanner. The scanner discovers, classifies, and labels files in "
                "on-premises repositories and reports activity to the compliance portal."
            ),
            "capabilities": [
                "Content discovery and classification in on-premises file shares",
                "Sensitivity label application to on-premises files",
                "Sensitive information type detection in on-premises content",
                "Reporting of on-premises classification activity to compliance portal",
            ],
            "configuration_steps": [
                "Install the AIP unified labelling scanner on a Windows Server",
                "Create a scanner cluster and content scan job in the compliance portal",
                "Configure repository paths for discovery (network shares, SharePoint Server)",
                "Run a discovery scan, review results, then enable enforcement mode",
                "Configure a service account with appropriate permissions to repositories",
                "Schedule regular scans to keep classification current",
            ],
            "known_limitations": [
                "AIP scanner operates on a scheduled scan basis, not real-time",
                "Encrypted files may not be decryptable without AIP super user configuration",
                "Scanner performance is limited by the server hardware and network bandwidth",
                "SharePoint Server 2013+ supported; older versions are not",
            ],
        },
    }

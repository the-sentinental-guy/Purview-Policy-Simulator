"""
Microsoft Purview Policy Knowledge Base
Contains policy templates, configurations, and expected effects
for Data Loss Prevention, Information Protection, and Data Lifecycle Management.
"""

POLICY_TEMPLATES = [
    {
        "id": "dlp_financial_us",
        "name": "U.S. Financial Data Protection",
        "category": "DLP",
        "subcategory": "Financial",
        "description": (
            "Detects and protects U.S. financial data including credit card numbers, "
            "bank account numbers, and routing numbers across Exchange, SharePoint, OneDrive, and Teams."
        ),
        "keywords": [
            "financial", "credit card", "bank account", "routing number", "payment",
            "PCI", "PCI-DSS", "wire transfer", "SWIFT", "IBAN", "debit", "finance"
        ],
        "sensitive_info_types": [
            "Credit Card Number",
            "U.S. Bank Account Number",
            "ABA Routing Number",
            "U.S. Individual Taxpayer Identification Number (ITIN)",
        ],
        "default_actions": ["Notify user", "Block sharing with external users", "Generate incident report"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": True,
        "confidence": 95,
        "expected_effects": [
            "Emails containing credit card numbers are blocked from external recipients.",
            "SharePoint/OneDrive files with financial data are restricted from external sharing.",
            "Teams messages with financial content trigger policy tips to users.",
            "Incident reports are generated in the Microsoft Purview compliance portal.",
            "Users receive policy tip notifications explaining the restriction.",
        ],
    },
    {
        "id": "dlp_pii_us",
        "name": "U.S. Personally Identifiable Information (PII)",
        "category": "DLP",
        "subcategory": "PII",
        "description": (
            "Protects U.S. PII including Social Security Numbers, driver's license numbers, "
            "and passport numbers. Prevents unauthorized sharing across all workloads."
        ),
        "keywords": [
            "PII", "personal information", "personally identifiable", "SSN", "social security",
            "driver license", "passport", "identity", "personal data", "GDPR", "privacy",
            "date of birth", "DOB", "address", "phone number"
        ],
        "sensitive_info_types": [
            "U.S. Social Security Number (SSN)",
            "U.S. Driver's License Number",
            "U.S. Passport Number",
            "U.S. Individual Taxpayer Identification Number (ITIN)",
        ],
        "default_actions": ["Notify user", "Block sharing externally", "Require justification to override"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": True,
        "confidence": 92,
        "expected_effects": [
            "SSNs and driver's license numbers detected in emails trigger blocks to external recipients.",
            "Documents with PII are restricted from anonymous sharing links.",
            "Users can override restrictions by providing a business justification.",
            "All overrides are logged for compliance audit purposes.",
            "Policy tips educate users about PII handling requirements.",
        ],
    },
    {
        "id": "dlp_health_hipaa",
        "name": "U.S. Health Insurance Act (HIPAA)",
        "category": "DLP",
        "subcategory": "Healthcare",
        "description": (
            "Protects Protected Health Information (PHI) to comply with HIPAA. "
            "Detects medical record numbers, health insurance IDs, and other health-related data."
        ),
        "keywords": [
            "HIPAA", "PHI", "health", "medical", "healthcare", "patient", "diagnosis",
            "treatment", "prescription", "insurance", "medical record", "health data",
            "clinical", "hospital", "doctor", "nurse", "EHR", "EMR"
        ],
        "sensitive_info_types": [
            "U.S. Social Security Number (SSN)",
            "International Classification of Diseases (ICD-9)",
            "International Classification of Diseases (ICD-10)",
            "Drug Enforcement Agency (DEA) Number",
        ],
        "default_actions": ["Block sending externally", "Notify compliance team", "Generate audit report"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": True,
        "confidence": 90,
        "expected_effects": [
            "PHI in emails is blocked from leaving the organization.",
            "Compliance team is notified of PHI policy violations.",
            "Detailed audit reports support HIPAA compliance documentation.",
            "Healthcare data is restricted to authorized users only.",
            "All access events to PHI are logged for audit purposes.",
        ],
    },
    {
        "id": "dlp_gdpr",
        "name": "General Data Protection Regulation (GDPR)",
        "category": "DLP",
        "subcategory": "Privacy",
        "description": (
            "Helps comply with GDPR by detecting EU residents' personal data and "
            "enforcing data protection policies across Microsoft 365 services."
        ),
        "keywords": [
            "GDPR", "EU", "European", "personal data", "data subject", "consent",
            "right to erasure", "data protection", "DPA", "privacy", "EU citizens",
            "European Union", "data processing"
        ],
        "sensitive_info_types": [
            "EU Debit Card Number",
            "EU Driver's License Number",
            "EU National Identification Number",
            "EU Passport Number",
            "EU Social Security Number",
            "EU Tax Identification Number",
        ],
        "default_actions": ["Notify user", "Block external sharing", "Notify privacy officer"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": True,
        "confidence": 88,
        "expected_effects": [
            "EU personal data is detected and protected across all M365 workloads.",
            "Privacy officer receives notifications when GDPR-sensitive data is shared.",
            "External sharing of EU personal data is restricted.",
            "Audit logs support GDPR accountability and compliance reporting.",
            "Users receive guidance on GDPR-compliant data handling.",
        ],
    },
    {
        "id": "sensitivity_label_confidential",
        "name": "Confidential Sensitivity Label",
        "category": "Information Protection",
        "subcategory": "Sensitivity Labels",
        "description": (
            "Applies a 'Confidential' label to documents and emails, encrypting content "
            "and restricting access to authorized users within the organization."
        ),
        "keywords": [
            "confidential", "sensitive", "label", "classify", "encryption", "restrict access",
            "internal only", "proprietary", "trade secret", "intellectual property",
            "classification", "mark", "protect document"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Apply encryption", "Add visual markings (watermark, header, footer)", "Restrict forwarding"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams", "Office Apps"],
        "template_available": True,
        "confidence": 93,
        "expected_effects": [
            "Documents labeled 'Confidential' are automatically encrypted.",
            "Visual watermarks and headers identify sensitive content.",
            "Only authorized internal users can access encrypted content.",
            "Forwarding of confidential emails is restricted.",
            "Rights Management protects content even when downloaded.",
        ],
    },
    {
        "id": "sensitivity_label_highly_confidential",
        "name": "Highly Confidential Sensitivity Label",
        "category": "Information Protection",
        "subcategory": "Sensitivity Labels",
        "description": (
            "Applies the highest level of protection, restricting content to specific "
            "individuals with strong encryption and access controls."
        ),
        "keywords": [
            "highly confidential", "top secret", "classified", "restricted", "executives only",
            "board", "merger", "acquisition", "M&A", "legal", "attorney-client", "privileged",
            "HR data", "salary", "compensation", "personnel file"
        ],
        "sensitive_info_types": [],
        "default_actions": [
            "Apply strong encryption",
            "Restrict to named users only",
            "Disable copy/paste/print",
            "Add prominent visual markings",
        ],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams", "Office Apps"],
        "template_available": True,
        "confidence": 91,
        "expected_effects": [
            "Content is encrypted with access limited to specified individuals.",
            "Copy, paste, print, and screenshot capabilities are disabled.",
            "Prominent visual markings indicate highest sensitivity level.",
            "External sharing is completely blocked.",
            "All access attempts are logged in the audit trail.",
        ],
    },
    {
        "id": "retention_policy_general",
        "name": "General Data Retention Policy",
        "category": "Data Lifecycle Management",
        "subcategory": "Retention",
        "description": (
            "Retains content for a defined period and then either deletes it or "
            "triggers a disposition review, helping meet compliance requirements."
        ),
        "keywords": [
            "retention", "retain", "keep", "archive", "delete", "dispose", "lifecycle",
            "records management", "hold", "legal hold", "compliance hold", "eDiscovery",
            "preserve", "purge", "expiry", "expire"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Retain content for specified period", "Delete after retention period", "Trigger disposition review"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": True,
        "confidence": 89,
        "expected_effects": [
            "Content is retained for the specified period regardless of user deletion.",
            "After the retention period, content is permanently deleted.",
            "eDiscovery searches can locate all retained content.",
            "Legal holds prevent deletion of content under litigation.",
            "Disposition review workflow notifies reviewers before permanent deletion.",
        ],
    },
    {
        "id": "dlp_source_code",
        "name": "Source Code Protection",
        "category": "DLP",
        "subcategory": "Intellectual Property",
        "description": (
            "Protects source code and intellectual property from being shared outside "
            "the organization through various channels."
        ),
        "keywords": [
            "source code", "code", "repository", "git", "intellectual property", "IP",
            "proprietary code", "software", "algorithm", "script", "programming",
            "developer", "engineering", "codebase"
        ],
        "sensitive_info_types": [
            "Source Code (custom keyword patterns)",
            "File extensions: .py, .js, .ts, .cs, .java, .cpp, .go",
        ],
        "default_actions": ["Block external sharing", "Notify security team", "Log access"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": False,
        "confidence": 75,
        "expected_effects": [
            "Source code files are blocked from external sharing.",
            "Security team receives alerts when code sharing is attempted.",
            "All source code access events are logged.",
            "Custom keyword dictionaries can be added to improve detection accuracy.",
        ],
    },
    {
        "id": "endpoint_dlp",
        "name": "Endpoint DLP Policy",
        "category": "DLP",
        "subcategory": "Endpoint",
        "description": (
            "Extends DLP protection to Windows endpoints, monitoring and controlling "
            "how sensitive data is used on devices including USB transfers, printing, and clipboard."
        ),
        "keywords": [
            "endpoint", "device", "USB", "removable storage", "print", "clipboard", "copy",
            "laptop", "workstation", "Windows", "device control", "local", "offline",
            "download", "transfer", "removable"
        ],
        "sensitive_info_types": [
            "All configured sensitive information types",
        ],
        "default_actions": ["Block copy to USB", "Block printing", "Block clipboard", "Audit all activities"],
        "workloads": ["Windows 10/11 Endpoints"],
        "template_available": False,
        "confidence": 82,
        "expected_effects": [
            "Sensitive data cannot be copied to USB drives or removable storage.",
            "Printing of sensitive documents is blocked or requires justification.",
            "Clipboard operations with sensitive content are controlled.",
            "All data activities on endpoints are logged for audit.",
            "Users on managed devices receive policy tips for compliance guidance.",
        ],
    },
    {
        "id": "communication_compliance",
        "name": "Communication Compliance Policy",
        "category": "Communication Compliance",
        "subcategory": "Monitoring",
        "description": (
            "Monitors communications for inappropriate content, regulatory violations, "
            "or insider trading using machine learning and keyword matching."
        ),
        "keywords": [
            "communication", "monitor", "surveillance", "inappropriate", "harassment",
            "insider trading", "regulatory", "compliance monitoring", "review",
            "Teams messages", "email monitoring", "conduct", "workplace"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Flag communications for review", "Notify reviewers", "Generate compliance reports"],
        "workloads": ["Exchange Online", "Microsoft Teams"],
        "template_available": True,
        "confidence": 85,
        "expected_effects": [
            "Flagged communications are queued for compliance officer review.",
            "Machine learning models detect inappropriate content patterns.",
            "Detailed reports support regulatory examination requirements.",
            "Reviewers receive notifications for policy-matched communications.",
            "All review actions are logged for audit trail.",
        ],
    },
    {
        "id": "insider_risk_data_theft",
        "name": "Insider Risk - Data Theft by Departing Users",
        "category": "Insider Risk Management",
        "subcategory": "Data Theft",
        "description": (
            "Detects data theft activities by users who are leaving the organization, "
            "such as mass downloads, USB transfers, or unusual email forwarding."
        ),
        "keywords": [
            "insider risk", "insider threat", "departing employee", "resignation", "termination",
            "data theft", "exfiltration", "mass download", "leakage", "leaving",
            "offboarding", "disgruntled", "risk score"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Risk scoring", "Alert security team", "Trigger investigation workflow"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams", "Endpoints"],
        "template_available": True,
        "confidence": 87,
        "expected_effects": [
            "Risk scores are calculated for users on HR termination watchlist.",
            "Unusual download or exfiltration patterns trigger security alerts.",
            "Security teams can investigate risky activities with full activity timeline.",
            "Automated responses can restrict user access when risk threshold is exceeded.",
            "Evidence packages are compiled for HR or legal proceedings.",
        ],
    },
    {
        "id": "dlp_external_email_sharing",
        "name": "Block External Email Sharing of Sensitive Data",
        "category": "DLP",
        "subcategory": "Email",
        "description": (
            "Prevents sensitive data from being sent outside the organization via email, "
            "with configurable override options for business justification."
        ),
        "keywords": [
            "external email", "block email", "email sharing", "send outside", "external",
            "outbound email", "forward", "email exfiltration", "prevent sending",
            "email restriction", "outside organization", "third party"
        ],
        "sensitive_info_types": [
            "Configurable based on requirements",
        ],
        "default_actions": ["Block outbound email", "Allow override with justification", "Notify sender"],
        "workloads": ["Exchange Online"],
        "template_available": False,
        "confidence": 80,
        "expected_effects": [
            "Emails with sensitive content to external recipients are blocked.",
            "Senders receive policy tip notifications explaining the block.",
            "Business justification overrides are logged for review.",
            "Email is held for compliance officer review when override is used.",
            "External recipients are not notified of the policy block.",
        ],
    },
]

CUSTOM_CONFIGURATIONS = [
    {
        "id": "custom_keyword_dict",
        "name": "Custom Keyword Dictionary",
        "description": "Create a custom keyword dictionary with organization-specific terms to detect sensitive content.",
        "when_to_use": "When built-in sensitive info types don't cover your specific terminology.",
        "configuration_steps": [
            "Navigate to Microsoft Purview > Data classification > Classifiers > Trainable classifiers",
            "Create a new keyword dictionary",
            "Upload or type your organization-specific keywords",
            "Test the dictionary against sample content",
            "Associate the dictionary with a DLP policy rule",
        ],
    },
    {
        "id": "custom_sit",
        "name": "Custom Sensitive Information Type (SIT)",
        "description": "Define a custom pattern using regular expressions to detect organization-specific data formats.",
        "when_to_use": "When you need to detect proprietary data formats (employee IDs, project codes, etc.).",
        "configuration_steps": [
            "Navigate to Microsoft Purview > Data classification > Sensitive info types",
            "Create a new custom sensitive info type",
            "Define the primary pattern using regex",
            "Add supporting evidence (keywords, checksum validators)",
            "Set confidence levels and instance count thresholds",
            "Test against sample data before deploying",
        ],
    },
    {
        "id": "trainable_classifier",
        "name": "Trainable Classifier",
        "description": "Use machine learning to classify content based on training examples rather than patterns.",
        "when_to_use": "When content is too complex for patterns (e.g., legal contracts, HR documents, source code).",
        "configuration_steps": [
            "Navigate to Microsoft Purview > Data classification > Classifiers > Trainable classifiers",
            "Choose 'Create trainable classifier'",
            "Upload positive examples (content that matches your category)",
            "The classifier trains on your examples (24-48 hours)",
            "Test and iterate to improve accuracy",
            "Deploy in a policy once accuracy meets your threshold",
        ],
    },
    {
        "id": "policy_tips_customization",
        "name": "Custom Policy Tips",
        "description": "Customize the messages users see when they violate a DLP policy.",
        "when_to_use": "When you want to provide specific guidance or links to internal resources.",
        "configuration_steps": [
            "Edit the DLP policy rule",
            "Navigate to 'User notifications' section",
            "Enable policy tips",
            "Customize the message text with actionable guidance",
            "Add a URL to internal compliance resources if available",
        ],
    },
    {
        "id": "adaptive_protection",
        "name": "Adaptive Protection Integration",
        "description": "Dynamically adjust DLP policy enforcement based on user risk scores from Insider Risk Management.",
        "when_to_use": "When you want stricter controls for high-risk users identified by Insider Risk Management.",
        "configuration_steps": [
            "Ensure Insider Risk Management is configured with appropriate policies",
            "Navigate to DLP policy > Conditions",
            "Add 'User risk level is' condition",
            "Set stricter actions for elevated/high risk users",
            "Configure risk level thresholds in Insider Risk Management settings",
        ],
    },
]

SENSITIVITY_LABEL_CONFIGS = {
    "encryption": {
        "name": "Encryption Settings",
        "options": [
            "Assign permissions now (fixed permissions)",
            "Let users assign permissions (Outlook only)",
            "Double Key Encryption (highest security)",
        ],
    },
    "auto_labeling": {
        "name": "Auto-labeling",
        "description": "Automatically apply labels based on sensitive info types detected in content.",
        "conditions": ["Contains sensitive info type", "Content matches keyword", "Document property matches"],
    },
    "mandatory_labeling": {
        "name": "Mandatory Labeling",
        "description": "Require users to apply a label before saving or sending content.",
    },
}

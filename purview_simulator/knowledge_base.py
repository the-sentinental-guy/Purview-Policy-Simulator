"""
Knowledge base for Microsoft Purview policy templates, configurations,
and their expected effects.

This module contains the structured data that the simulation engine uses
to match user requirements against available Purview capabilities.
"""

# Sensitive information types recognized by Purview
SENSITIVE_INFO_TYPES = {
    "credit_card": {
        "name": "Credit Card Number",
        "category": "financial",
        "keywords": ["credit card", "cc number", "card number", "visa", "mastercard", "amex"],
        "description": "Detects credit card numbers from major card issuers.",
    },
    "ssn": {
        "name": "U.S. Social Security Number (SSN)",
        "category": "pii",
        "keywords": ["ssn", "social security", "social security number"],
        "description": "Detects U.S. Social Security Numbers.",
    },
    "bank_account": {
        "name": "Bank Account Number",
        "category": "financial",
        "keywords": ["bank account", "account number", "routing number", "iban", "swift"],
        "description": "Detects bank account and routing numbers.",
    },
    "passport": {
        "name": "Passport Number",
        "category": "pii",
        "keywords": ["passport", "passport number", "travel document"],
        "description": "Detects passport numbers from various countries.",
    },
    "email": {
        "name": "Email Address",
        "category": "pii",
        "keywords": ["email", "email address", "e-mail"],
        "description": "Detects email addresses.",
    },
    "ip_address": {
        "name": "IP Address",
        "category": "technical",
        "keywords": ["ip address", "ip", "network address", "ipv4", "ipv6"],
        "description": "Detects IPv4 and IPv6 addresses.",
    },
    "health_record": {
        "name": "Health/Medical Record",
        "category": "health",
        "keywords": ["health", "medical", "hipaa", "patient", "diagnosis", "prescription", "phi"],
        "description": "Detects protected health information (PHI).",
    },
    "driver_license": {
        "name": "Driver's License Number",
        "category": "pii",
        "keywords": ["driver license", "drivers license", "driving license", "dl number"],
        "description": "Detects driver's license numbers.",
    },
    "tax_id": {
        "name": "Tax Identification Number",
        "category": "financial",
        "keywords": ["tax id", "tin", "ein", "tax number", "taxpayer"],
        "description": "Detects tax identification numbers.",
    },
    "azure_secret": {
        "name": "Azure Service Credentials",
        "category": "credentials",
        "keywords": ["azure key", "azure secret", "connection string", "sas token",
                     "api key", "api keys", "secret", "secrets", "credential",
                     "credentials", "password", "token", "key vault"],
        "description": "Detects Azure service credentials and secrets.",
    },
    "source_code": {
        "name": "Source Code",
        "category": "intellectual_property",
        "keywords": ["source code", "code", "proprietary code", "algorithm", "software"],
        "description": "Detects source code patterns.",
    },
    "gdpr_personal_data": {
        "name": "GDPR Personal Data",
        "category": "privacy",
        "keywords": ["gdpr", "eu personal data", "european", "data subject", "eu citizen",
                     "personal data", "data protection"],
        "description": "Detects personal data as defined under EU GDPR.",
    },
}

# Locations/workloads where policies can be applied
POLICY_LOCATIONS = {
    "exchange": {
        "name": "Exchange Online (Email)",
        "keywords": ["email", "mail", "exchange", "outlook", "smtp"],
    },
    "sharepoint": {
        "name": "SharePoint Online",
        "keywords": ["sharepoint", "document library", "site"],
    },
    "onedrive": {
        "name": "OneDrive for Business",
        "keywords": ["onedrive", "one drive", "personal storage", "file sync"],
    },
    "teams": {
        "name": "Microsoft Teams",
        "keywords": ["teams", "chat", "teams message", "channel"],
    },
    "devices": {
        "name": "Devices (Endpoint DLP)",
        "keywords": ["device", "endpoint", "laptop", "desktop", "usb", "clipboard",
                     "print", "screen", "local"],
    },
    "power_bi": {
        "name": "Power BI",
        "keywords": ["power bi", "powerbi", "dashboard", "report", "dataset"],
    },
    "on_premises": {
        "name": "On-premises Repositories",
        "keywords": ["on-premises", "on premises", "file server", "on-prem", "local server"],
    },
    "fabric_lakehouse": {
        "name": "Microsoft Fabric and AI Hub",
        "keywords": ["fabric", "lakehouse", "ai hub", "copilot"],
    },
}

# Actions that can be taken by policies
POLICY_ACTIONS = {
    "block": {
        "name": "Block Content",
        "description": "Prevents sharing or sending of content that matches the policy.",
        "keywords": ["block", "prevent", "stop", "deny", "restrict"],
    },
    "block_with_override": {
        "name": "Block with Override",
        "description": "Blocks sharing but allows users to override with a business justification.",
        "keywords": ["block override", "override", "justification", "allow override",
                     "business justification"],
    },
    "encrypt": {
        "name": "Encrypt Content",
        "description": "Applies encryption to content matching the policy.",
        "keywords": ["encrypt", "encryption", "protect", "rights management", "rms"],
    },
    "notify_user": {
        "name": "Notify User (Policy Tip)",
        "description": "Shows a policy tip to users when they handle sensitive content.",
        "keywords": ["notify", "warn", "alert user", "policy tip", "educate", "inform"],
    },
    "notify_admin": {
        "name": "Notify Administrator",
        "description": "Sends an alert to administrators when a policy match occurs.",
        "keywords": ["notify admin", "alert admin", "report", "admin notification", "incident"],
    },
    "audit": {
        "name": "Audit Only",
        "description": "Logs the activity without blocking. Useful for testing policies.",
        "keywords": ["audit", "log", "monitor", "track", "test mode", "detect only"],
    },
    "apply_label": {
        "name": "Apply Sensitivity Label",
        "description": "Automatically applies a sensitivity label to matching content.",
        "keywords": ["label", "sensitivity label", "classify", "tag", "auto-label",
                     "auto label", "classification"],
    },
    "restrict_access": {
        "name": "Restrict Access to Content",
        "description": "Limits who can access the content (e.g., owner only).",
        "keywords": ["restrict access", "limit access", "owner only", "revoke access"],
    },
}

# Built-in policy templates available in Microsoft Purview
POLICY_TEMPLATES = [
    {
        "id": "financial_data_dlp",
        "name": "U.S. Financial Data",
        "category": "data_loss_prevention",
        "description": "Protects U.S. financial data including credit card numbers, bank account "
                       "numbers, and tax identification numbers.",
        "sensitive_info_types": ["credit_card", "bank_account", "tax_id"],
        "default_locations": ["exchange", "sharepoint", "onedrive", "teams"],
        "default_actions": ["block_with_override", "notify_user", "notify_admin"],
        "keywords": ["financial", "credit card", "bank", "payment", "pci", "pci-dss",
                     "finance", "monetary"],
        "expected_effects": [
            "Emails containing financial data will be blocked from external recipients unless "
            "the sender provides a business justification.",
            "Documents with financial data in SharePoint/OneDrive will show sharing restrictions.",
            "Users will receive policy tips when composing messages with financial data.",
            "Administrators will receive incident reports for policy matches.",
        ],
    },
    {
        "id": "pii_protection_dlp",
        "name": "U.S. Personally Identifiable Information (PII)",
        "category": "data_loss_prevention",
        "description": "Protects PII including SSNs, passport numbers, and driver's license "
                       "numbers from being shared externally.",
        "sensitive_info_types": ["ssn", "passport", "driver_license", "email"],
        "default_locations": ["exchange", "sharepoint", "onedrive", "teams"],
        "default_actions": ["block_with_override", "notify_user", "notify_admin"],
        "keywords": ["pii", "personal", "identity", "ssn", "social security", "passport",
                     "personally identifiable"],
        "expected_effects": [
            "External sharing of documents containing PII will be blocked.",
            "Users will see policy tips when editing documents with PII.",
            "Email messages with PII sent externally will be blocked with override option.",
            "Incident reports generated for compliance review.",
        ],
    },
    {
        "id": "hipaa_dlp",
        "name": "U.S. Health Insurance Act (HIPAA)",
        "category": "data_loss_prevention",
        "description": "Helps meet HIPAA compliance by protecting health-related information.",
        "sensitive_info_types": ["health_record", "ssn"],
        "default_locations": ["exchange", "sharepoint", "onedrive", "teams"],
        "default_actions": ["block", "encrypt", "notify_admin"],
        "keywords": ["hipaa", "health", "medical", "patient", "phi", "protected health",
                     "healthcare", "hospital", "clinical"],
        "expected_effects": [
            "Health information will be blocked from external sharing without exception.",
            "Documents with PHI will be automatically encrypted.",
            "Administrators receive alerts on all PHI-related policy matches.",
            "Teams messages containing PHI will be blocked.",
        ],
    },
    {
        "id": "gdpr_dlp",
        "name": "EU General Data Protection Regulation (GDPR)",
        "category": "data_loss_prevention",
        "description": "Protects personal data of EU residents in compliance with GDPR.",
        "sensitive_info_types": ["gdpr_personal_data", "email", "passport"],
        "default_locations": ["exchange", "sharepoint", "onedrive", "teams"],
        "default_actions": ["block_with_override", "encrypt", "notify_user", "notify_admin"],
        "keywords": ["gdpr", "european", "eu", "data protection", "eu citizen",
                     "general data protection", "privacy regulation"],
        "expected_effects": [
            "Personal data of EU residents will be restricted from leaving the organization.",
            "Content with GDPR-regulated data will be encrypted automatically.",
            "Users will receive policy tips about GDPR-sensitive content.",
            "Compliance officers will receive incident reports.",
        ],
    },
    {
        "id": "endpoint_dlp",
        "name": "Endpoint Data Loss Prevention",
        "category": "data_loss_prevention",
        "description": "Prevents sensitive data from being copied, printed, or transferred via "
                       "USB or network share from managed endpoints.",
        "sensitive_info_types": ["credit_card", "ssn", "bank_account", "health_record"],
        "default_locations": ["devices"],
        "default_actions": ["block", "audit", "notify_user"],
        "keywords": ["endpoint", "device", "usb", "copy", "print", "clipboard", "screen capture",
                     "local", "desktop", "laptop", "removable", "bluetooth"],
        "expected_effects": [
            "Copying sensitive files to USB drives will be blocked on managed devices.",
            "Printing documents with sensitive data will be restricted.",
            "Clipboard operations for sensitive content will be audited or blocked.",
            "Users will be notified when attempting restricted endpoint operations.",
        ],
    },
    {
        "id": "sensitivity_labels_auto",
        "name": "Auto-Labeling with Sensitivity Labels",
        "category": "data_protection",
        "description": "Automatically applies sensitivity labels to content based on detected "
                       "sensitive information types.",
        "sensitive_info_types": ["credit_card", "ssn", "health_record", "gdpr_personal_data",
                                 "source_code", "azure_secret"],
        "default_locations": ["exchange", "sharepoint", "onedrive"],
        "default_actions": ["apply_label", "encrypt", "notify_user"],
        "keywords": ["auto label", "auto-label", "sensitivity label", "classify",
                     "classification", "automatic label", "tag", "categorize"],
        "expected_effects": [
            "Documents and emails will be automatically labeled based on their content.",
            "Labeled content will inherit the protection settings of the label (e.g., encryption).",
            "Users will see the applied label and can be educated on handling requirements.",
            "Unlabeled content with sensitive data will receive default labels.",
        ],
    },
    {
        "id": "credential_protection",
        "name": "Credential and Secret Protection",
        "category": "data_loss_prevention",
        "description": "Prevents accidental sharing of credentials, API keys, and secrets.",
        "sensitive_info_types": ["azure_secret"],
        "default_locations": ["exchange", "sharepoint", "onedrive", "teams"],
        "default_actions": ["block", "notify_user", "notify_admin"],
        "keywords": ["credential", "secret", "api key", "password", "token", "connection string",
                     "sas", "key vault", "leak", "exposure"],
        "expected_effects": [
            "Messages and documents containing credentials will be blocked from external sharing.",
            "Users will receive immediate policy tips when credentials are detected.",
            "Incident alerts will be sent to security administrators.",
            "Credentials in Teams messages will be blocked from being sent.",
        ],
    },
    {
        "id": "ip_protection",
        "name": "Intellectual Property Protection",
        "category": "data_protection",
        "description": "Protects proprietary source code, algorithms, and trade secrets.",
        "sensitive_info_types": ["source_code"],
        "default_locations": ["exchange", "sharepoint", "onedrive", "teams", "devices"],
        "default_actions": ["block", "encrypt", "notify_admin"],
        "keywords": ["intellectual property", "trade secret", "proprietary", "source code",
                     "algorithm", "patent", "confidential", "ip protection"],
        "expected_effects": [
            "Source code files will be blocked from external sharing.",
            "Documents classified as IP will be encrypted.",
            "External email attachments containing code will be blocked.",
            "Endpoint DLP will prevent copying IP to removable media.",
        ],
    },
]

# Configuration options for custom policy creation
CUSTOM_POLICY_OPTIONS = {
    "conditions": {
        "content_contains": {
            "name": "Content contains sensitive information",
            "description": "Triggers when content matches specified sensitive information types.",
        },
        "content_shared_external": {
            "name": "Content is shared with people outside the organization",
            "description": "Triggers when content is shared externally.",
        },
        "content_shared_internal": {
            "name": "Content is shared within the organization",
            "description": "Triggers when content is shared internally.",
        },
        "sender_is": {
            "name": "Sender is a member of a specific group",
            "description": "Triggers based on the sender's group membership.",
        },
        "recipient_is": {
            "name": "Recipient is a specific user or domain",
            "description": "Triggers based on the recipient's identity.",
        },
        "document_property": {
            "name": "Document property matches",
            "description": "Triggers based on document metadata properties.",
        },
        "file_extension": {
            "name": "File extension is",
            "description": "Triggers based on the file type/extension.",
        },
        "volume_threshold": {
            "name": "Volume of sensitive items threshold",
            "description": "Triggers when the count of sensitive items exceeds a threshold.",
        },
    },
    "user_overrides": {
        "allow_override": {
            "name": "Allow overrides from M365 services",
            "description": "Allows users to override policy actions with justification.",
        },
        "require_justification": {
            "name": "Require business justification to override",
            "description": "Requires a justification reason when overriding a policy.",
        },
        "allow_false_positive": {
            "name": "Override if reported as false positive",
            "description": "Allows override when the user reports a false positive detection.",
        },
    },
    "incident_reports": {
        "severity_low": {"name": "Low severity alert", "description": "Generates low-priority alerts."},
        "severity_medium": {"name": "Medium severity alert", "description": "Generates medium-priority alerts."},
        "severity_high": {"name": "High severity alert", "description": "Generates high-priority alerts."},
        "send_email": {
            "name": "Send alert via email",
            "description": "Sends alert details to specified administrators via email.",
        },
    },
}


def get_all_keywords():
    """Return a flat mapping of keyword -> source for quick lookup."""
    keyword_map = {}
    for sit_id, sit in SENSITIVE_INFO_TYPES.items():
        for kw in sit["keywords"]:
            keyword_map[kw] = ("sensitive_info_type", sit_id)
    for loc_id, loc in POLICY_LOCATIONS.items():
        for kw in loc["keywords"]:
            keyword_map[kw] = ("location", loc_id)
    for act_id, act in POLICY_ACTIONS.items():
        for kw in act["keywords"]:
            keyword_map[kw] = ("action", act_id)
    for tmpl in POLICY_TEMPLATES:
        for kw in tmpl["keywords"]:
            keyword_map[kw] = ("template", tmpl["id"])
    return keyword_map

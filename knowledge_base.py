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
    # ── Financial DLP Templates ────────────────────────────────────────────────
    {
        "id": "dlp_pci_dss",
        "name": "U.S. PCI Data Security Standard (PCI-DSS)",
        "category": "DLP",
        "subcategory": "Financial",
        "description": (
            "Enforces PCI-DSS requirements by detecting primary account numbers (PAN), "
            "cardholder data, CVV codes, and magnetic stripe data across all M365 workloads."
        ),
        "keywords": [
            "PCI", "PCI-DSS", "PCI DSS", "payment card", "cardholder", "PAN", "primary account number",
            "CVV", "CVV2", "CVC", "card verification", "magnetic stripe", "credit card industry",
            "card data", "merchant", "acquirer", "issuer", "card brand"
        ],
        "sensitive_info_types": [
            "Credit Card Number",
            "Credit Card Magnetic Strip Data",
        ],
        "default_actions": ["Block sharing externally", "Notify compliance team", "Generate incident report", "Encrypt at rest"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": True,
        "confidence": 95,
        "expected_effects": [
            "Emails containing PANs or cardholder data are blocked from leaving the organization.",
            "SharePoint and OneDrive files with card data are restricted from external access.",
            "Compliance team receives real-time alerts for PCI-DSS violations.",
            "All incidents are logged to support PCI-DSS audit requirements.",
            "Policy tips guide users on proper cardholder data handling procedures.",
        ],
        "troubleshooting_tips": [
            "Ensure credit card number SIT is configured with the correct confidence level (High) to reduce false positives on test card numbers.",
            "Use PCI-DSS scoped locations to exclude tokenization systems that store card tokens rather than raw PANs.",
            "Verify policy applies to all content types including attachments, not just email body.",
        ],
        "doc_search_query": "PCI DSS DLP policy Microsoft Purview credit card cardholder data protection",
    },
    {
        "id": "dlp_sox_compliance",
        "name": "Sarbanes-Oxley (SOX) Compliance",
        "category": "DLP",
        "subcategory": "Financial",
        "description": (
            "Supports SOX compliance by protecting financial reporting data, earnings information, "
            "auditor communications, and material non-public information (MNPI)."
        ),
        "keywords": [
            "SOX", "Sarbanes-Oxley", "financial reporting", "earnings", "auditor", "MNPI",
            "material non-public", "quarterly report", "annual report", "10-K", "10-Q",
            "internal controls", "financial statements", "SEC filing", "public company", "CFO"
        ],
        "sensitive_info_types": [
            "U.S. Bank Account Number",
            "Financial Statement Keywords (custom)",
            "Audit Report Keywords (custom)",
        ],
        "default_actions": ["Restrict access to finance team", "Notify compliance officer", "Audit log all access"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": False,
        "confidence": 78,
        "expected_effects": [
            "Financial reporting documents are restricted to authorized finance personnel.",
            "Earnings data and draft filings cannot be shared externally before public release.",
            "Auditor communications are logged and monitored for compliance.",
            "Insider trading risk is reduced by controlling MNPI distribution.",
            "Compliance officer is alerted when SOX-sensitive content is accessed unusually.",
        ],
        "troubleshooting_tips": [
            "Create a custom keyword dictionary with your organization's financial terminology (ticker symbols, fiscal period references) for more accurate detection.",
            "Coordinate with the Insider Risk Management team to correlate SOX policy violations with user risk scores.",
        ],
        "doc_search_query": "SOX Sarbanes-Oxley compliance DLP Microsoft Purview financial data protection",
    },
    {
        "id": "dlp_glba",
        "name": "Gramm-Leach-Bliley Act (GLBA)",
        "category": "DLP",
        "subcategory": "Financial",
        "description": (
            "Protects financial consumers' nonpublic personal information (NPI) as required by GLBA. "
            "Covers bank records, loan data, investment information, and customer financial profiles."
        ),
        "keywords": [
            "GLBA", "Gramm-Leach-Bliley", "NPI", "nonpublic personal information", "bank records",
            "financial institution", "consumer finance", "loan data", "mortgage", "investment account",
            "brokerage", "customer financial", "privacy notice", "safeguards rule", "FTC"
        ],
        "sensitive_info_types": [
            "U.S. Bank Account Number",
            "ABA Routing Number",
            "U.S. Individual Taxpayer Identification Number (ITIN)",
            "U.S. Social Security Number (SSN)",
        ],
        "default_actions": ["Block external sharing", "Notify privacy officer", "Generate incident report"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": True,
        "confidence": 85,
        "expected_effects": [
            "Consumer financial records are blocked from unauthorized external sharing.",
            "Privacy officer is notified of GLBA-related policy violations.",
            "Loan and banking data in emails is intercepted and reviewed.",
            "All consumer data access is logged to support GLBA audit trail.",
            "Policy tips educate staff on GLBA obligations regarding consumer data.",
        ],
        "troubleshooting_tips": [
            "Extend the policy to cover third-party service providers by including their email domains in monitored sender/recipient lists.",
            "Review the GLBA Safeguards Rule requirements and ensure encryption actions are enabled for stored NPI.",
        ],
        "doc_search_query": "GLBA Gramm-Leach-Bliley financial data DLP policy Microsoft Purview NPI protection",
    },
    {
        "id": "dlp_swift_codes",
        "name": "SWIFT Codes and Wire Transfer Data",
        "category": "DLP",
        "subcategory": "Financial",
        "description": (
            "Detects and protects SWIFT BIC codes, wire transfer instructions, IBAN numbers, "
            "and other international banking identifiers to prevent financial fraud."
        ),
        "keywords": [
            "SWIFT", "BIC code", "wire transfer", "IBAN", "international wire", "correspondent bank",
            "bank transfer", "remittance", "SEPA", "ACH", "routing", "beneficiary account",
            "financial messaging", "interbank", "cross-border payment"
        ],
        "sensitive_info_types": [
            "SWIFT Code",
            "International Banking Account Number (IBAN)",
            "U.S. Bank Account Number",
            "ABA Routing Number",
        ],
        "default_actions": ["Block external sharing", "Notify security team", "Require approval for override"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": False,
        "confidence": 82,
        "expected_effects": [
            "Wire transfer instructions containing SWIFT/IBAN data are blocked from unauthorized recipients.",
            "Security team is alerted to potential business email compromise (BEC) scenarios.",
            "Override requires dual-approval to prevent social engineering attacks.",
            "All wire transfer data sharing events are logged for fraud investigation.",
            "Employees receive policy tips reminding them to verify wire transfer requests.",
        ],
        "troubleshooting_tips": [
            "Configure the policy to allow exceptions for treasury and finance teams using group-based exclusions.",
            "Combine with Communication Compliance monitoring to detect social engineering attempts in emails discussing wire transfers.",
        ],
        "doc_search_query": "SWIFT BIC IBAN wire transfer DLP Microsoft Purview financial fraud prevention",
    },
    # ── Healthcare Templates ───────────────────────────────────────────────────
    {
        "id": "dlp_phi_protection",
        "name": "Protected Health Information (PHI) Comprehensive",
        "category": "DLP",
        "subcategory": "Healthcare",
        "description": (
            "Comprehensive PHI protection beyond basic HIPAA, covering lab results, prescriptions, "
            "patient names combined with medical info, mental health records, and genomic data."
        ),
        "keywords": [
            "PHI", "protected health information", "lab results", "prescription", "patient name",
            "medical record number", "MRN", "diagnosis code", "genomic", "mental health",
            "psychiatric", "substance abuse", "radiology", "pathology", "discharge summary", "EHR"
        ],
        "sensitive_info_types": [
            "U.S. Social Security Number (SSN)",
            "International Classification of Diseases (ICD-9)",
            "International Classification of Diseases (ICD-10)",
            "Drug Enforcement Agency (DEA) Number",
            "Medical Terms (custom keyword dictionary)",
        ],
        "default_actions": ["Block external sharing", "Encrypt content", "Notify HIPAA privacy officer", "Generate audit report"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": True,
        "confidence": 88,
        "expected_effects": [
            "Lab results, prescriptions, and clinical notes are blocked from external sharing.",
            "HIPAA privacy officer receives immediate notification of PHI exposure risks.",
            "Mental health and substance abuse records receive heightened protection.",
            "All PHI access events are logged for HIPAA audit trail requirements.",
            "Encrypted email is automatically applied when PHI is detected in outbound messages.",
        ],
        "troubleshooting_tips": [
            "Create a custom medical keyword dictionary with your facility's specific terminology, procedure codes, and department names.",
            "Use instance count thresholds to avoid false positives when medical terms appear in non-clinical contexts (e.g., general wellness emails).",
            "Test policy against de-identified records to ensure anonymized data does not trigger false positives.",
        ],
        "doc_search_query": "HIPAA PHI comprehensive DLP policy Microsoft Purview healthcare data protection lab results",
    },
    {
        "id": "dlp_medical_devices",
        "name": "Medical Device and Clinical Trial Data",
        "category": "DLP",
        "subcategory": "Healthcare",
        "description": (
            "Protects FDA submissions, clinical trial results, device specifications, "
            "and investigational new drug (IND) applications from unauthorized disclosure."
        ),
        "keywords": [
            "medical device", "clinical trial", "FDA", "510k", "PMA", "premarket approval",
            "IND", "investigational new drug", "NDA", "biologics", "BLA", "clinical data",
            "device specification", "adverse event", "IRB", "protocol", "GCP", "GMP"
        ],
        "sensitive_info_types": [
            "FDA Application Numbers (custom)",
            "Clinical Trial Identifiers (custom)",
            "Drug/Device Keywords (custom dictionary)",
        ],
        "default_actions": ["Restrict to R&D team", "Block external sharing without approval", "Notify regulatory affairs team"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": False,
        "confidence": 75,
        "expected_effects": [
            "FDA submission documents are restricted to authorized regulatory affairs personnel.",
            "Clinical trial data cannot be shared externally without explicit approval.",
            "Adverse event reports are protected from unauthorized disclosure.",
            "Regulatory affairs team is notified of any attempted unauthorized sharing.",
            "Device specifications and trade secrets in R&D documents are protected.",
        ],
        "troubleshooting_tips": [
            "Work with regulatory affairs to build a custom keyword dictionary covering FDA form numbers, trial phase identifiers, and device classification codes.",
            "Ensure SharePoint sites used for clinical trial data have separate DLP scoping to avoid overly broad policy application.",
        ],
        "doc_search_query": "medical device clinical trial FDA DLP Microsoft Purview regulatory data protection",
    },
    # ── Privacy/PII Templates ──────────────────────────────────────────────────
    {
        "id": "dlp_ccpa",
        "name": "California Consumer Privacy Act (CCPA)",
        "category": "DLP",
        "subcategory": "Privacy",
        "description": (
            "Protects California residents' personal data as required by CCPA and CPRA. "
            "Covers identifiers, biometric data, geolocation, browsing history, and inferences."
        ),
        "keywords": [
            "CCPA", "CPRA", "California privacy", "California consumer", "personal information",
            "biometric", "geolocation", "browsing history", "opt-out", "do not sell",
            "sensitive personal information", "California residents", "consumer rights", "data broker"
        ],
        "sensitive_info_types": [
            "U.S. Social Security Number (SSN)",
            "U.S. Driver's License Number",
            "U.S. Bank Account Number",
            "Credit Card Number",
        ],
        "default_actions": ["Restrict sharing", "Notify privacy team", "Log for consumer request fulfillment"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": True,
        "confidence": 83,
        "expected_effects": [
            "California residents' personal data is detected and restricted from unauthorized sharing.",
            "Privacy team is notified to support data subject access requests (DSAR).",
            "Sensitive categories (biometric, geolocation) receive enhanced protection.",
            "Audit logs support CCPA compliance verification and consumer rights fulfillment.",
            "Policy tips remind employees of CCPA opt-out and deletion obligations.",
        ],
        "troubleshooting_tips": [
            "Supplement built-in SITs with a custom keyword dictionary for California-specific data categories like household data and inferences.",
            "Ensure the policy covers all systems that collect California consumer data, including marketing automation tools connected via connectors.",
        ],
        "doc_search_query": "CCPA California Consumer Privacy Act DLP Microsoft Purview personal data protection",
    },
    {
        "id": "dlp_gdpr_extended",
        "name": "GDPR Extended - All EU Member States",
        "category": "DLP",
        "subcategory": "Privacy",
        "description": (
            "Expanded GDPR coverage including special categories of personal data such as "
            "racial/ethnic origin, political opinions, biometric data, health data, and sexual orientation."
        ),
        "keywords": [
            "GDPR", "EU GDPR", "special categories", "sensitive personal data", "racial origin",
            "ethnic origin", "political opinion", "trade union", "biometric data", "genetic data",
            "health data", "sexual orientation", "criminal convictions", "data controller",
            "data processor", "lawful basis", "legitimate interest", "DPA"
        ],
        "sensitive_info_types": [
            "EU Debit Card Number",
            "EU Driver's License Number",
            "EU National Identification Number",
            "EU Passport Number",
            "EU Social Security Number",
            "EU Tax Identification Number",
            "EU GPS Coordinates (custom)",
        ],
        "default_actions": ["Block external transfer", "Notify Data Protection Officer", "Require lawful basis documentation"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": True,
        "confidence": 87,
        "expected_effects": [
            "Special category personal data receives enhanced protection controls.",
            "Data Protection Officer (DPO) is notified of high-risk data transfers.",
            "Cross-border data transfers outside EEA are flagged for review.",
            "Audit trail supports GDPR Article 30 record-keeping obligations.",
            "Data subject rights requests can be supported through audit log searches.",
        ],
        "troubleshooting_tips": [
            "Configure country-specific SITs for each EU member state's national ID formats to maximize detection coverage.",
            "Coordinate with the DPO to ensure policy notifications are routed to the correct privacy contact for each EU operating country.",
        ],
        "doc_search_query": "GDPR extended special categories sensitive personal data Microsoft Purview EU compliance",
    },
    {
        "id": "dlp_lgpd",
        "name": "Brazil Lei Geral de Proteção de Dados (LGPD)",
        "category": "DLP",
        "subcategory": "Privacy",
        "description": (
            "Protects Brazilian personal data in compliance with LGPD. "
            "Covers CPF numbers, CNPJ, Brazilian IDs, and sensitive personal data categories."
        ),
        "keywords": [
            "LGPD", "Brazil", "Brazilian", "CPF", "CNPJ", "RG", "personal data", "dados pessoais",
            "titular", "controlador", "operador", "ANPD", "consentimento", "sensitive data",
            "Brazilian citizens", "Brazil privacy law", "data localization"
        ],
        "sensitive_info_types": [
            "Brazil CPF Number",
            "Brazil CNPJ Number",
            "Brazil National ID Card (RG) (custom)",
        ],
        "default_actions": ["Block external sharing", "Notify privacy team", "Generate LGPD compliance report"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": False,
        "confidence": 78,
        "expected_effects": [
            "Brazilian personal data (CPF, CNPJ) is detected and protected across M365 workloads.",
            "Privacy team receives alerts to support LGPD data subject rights requests.",
            "International transfers of Brazilian data are logged and flagged for review.",
            "Compliance reports support ANPD accountability requirements.",
            "Policy tips educate employees on LGPD obligations.",
        ],
        "troubleshooting_tips": [
            "Verify that Brazilian CPF number SIT regex patterns are correctly configured as the format (###.###.###-##) can vary.",
            "Add Portuguese-language keywords to the detection dictionary for documents written in Portuguese.",
        ],
        "doc_search_query": "LGPD Brazil data protection DLP Microsoft Purview CPF CNPJ personal data",
    },
    {
        "id": "dlp_passport_numbers",
        "name": "International Passport Numbers",
        "category": "DLP",
        "subcategory": "PII",
        "description": (
            "Detects passport numbers from multiple countries including US, UK, EU member states, "
            "Canada, Australia, and other major nations to prevent identity theft."
        ),
        "keywords": [
            "passport", "passport number", "travel document", "international passport",
            "visa", "national passport", "passport ID", "biometric passport",
            "border crossing", "immigration", "ICAO", "machine readable", "MRZ", "nationality"
        ],
        "sensitive_info_types": [
            "U.S. Passport Number",
            "EU Passport Number",
            "Australia Passport Number",
            "Canada Passport Number",
            "UK Passport Number",
            "China Resident Identity Card Number",
        ],
        "default_actions": ["Block external sharing", "Notify HR/security", "Generate incident report"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": True,
        "confidence": 85,
        "expected_effects": [
            "Passport numbers from supported countries are detected across all M365 workloads.",
            "Documents containing passport scans or numbers are blocked from external sharing.",
            "HR and security teams are notified of passport data exposure risks.",
            "Incident reports support compliance with identity theft regulations.",
            "Policy applies to structured (forms, spreadsheets) and unstructured (emails, docs) content.",
        ],
        "troubleshooting_tips": [
            "Adjust instance count thresholds; a single passport number may appear legitimately in HR onboarding contexts.",
            "Use the 'Exact Data Match' (EDM) feature to match against a known employee passport number list to reduce false positives.",
        ],
        "doc_search_query": "international passport numbers DLP Microsoft Purview multi-country identity protection",
    },
    {
        "id": "dlp_driver_license",
        "name": "Driver's License Numbers (Multi-state)",
        "category": "DLP",
        "subcategory": "PII",
        "description": (
            "Detects driver's license numbers from all 50 U.S. states and territories, "
            "protecting this common identity credential from unauthorized disclosure."
        ),
        "keywords": [
            "driver license", "driver's license", "DL number", "state ID", "motor vehicle",
            "DMV", "license plate", "vehicle registration", "operator license",
            "identification card", "state-issued ID", "license number", "driving record"
        ],
        "sensitive_info_types": [
            "U.S. Driver's License Number",
            "State-specific Driver's License Patterns (custom)",
        ],
        "default_actions": ["Block external sharing", "Notify user", "Require justification for override"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": True,
        "confidence": 80,
        "expected_effects": [
            "Driver's license numbers are detected and protected across all workloads.",
            "External sharing of documents containing DL numbers is blocked.",
            "Users receive guidance on proper handling of government-issued IDs.",
            "Override requires a business justification that is logged for audit.",
            "Policy helps meet state privacy law requirements for ID number protection.",
        ],
        "troubleshooting_tips": [
            "Driver's license formats vary significantly by state; supplement the built-in SIT with state-specific custom regex patterns for higher accuracy.",
            "Exclude HR and background check workflows using group-based policy exceptions to avoid blocking legitimate use cases.",
        ],
        "doc_search_query": "driver license number DLP Microsoft Purview multi-state US identity protection",
    },
    # ── Regional Compliance Templates ─────────────────────────────────────────
    {
        "id": "dlp_uk_data_protection",
        "name": "UK Data Protection Act 2018",
        "category": "DLP",
        "subcategory": "Privacy",
        "description": (
            "Implements UK GDPR post-Brexit data protection requirements under the Data Protection Act 2018, "
            "covering UK residents' personal data and special category data."
        ),
        "keywords": [
            "UK GDPR", "Data Protection Act", "DPA 2018", "UK data protection", "ICO",
            "Information Commissioner", "British", "United Kingdom", "NI number",
            "National Insurance", "NHS number", "UK residents", "post-Brexit", "adequacy decision"
        ],
        "sensitive_info_types": [
            "UK National Insurance Number",
            "UK NHS Number",
            "UK Driver's License Number",
            "UK Passport Number",
            "UK Electoral Roll Number",
        ],
        "default_actions": ["Block external transfer", "Notify Data Protection Officer", "Generate ICO compliance report"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": True,
        "confidence": 86,
        "expected_effects": [
            "UK personal data is detected and protected across all M365 workloads.",
            "Transfers of UK data to non-adequate countries are flagged for review.",
            "DPO receives notifications to support UK GDPR accountability obligations.",
            "NHS numbers and National Insurance numbers receive special protection.",
            "Audit logs support ICO investigation requirements.",
        ],
        "troubleshooting_tips": [
            "After Brexit, UK and EU GDPR are separate regimes; ensure you have distinct policies for UK vs EU data if your org operates in both regions.",
            "Verify NHS number SIT patterns are enabled if your organization handles health data for UK residents.",
        ],
        "doc_search_query": "UK Data Protection Act 2018 GDPR DLP Microsoft Purview ICO compliance",
    },
    {
        "id": "dlp_canada_pipeda",
        "name": "Canada PIPEDA Compliance",
        "category": "DLP",
        "subcategory": "Privacy",
        "description": (
            "Protects Canadian personal information as required by PIPEDA and provincial laws "
            "(Quebec Law 25, PIPA Alberta/BC), covering SINs, health card numbers, and more."
        ),
        "keywords": [
            "PIPEDA", "Canada privacy", "Canadian", "SIN", "social insurance number",
            "Quebec Law 25", "PIPA", "Alberta privacy", "BC privacy", "OPC",
            "Privacy Commissioner", "Canadian residents", "personal information", "health card"
        ],
        "sensitive_info_types": [
            "Canada Social Insurance Number (SIN)",
            "Canada Bank Account Number",
            "Canada Driver's License Number",
            "Canada Health Service Number",
            "Canada Passport Number",
        ],
        "default_actions": ["Block external sharing", "Notify privacy officer", "Log for PIPEDA breach reporting"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": True,
        "confidence": 84,
        "expected_effects": [
            "Canadian SINs and health card numbers are detected across M365 workloads.",
            "Privacy officer is notified to support 72-hour breach notification obligations.",
            "Provincial law requirements (Quebec Law 25) are addressed through enhanced controls.",
            "Cross-border data transfers involving Canadian data are logged.",
            "Audit trail supports OPC accountability requirements.",
        ],
        "troubleshooting_tips": [
            "Quebec Law 25 (Law 25) has stricter requirements than PIPEDA; consider a separate, stricter policy for Quebec-based employees and data.",
            "Ensure SIN detection includes both formatted (###-###-###) and unformatted (9-digit) patterns.",
        ],
        "doc_search_query": "PIPEDA Canada privacy compliance DLP Microsoft Purview SIN personal data",
    },
    {
        "id": "dlp_australia_privacy",
        "name": "Australia Privacy Act 1988",
        "category": "DLP",
        "subcategory": "Privacy",
        "description": (
            "Protects Australian personal information under the Privacy Act 1988 and Australian Privacy Principles (APPs), "
            "covering Tax File Numbers (TFN), Medicare numbers, and personal data."
        ),
        "keywords": [
            "Australia Privacy Act", "Australian Privacy Principles", "APP", "TFN", "tax file number",
            "Medicare", "Australian", "OAIC", "Notifiable Data Breaches", "NDB scheme",
            "sensitive information", "credit reporting", "health information", "My Health Record"
        ],
        "sensitive_info_types": [
            "Australia Tax File Number",
            "Australia Medicare Number",
            "Australia Passport Number",
            "Australia Bank Account Number",
            "Australia Driver's License Number",
        ],
        "default_actions": ["Block external sharing", "Notify privacy team", "Generate NDB scheme incident report"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": True,
        "confidence": 85,
        "expected_effects": [
            "Australian TFNs and Medicare numbers are detected and protected.",
            "Notifiable Data Breach (NDB) incident reports are generated automatically.",
            "OAIC notification requirements are supported through automated alerting.",
            "Health information receives enhanced protection under the APPs.",
            "Audit logs support APP accountability and transparency requirements.",
        ],
        "troubleshooting_tips": [
            "TFN detection has a high false positive rate; use corroborating evidence conditions (keywords like 'tax file number' near the pattern) to improve precision.",
            "Enable the Notifiable Data Breaches scheme notification workflow to meet the 30-day OAIC reporting deadline.",
        ],
        "doc_search_query": "Australia Privacy Act TFN Medicare DLP Microsoft Purview APPs compliance",
    },
    {
        "id": "dlp_japan_appi",
        "name": "Japan Act on Protection of Personal Information (APPI)",
        "category": "DLP",
        "subcategory": "Privacy",
        "description": (
            "Implements APPI compliance for Japanese personal data including My Number (Individual Number), "
            "Japanese passport, and sensitive personal information categories."
        ),
        "keywords": [
            "APPI", "Japan privacy", "Japanese", "My Number", "individual number", "juki code",
            "PPC", "Personal Information Protection Commission", "sensitive personal information",
            "cross-border transfer", "third party provision", "opt-in consent", "Japan GDPR"
        ],
        "sensitive_info_types": [
            "Japan My Number (Individual Number)",
            "Japan Passport Number",
            "Japan Bank Account Number (custom)",
        ],
        "default_actions": ["Block external transfer", "Notify privacy compliance team", "Restrict third-party sharing"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": False,
        "confidence": 76,
        "expected_effects": [
            "My Number (Individual Number) data is detected and protected across M365.",
            "Cross-border transfers of Japanese personal data are flagged for legal basis review.",
            "Third-party provision of personal data is restricted and logged.",
            "Privacy compliance team receives alerts for APPI-sensitive data exposure.",
            "Audit trail supports PPC accountability requirements.",
        ],
        "troubleshooting_tips": [
            "My Number is a 12-digit number; configure the SIT with supporting Japanese keywords (マイナンバー, 個人番号) to reduce false positives.",
            "Japanese text documents require Unicode-aware keyword matching; verify policy works on Japanese-language content.",
        ],
        "doc_search_query": "Japan APPI My Number personal information DLP Microsoft Purview compliance",
    },
    {
        "id": "dlp_india_pdp",
        "name": "India Personal Data Protection Bill",
        "category": "DLP",
        "subcategory": "Privacy",
        "description": (
            "Implements protections for Indian personal data in compliance with the Digital Personal Data "
            "Protection Act (DPDPA), covering Aadhaar, PAN cards, and Indian financial identifiers."
        ),
        "keywords": [
            "India PDPB", "DPDPA", "India privacy", "Indian", "Aadhaar", "PAN card",
            "permanent account number", "UIDAI", "Indian residents", "data fiduciary",
            "data principal", "consent manager", "significant data fiduciary", "cross-border"
        ],
        "sensitive_info_types": [
            "India Permanent Account Number (PAN)",
            "India Unique Identification (Aadhaar) Number",
            "India Passport Number (custom)",
        ],
        "default_actions": ["Block external sharing", "Notify data protection officer", "Log for DPDPA compliance"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": False,
        "confidence": 74,
        "expected_effects": [
            "Aadhaar numbers and PAN cards are detected and protected across M365 workloads.",
            "Cross-border transfers of Indian personal data are logged and reviewed.",
            "Data protection officer receives notifications of potential DPDPA violations.",
            "Consent-based data processing records are maintained through audit logs.",
            "Policy tips educate employees on DPDPA obligations.",
        ],
        "troubleshooting_tips": [
            "Aadhaar detection should require high confidence due to the format (####-####-####) being easily confused with other numeric sequences; add keyword corroboration.",
            "Monitor for policy updates as the DPDPA rules are still being finalized; update keyword dictionaries as regulations evolve.",
        ],
        "doc_search_query": "India DPDPA personal data protection Aadhaar PAN Microsoft Purview DLP compliance",
    },
    # ── IP Protection Templates ────────────────────────────────────────────────
    {
        "id": "dlp_trade_secrets",
        "name": "Trade Secrets and Confidential Business Information",
        "category": "DLP",
        "subcategory": "Intellectual Property",
        "description": (
            "Protects proprietary formulas, business strategies, competitive intelligence, "
            "and other trade secrets from disclosure under the Defend Trade Secrets Act (DTSA)."
        ),
        "keywords": [
            "trade secret", "proprietary", "confidential business", "competitive intelligence",
            "business strategy", "formula", "recipe", "manufacturing process", "know-how",
            "DTSA", "misappropriation", "NDA", "non-disclosure", "confidential", "secret"
        ],
        "sensitive_info_types": [
            "Confidential Document Markings (custom)",
            "Trade Secret Keywords (custom dictionary)",
            "NDA Keywords (custom)",
        ],
        "default_actions": ["Block external sharing", "Notify legal team", "Require legal approval for override"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams", "Endpoints"],
        "template_available": False,
        "confidence": 73,
        "expected_effects": [
            "Documents containing trade secret keywords are blocked from external sharing.",
            "Legal team is notified when proprietary information is at risk of disclosure.",
            "Override requires legal team approval to prevent inadvertent disclosure.",
            "All access and sharing events for trade secret documents are logged.",
            "Policy supports DTSA misappropriation prevention and evidence requirements.",
        ],
        "troubleshooting_tips": [
            "Build a rich custom keyword dictionary in collaboration with legal and R&D teams covering product codenames, proprietary process names, and internal project terms.",
            "Combine with sensitivity labels (Highly Confidential) to ensure trade secret documents are encrypted and tracked.",
        ],
        "doc_search_query": "trade secrets DLP Microsoft Purview proprietary information confidential business protection",
    },
    {
        "id": "dlp_patent_documents",
        "name": "Patent and R&D Documents",
        "category": "DLP",
        "subcategory": "Intellectual Property",
        "description": (
            "Protects patent filings, invention disclosures, R&D research data, and pre-publication "
            "scientific findings from premature disclosure that could invalidate patent rights."
        ),
        "keywords": [
            "patent", "patent filing", "invention disclosure", "R&D", "research and development",
            "prior art", "USPTO", "EPO", "patent application", "claims", "specification",
            "inventor", "assignee", "provisional patent", "non-provisional", "publication bar"
        ],
        "sensitive_info_types": [
            "Patent Application Numbers (custom)",
            "R&D Document Keywords (custom dictionary)",
            "Invention Disclosure Keywords (custom)",
        ],
        "default_actions": ["Restrict to R&D and legal teams", "Block external sharing", "Notify IP counsel"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": False,
        "confidence": 72,
        "expected_effects": [
            "Patent draft documents are restricted to R&D and IP legal teams.",
            "Pre-filing invention disclosures cannot be shared externally.",
            "IP counsel is notified of any patent document sharing attempts.",
            "Publication bars are protected by preventing premature public disclosure.",
            "All patent document access is logged for IP management purposes.",
        ],
        "troubleshooting_tips": [
            "Create a SharePoint site-scoped policy for patent repositories rather than a broad organization policy to reduce false positives.",
            "Use sensitivity labels for patent documents with automatic expiry of protection after public filing.",
        ],
        "doc_search_query": "patent R&D invention disclosure DLP Microsoft Purview intellectual property protection",
    },
    {
        "id": "dlp_confidential_markings",
        "name": "Confidential Document Markings",
        "category": "DLP",
        "subcategory": "Intellectual Property",
        "description": (
            "Detects documents marked with CONFIDENTIAL, PROPRIETARY, RESTRICTED, or similar markings "
            "and enforces appropriate sharing restrictions based on document classification."
        ),
        "keywords": [
            "confidential marking", "document marking", "PROPRIETARY", "RESTRICTED", "FOR INTERNAL USE",
            "NOT FOR DISTRIBUTION", "COMPANY CONFIDENTIAL", "PRIVATE AND CONFIDENTIAL",
            "classification marking", "watermark", "header footer marking", "document classification"
        ],
        "sensitive_info_types": [
            "Confidential Document Markings (custom keyword dictionary)",
            "Document Header/Footer Patterns (custom)",
        ],
        "default_actions": ["Restrict external sharing", "Notify user with policy tip", "Log sharing attempts"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams", "Office Apps"],
        "template_available": False,
        "confidence": 77,
        "expected_effects": [
            "Documents with confidential markings in headers, footers, or body are detected.",
            "External sharing of marked documents is restricted based on marking level.",
            "Users receive policy tips explaining the restriction and proper handling.",
            "All sharing attempts for marked documents are logged for compliance.",
            "Works in tandem with sensitivity labels for defense-in-depth protection.",
        ],
        "troubleshooting_tips": [
            "Build a comprehensive keyword dictionary covering all marking variations used in your organization, including legacy markings.",
            "Consider also scanning document metadata fields (Author, Subject) where classification markings may be stored programmatically.",
        ],
        "doc_search_query": "confidential document markings DLP Microsoft Purview proprietary restricted detection",
    },
    # ── Endpoint DLP Templates ─────────────────────────────────────────────────
    {
        "id": "endpoint_dlp_usb",
        "name": "Endpoint DLP - USB and Removable Storage Blocking",
        "category": "DLP",
        "subcategory": "Endpoint",
        "description": (
            "Blocks copying of sensitive data to USB drives and removable storage on managed Windows endpoints, "
            "with audit logging and optional user override with justification."
        ),
        "keywords": [
            "USB", "removable storage", "flash drive", "thumb drive", "external drive",
            "SD card", "removable media", "device control", "USB blocking", "endpoint control",
            "data exfiltration", "physical transfer", "portable storage", "USB restriction"
        ],
        "sensitive_info_types": [
            "All configured sensitive information types",
        ],
        "default_actions": ["Block copy to USB/removable storage", "Audit activity", "Notify user", "Generate incident report"],
        "workloads": ["Windows 10/11 Endpoints"],
        "template_available": True,
        "confidence": 88,
        "expected_effects": [
            "Sensitive data files cannot be copied to USB drives or removable storage.",
            "Users attempting USB copy receive an immediate policy tip notification.",
            "All blocked and audited USB events are visible in the Activity Explorer.",
            "Override with business justification is configurable for authorized users.",
            "Incident reports are generated for compliance officer review.",
        ],
        "troubleshooting_tips": [
            "Ensure Microsoft Defender for Endpoint is onboarded and the device is in scope for Endpoint DLP before the policy will take effect.",
            "Verify the 'Devices' workload is enabled in the DLP policy and that device groups are correctly targeted.",
            "Test with a non-sensitive file first to confirm the endpoint DLP agent is active before testing with sensitive content.",
        ],
        "doc_search_query": "Endpoint DLP USB removable storage blocking Microsoft Purview device control Windows",
    },
    {
        "id": "endpoint_dlp_print",
        "name": "Endpoint DLP - Print Blocking",
        "category": "DLP",
        "subcategory": "Endpoint",
        "description": (
            "Prevents printing of sensitive documents on managed Windows endpoints, "
            "including local printers, network printers, and print-to-PDF/XPS operations."
        ),
        "keywords": [
            "print", "printing", "print blocking", "printer", "print restriction",
            "hardcopy", "paper copy", "print-to-PDF", "print-to-XPS", "virtual printer",
            "network printer", "local printer", "document printing", "endpoint print control"
        ],
        "sensitive_info_types": [
            "All configured sensitive information types",
        ],
        "default_actions": ["Block printing", "Notify user", "Allow override with justification", "Audit print activity"],
        "workloads": ["Windows 10/11 Endpoints"],
        "template_available": True,
        "confidence": 85,
        "expected_effects": [
            "Printing of sensitive documents is blocked on managed Windows devices.",
            "Print-to-PDF and print-to-XPS operations are also controlled.",
            "Users receive policy tips explaining why printing was blocked.",
            "Authorized users can override with a business justification that is logged.",
            "Print activity audit logs are available in Activity Explorer.",
        ],
        "troubleshooting_tips": [
            "Print blocking on Endpoint DLP requires Windows 10 RS5 (version 1809) or later; verify endpoint OS version compliance.",
            "Virtual PDF printers are treated as print destinations; ensure your policy scope includes 'Print to PDF' if you want to block that as well.",
        ],
        "doc_search_query": "Endpoint DLP print blocking Microsoft Purview printer restriction sensitive documents",
    },
    {
        "id": "endpoint_dlp_browser",
        "name": "Endpoint DLP - Browser Upload Restrictions",
        "category": "DLP",
        "subcategory": "Endpoint",
        "description": (
            "Blocks uploads of sensitive files to unallowed websites via Chrome, Edge, and Firefox "
            "on managed Windows endpoints, preventing data exfiltration through browser file uploads."
        ),
        "keywords": [
            "browser upload", "web upload", "file upload", "browser restriction", "Chrome DLP",
            "Edge DLP", "Firefox DLP", "web exfiltration", "cloud upload", "file sharing site",
            "personal storage", "Dropbox", "Google Drive personal", "browser extension", "upload blocking"
        ],
        "sensitive_info_types": [
            "All configured sensitive information types",
        ],
        "default_actions": ["Block upload to unallowed sites", "Notify user", "Audit browser upload activity"],
        "workloads": ["Windows 10/11 Endpoints"],
        "template_available": True,
        "confidence": 83,
        "expected_effects": [
            "Sensitive file uploads to personal cloud storage and unallowed websites are blocked.",
            "Chrome, Edge, and Firefox uploads are all monitored and controlled.",
            "Users receive a browser notification when an upload is blocked.",
            "Allowed business sites (e.g., SharePoint, approved vendors) are excluded.",
            "Browser upload activity is logged in Activity Explorer.",
        ],
        "troubleshooting_tips": [
            "The Microsoft Purview browser extension must be installed on Chrome/Firefox; Edge has native support. Verify extension deployment via Intune or Group Policy.",
            "Build an allowed-sites list for legitimate business cloud services to avoid blocking approved workflows.",
        ],
        "doc_search_query": "Endpoint DLP browser upload restriction Microsoft Purview Chrome Edge Firefox file upload blocking",
    },
    {
        "id": "endpoint_dlp_clipboard",
        "name": "Endpoint DLP - Clipboard Restriction",
        "category": "DLP",
        "subcategory": "Endpoint",
        "description": (
            "Controls clipboard operations involving sensitive data on managed Windows endpoints, "
            "preventing copy-paste exfiltration to unauthorized applications or external locations."
        ),
        "keywords": [
            "clipboard", "copy paste", "clipboard restriction", "paste blocking", "clipboard control",
            "screen capture", "clipboard exfiltration", "copy to clipboard", "paste to external",
            "clipboard monitoring", "data paste", "unmanaged app", "clipboard data"
        ],
        "sensitive_info_types": [
            "All configured sensitive information types",
        ],
        "default_actions": ["Block clipboard to unmanaged apps", "Notify user", "Audit clipboard activity"],
        "workloads": ["Windows 10/11 Endpoints"],
        "template_available": False,
        "confidence": 80,
        "expected_effects": [
            "Copy-pasting sensitive data to unmanaged or personal applications is blocked.",
            "Clipboard operations within managed/approved apps are permitted.",
            "Users receive policy tips when clipboard restrictions are applied.",
            "Clipboard exfiltration to external chat apps or personal email is prevented.",
            "All clipboard restriction events are logged in Activity Explorer.",
        ],
        "troubleshooting_tips": [
            "Define the list of allowed (managed) applications carefully; overly restrictive clipboard policies can significantly impact productivity.",
            "Clipboard restriction requires testing across your specific application stack as some custom LOB apps may trigger unexpected blocks.",
        ],
        "doc_search_query": "Endpoint DLP clipboard restriction Microsoft Purview copy paste control sensitive data",
    },
    # ── Enhanced Sensitivity Label Templates ──────────────────────────────────
    {
        "id": "sensitivity_label_public",
        "name": "Public Sensitivity Label",
        "category": "Information Protection",
        "subcategory": "Sensitivity Labels",
        "description": (
            "Defines a 'Public' sensitivity label for content that is approved for public distribution, "
            "with no access restrictions and clear visual marking."
        ),
        "keywords": [
            "public", "public label", "publicly shareable", "no restriction", "open content",
            "press release", "public document", "marketing material", "public website",
            "unrestricted", "approved for release", "external sharing allowed", "public data"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Apply Public label", "Add visual marking", "Allow external sharing"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams", "Office Apps"],
        "template_available": True,
        "confidence": 90,
        "expected_effects": [
            "Content is explicitly marked as approved for public distribution.",
            "No encryption or access restrictions are applied.",
            "Visual markings clearly identify the content as public.",
            "External sharing is permitted without restrictions.",
            "Audit logs track when content is labeled public for accountability.",
        ],
        "troubleshooting_tips": [
            "Ensure the Public label is at the bottom of your label hierarchy and configured so users cannot apply it to content that already has a higher classification.",
            "Configure mandatory labeling to encourage users to explicitly choose Public rather than leaving content unlabeled.",
        ],
        "doc_search_query": "public sensitivity label Microsoft Purview information protection label hierarchy",
    },
    {
        "id": "sensitivity_label_general",
        "name": "General Sensitivity Label",
        "category": "Information Protection",
        "subcategory": "Sensitivity Labels",
        "description": (
            "A 'General' or 'Internal' sensitivity label for everyday internal business content "
            "that is not sensitive but should stay within the organization."
        ),
        "keywords": [
            "general", "internal", "internal use", "non-sensitive", "standard", "everyday",
            "business content", "internal document", "general label", "default label",
            "not sensitive", "internal only", "org content", "standard content"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Apply General label", "Add visual marking", "Restrict anonymous external access"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams", "Office Apps"],
        "template_available": True,
        "confidence": 88,
        "expected_effects": [
            "Content is labeled as general internal business information.",
            "Anonymous (unauthenticated) external sharing is disabled.",
            "Visual markings identify the content as internal use.",
            "Authenticated external sharing with known guests is permitted.",
            "Default label policy can automatically apply this to unlabeled content.",
        ],
        "troubleshooting_tips": [
            "Consider making this the default label for your organization so all new content starts with at least a General classification.",
            "General label should not apply encryption to avoid friction; use policy tips to educate users about appropriate handling.",
        ],
        "doc_search_query": "general internal sensitivity label Microsoft Purview default label information protection",
    },
    {
        "id": "sensitivity_label_confidential_all_employees",
        "name": "Confidential - All Employees",
        "category": "Information Protection",
        "subcategory": "Sensitivity Labels",
        "description": (
            "A 'Confidential - All Employees' sensitivity label that encrypts content and restricts "
            "access to all authenticated members of the organization, blocking external sharing."
        ),
        "keywords": [
            "confidential all employees", "internal confidential", "organization wide",
            "all staff", "all users", "authenticated employees", "org restricted",
            "internal encryption", "employee only", "restricted internal", "confidential label"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Apply encryption (all employees)", "Add visual markings", "Block external access", "Allow internal co-authoring"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams", "Office Apps"],
        "template_available": True,
        "confidence": 92,
        "expected_effects": [
            "Content is encrypted and accessible only to authenticated organizational members.",
            "External sharing is blocked; guests cannot access the content.",
            "All employees can read and edit the content without friction.",
            "Visual header/footer markings identify the confidential classification.",
            "Rights Management protection persists when files are downloaded.",
        ],
        "troubleshooting_tips": [
            "Ensure the Azure AD group used for 'all employees' encryption is kept up to date; departing employees should be removed promptly.",
            "Co-authoring on encrypted files requires Office 365 Apps; verify all users have the correct license to avoid editing errors.",
        ],
        "doc_search_query": "Confidential All Employees sensitivity label Microsoft Purview encryption all staff",
    },
    {
        "id": "sensitivity_label_confidential_finance",
        "name": "Confidential - Finance Only",
        "category": "Information Protection",
        "subcategory": "Sensitivity Labels",
        "description": (
            "A 'Confidential - Finance' sensitivity label that restricts access to the finance team only, "
            "applying strong encryption with named user/group permissions."
        ),
        "keywords": [
            "confidential finance", "finance only", "finance team", "financial confidential",
            "accounting restricted", "CFO", "controller", "treasury", "finance label",
            "group restricted label", "department restricted", "finance department"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Apply encryption (finance group)", "Add visual markings", "Block access for non-finance users"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams", "Office Apps"],
        "template_available": True,
        "confidence": 91,
        "expected_effects": [
            "Content is encrypted and accessible only to the defined finance security group.",
            "Non-finance employees receive an access denied error when opening the file.",
            "Finance team retains full rights including edit, print, and forward.",
            "Visual markings identify the finance-only classification.",
            "Protection persists when files are emailed or downloaded.",
        ],
        "troubleshooting_tips": [
            "Use a security group (not a distribution list) for the finance team permission assignment for correct Rights Management enforcement.",
            "Create sublabels (e.g., Confidential/Finance, Confidential/HR) under a parent Confidential label for a clean label hierarchy.",
        ],
        "doc_search_query": "Confidential Finance sensitivity label Microsoft Purview group restricted encryption department",
    },
    {
        "id": "sensitivity_label_highly_confidential_dke",
        "name": "Highly Confidential - Double Key Encryption",
        "category": "Information Protection",
        "subcategory": "Sensitivity Labels",
        "description": (
            "Applies Double Key Encryption (DKE) for the highest security content, ensuring "
            "Microsoft and unauthorized parties cannot decrypt the data even if cloud keys are compromised."
        ),
        "keywords": [
            "double key encryption", "DKE", "highly confidential", "customer managed key",
            "sovereign encryption", "air-gapped", "government secret", "classified",
            "offline encryption", "key sovereignty", "no Microsoft access", "CMK", "BYOK"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Apply DKE encryption", "Restrict to named individuals", "Disable online editing", "Block all external access"],
        "workloads": ["Office Apps (Desktop only)", "SharePoint Online (with DKE support)"],
        "template_available": False,
        "confidence": 88,
        "expected_effects": [
            "Content is encrypted with two keys: Microsoft's and the organization's private key.",
            "Microsoft cannot decrypt content even under legal compulsion.",
            "Only specifically named users with both keys can access the content.",
            "Online editing in Office for the web is not available (desktop only).",
            "Provides highest assurance for government, legal, and classified content.",
        ],
        "troubleshooting_tips": [
            "DKE requires deploying and maintaining a DKE service on your own infrastructure (Azure App Service or on-premises); plan for high availability.",
            "DKE-protected files cannot be opened in Office for the Web; users must use Office desktop apps version 2009 or later.",
            "Ensure the DKE service URL is accessible from all user endpoints and that certificate management is in place.",
        ],
        "doc_search_query": "Double Key Encryption DKE sensitivity label Microsoft Purview highly confidential sovereign",
    },
    {
        "id": "sensitivity_label_auto",
        "name": "Auto-Labeling Policy",
        "category": "Information Protection",
        "subcategory": "Sensitivity Labels",
        "description": (
            "Automatically applies sensitivity labels to content in SharePoint, OneDrive, and Exchange "
            "based on sensitive information types and trainable classifiers, without user action."
        ),
        "keywords": [
            "auto-labeling", "automatic label", "auto apply", "automatically classify",
            "service-side labeling", "auto classification", "label automation",
            "auto-label policy", "without user interaction", "bulk labeling", "existing content"
        ],
        "sensitive_info_types": [
            "Configurable - any sensitive info type or trainable classifier",
        ],
        "default_actions": ["Auto-apply sensitivity label", "Notify user of applied label", "Generate labeling activity report"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business"],
        "template_available": True,
        "confidence": 85,
        "expected_effects": [
            "Labels are automatically applied to matching content without user involvement.",
            "Existing unlabeled content in SharePoint and OneDrive is retroactively labeled.",
            "Simulation mode allows testing the policy scope before enforcement.",
            "Users are notified when a label is automatically applied to their content.",
            "Labeling activity reports show coverage and match statistics.",
        ],
        "troubleshooting_tips": [
            "Always run in simulation mode first to estimate policy scope and review matches before switching to enforce mode.",
            "Auto-labeling policies can take up to 7 days to process existing content in large SharePoint/OneDrive tenants; plan accordingly.",
            "Auto-labeling for emails applies labels at send/receive time; it does not retroactively label content already in mailboxes.",
        ],
        "doc_search_query": "auto-labeling policy Microsoft Purview sensitivity labels automatic classification SharePoint OneDrive Exchange",
    },
    # ── Insider Risk Management Templates ─────────────────────────────────────
    {
        "id": "insider_risk_general_leaks",
        "name": "Insider Risk - General Data Leaks",
        "category": "Insider Risk Management",
        "subcategory": "Data Leaks",
        "description": (
            "Detects unusual data movement and potential data leaks by monitoring for anomalous "
            "download, exfiltration, and sharing patterns across all users in the organization."
        ),
        "keywords": [
            "data leak", "data leakage", "unusual download", "mass download", "exfiltration",
            "anomalous activity", "risk score", "user activity", "general data leak",
            "insider threat", "data movement", "unusual sharing", "bulk access", "data spillage"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Risk scoring", "Alert security team", "Enable activity explorer investigation"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams", "Endpoints"],
        "template_available": True,
        "confidence": 82,
        "expected_effects": [
            "Risk scores are calculated for all users based on data movement patterns.",
            "Security team is alerted when risk scores exceed configured thresholds.",
            "Activity Explorer provides detailed timeline of risky user activities.",
            "Adaptive Protection can automatically tighten DLP controls for high-risk users.",
            "Evidence packages support HR and legal investigation workflows.",
        ],
        "troubleshooting_tips": [
            "Ensure Microsoft 365 audit logging is enabled in all required workloads before activating the policy; missing audit signals result in incomplete risk scores.",
            "Tune risk score weights based on your organization's baseline; initial alerts may require threshold adjustment to reduce noise.",
        ],
        "doc_search_query": "Insider Risk Management general data leaks Microsoft Purview anomalous activity detection",
    },
    {
        "id": "insider_risk_priority_users",
        "name": "Insider Risk - Data Leaks by Priority Users",
        "category": "Insider Risk Management",
        "subcategory": "Data Leaks",
        "description": (
            "Focuses Insider Risk Management on executives, administrators, and users with access "
            "to highly sensitive data, with enhanced monitoring and lower risk score thresholds."
        ),
        "keywords": [
            "priority users", "executives", "administrators", "privileged users", "high-value targets",
            "C-suite", "VIP users", "elevated access", "admin accounts", "sensitive role",
            "priority user group", "enhanced monitoring", "executive risk", "privileged insider"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Enhanced risk scoring for priority users", "Immediate alert on any anomaly", "Notify CISO"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams", "Endpoints"],
        "template_available": True,
        "confidence": 85,
        "expected_effects": [
            "Priority user group members receive enhanced monitoring with boosted risk scores.",
            "CISO is immediately notified of any unusual activity by priority users.",
            "Lower activity thresholds trigger alerts compared to standard users.",
            "Priority user activity is retained longer for investigation purposes.",
            "Supports separation of duties by monitoring privileged administrators.",
        ],
        "troubleshooting_tips": [
            "Define priority user groups carefully and review membership regularly; over-designation reduces effectiveness through alert fatigue.",
            "Coordinate with HR and legal before monitoring executives to ensure compliance with employment law and union agreements.",
        ],
        "doc_search_query": "Insider Risk priority users executives privileged Microsoft Purview enhanced monitoring",
    },
    {
        "id": "insider_risk_disgruntled",
        "name": "Insider Risk - Disgruntled User Data Leaks",
        "category": "Insider Risk Management",
        "subcategory": "Data Leaks",
        "description": (
            "Correlates HR signals such as performance reviews, PIPs, and workplace complaints "
            "with data activity to detect potential data leaks by at-risk employees."
        ),
        "keywords": [
            "disgruntled", "at-risk employee", "PIP", "performance improvement plan", "HR signal",
            "workplace complaint", "demotion", "disciplinary action", "grievance", "work conflict",
            "negative review", "harassment complaint", "frustrated employee", "workplace dispute"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Correlate HR signals with data activity", "Elevate risk score", "Alert HR and security"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams", "Endpoints"],
        "template_available": True,
        "confidence": 78,
        "expected_effects": [
            "HR system events trigger elevated monitoring of affected users.",
            "Correlation between HR signals and unusual data activity raises risk scores.",
            "HR and security teams are jointly notified of correlated risk indicators.",
            "Investigation timeline shows HR events alongside data activity for context.",
            "Enables proactive intervention before actual data theft occurs.",
        ],
        "troubleshooting_tips": [
            "Configure the HR connector to import data from your HRIS system; without HR signals, this policy functions as a standard data leaks policy.",
            "Work with HR and legal to define the HR events that should be used as risk triggers, ensuring alignment with employment law.",
        ],
        "doc_search_query": "Insider Risk disgruntled employee HR signals data leaks Microsoft Purview performance",
    },
    {
        "id": "insider_risk_security_violations",
        "name": "Insider Risk - Security Policy Violations",
        "category": "Insider Risk Management",
        "subcategory": "Security Violations",
        "description": (
            "Detects security policy violations including DLP bypass attempts, access to restricted "
            "resources, and other risky behaviors that indicate potential malicious insider activity."
        ),
        "keywords": [
            "security violation", "policy violation", "DLP bypass", "override", "risky behavior",
            "unauthorized access", "security alert", "Azure AD risk", "MFA bypass",
            "suspicious sign-in", "anomalous access", "privileged escalation", "security incident"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Risk scoring", "Alert SOC team", "Trigger automated investigation workflow"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams", "Endpoints", "Azure AD"],
        "template_available": True,
        "confidence": 83,
        "expected_effects": [
            "Security policy violations are correlated with insider risk scores.",
            "SOC team receives immediate alerts for high-severity security violations.",
            "Automated investigation workflows are triggered for critical risk events.",
            "DLP policy override attempts are flagged as risk indicators.",
            "Azure AD risk signals from Identity Protection are incorporated into scoring.",
        ],
        "troubleshooting_tips": [
            "Ensure the Microsoft Defender for Endpoint integration is enabled so that endpoint security alerts feed into insider risk scores.",
            "Configure alert volume carefully; security violations policies can generate high alert volumes in environments with many DLP overrides.",
        ],
        "doc_search_query": "Insider Risk security policy violations DLP bypass Microsoft Purview SOC investigation",
    },
    {
        "id": "insider_risk_patient_data",
        "name": "Insider Risk - Patient Data Misuse",
        "category": "Insider Risk Management",
        "subcategory": "Healthcare",
        "description": (
            "Detects healthcare employees misusing patient data including snooping on celebrity patients, "
            "ex-partners, or any patient outside their care assignment."
        ),
        "keywords": [
            "patient data misuse", "VIP patient", "snooping", "unauthorized patient access",
            "HIPAA violation", "patient privacy", "EHR snooping", "celebrity patient",
            "family member access", "unauthorized viewing", "patient record access", "healthcare insider"
        ],
        "sensitive_info_types": [
            "Medical Record Numbers (custom)",
            "Patient Identifiers (custom)",
        ],
        "default_actions": ["Detect unauthorized patient record access", "Alert privacy officer", "Generate HIPAA incident report"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams", "Endpoints"],
        "template_available": True,
        "confidence": 80,
        "expected_effects": [
            "Unusual patient record access patterns are detected and risk-scored.",
            "Privacy officer is alerted to potential HIPAA violations.",
            "Snooping on VIP or celebrity patients triggers immediate high-risk alerts.",
            "HIPAA incident reports are automatically generated for compliance.",
            "Activity timeline supports investigation and potential breach notification.",
        ],
        "troubleshooting_tips": [
            "Integrate with your EHR system's audit logs via a custom connector to ensure patient access events are captured.",
            "Define 'unusual access' thresholds based on average patient record access rates for different clinical roles.",
        ],
        "doc_search_query": "Insider Risk patient data misuse HIPAA snooping Microsoft Purview healthcare EHR",
    },
    {
        "id": "insider_risk_risky_browser",
        "name": "Insider Risk - Risky Browser Usage",
        "category": "Insider Risk Management",
        "subcategory": "Security Violations",
        "description": (
            "Detects risky browser activity including access to dark web sites, data exfiltration "
            "services, hacking forums, and other URLs associated with insider threat behavior."
        ),
        "keywords": [
            "risky browsing", "dark web", "Tor", "hacking forum", "data breach site",
            "paste site", "exfiltration site", "risky URL", "browser history", "web activity",
            "personal email web", "Pastebin", "anonymous browsing", "proxy bypass"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Detect risky URL visits", "Elevate risk score", "Alert security team"],
        "workloads": ["Windows 10/11 Endpoints"],
        "template_available": True,
        "confidence": 79,
        "expected_effects": [
            "Visits to dark web and risky sites are detected on managed endpoints.",
            "Risk scores are elevated when users access known exfiltration or hacking resources.",
            "Security team receives alerts correlated with other suspicious data activities.",
            "Browser activity data contributes to overall insider risk score calculation.",
            "Evidence of risky browsing is captured for investigation purposes.",
        ],
        "troubleshooting_tips": [
            "Risky browser usage detection requires the Purview browser extension to be installed and Endpoint DLP to be active.",
            "Customize the risky URL indicator list with your organization-specific sites of concern in addition to Microsoft's built-in threat intelligence feeds.",
        ],
        "doc_search_query": "Insider Risk risky browser usage dark web Microsoft Purview endpoint browser detection",
    },
    # ── Retention Policy Templates ─────────────────────────────────────────────
    {
        "id": "retention_regulatory_records",
        "name": "Regulatory Records Retention",
        "category": "Data Lifecycle Management",
        "subcategory": "Retention",
        "description": (
            "Implements SEC Rule 17a-4, FINRA, and other regulatory records retention requirements "
            "with immutable storage, 7+ year retention, and write-once read-many (WORM) compliance."
        ),
        "keywords": [
            "regulatory records", "SEC 17a-4", "FINRA", "WORM", "write-once read-many",
            "immutable storage", "financial records", "broker-dealer", "7 year retention",
            "regulatory hold", "compliance records", "books and records", "SEC compliance"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Retain for regulatory period", "Lock retention policy", "Prevent modification", "Trigger disposition review"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": True,
        "confidence": 90,
        "expected_effects": [
            "Regulatory records are retained for the required period (7+ years for SEC/FINRA).",
            "Preservation Lock prevents compliance administrators from shortening retention.",
            "WORM-compliant storage satisfies SEC Rule 17a-4(f) requirements.",
            "Disposition review workflow notifies compliance officers before record deletion.",
            "Immutable audit trail supports regulatory examination requirements.",
        ],
        "troubleshooting_tips": [
            "Enable Preservation Lock ONLY after thorough testing; it cannot be reversed and locks retention settings permanently.",
            "Coordinate with your records management team to map regulatory retention schedules to specific content types and locations.",
        ],
        "doc_search_query": "regulatory records retention SEC FINRA 17a-4 WORM Microsoft Purview immutable compliance",
    },
    {
        "id": "retention_legal_hold",
        "name": "Legal Hold / eDiscovery Preservation",
        "category": "Data Lifecycle Management",
        "subcategory": "Retention",
        "description": (
            "Places content on legal hold to preserve all relevant data for litigation, "
            "regulatory investigation, or eDiscovery, preventing deletion by users or retention policies."
        ),
        "keywords": [
            "legal hold", "litigation hold", "eDiscovery", "preservation", "legal preservation",
            "lawsuit", "litigation", "regulatory investigation", "subpoena", "court order",
            "hold policy", "preserve content", "legal proceedings", "spoliation", "custodian"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Place on legal hold", "Preserve all versions", "Prevent user deletion", "Index for eDiscovery"],
        "workloads": ["Exchange Online", "SharePoint Online", "OneDrive for Business", "Microsoft Teams"],
        "template_available": True,
        "confidence": 92,
        "expected_effects": [
            "All content for specified custodians or locations is preserved regardless of user actions.",
            "User deletions are preserved in hidden locations invisible to the user.",
            "All content versions are retained for complete eDiscovery review.",
            "Content is indexed and searchable in Microsoft Purview eDiscovery.",
            "Legal hold status is tracked and audited for court documentation.",
        ],
        "troubleshooting_tips": [
            "Legal holds take precedence over retention policies; content under legal hold will not be deleted even when a retention policy's delete action applies.",
            "Use custodian-based holds in eDiscovery Premium for targeted preservation rather than broad location-based holds to reduce over-preservation.",
        ],
        "doc_search_query": "legal hold eDiscovery preservation Microsoft Purview litigation hold custodian",
    },
    {
        "id": "retention_email_policy",
        "name": "Email Retention Policy",
        "category": "Data Lifecycle Management",
        "subcategory": "Retention",
        "description": (
            "Retains email messages for defined compliance periods and then permanently deletes them, "
            "helping manage mailbox storage while meeting email record-keeping requirements."
        ),
        "keywords": [
            "email retention", "mailbox retention", "email archive", "email delete",
            "mailbox policy", "email lifecycle", "email compliance", "journaling",
            "email records", "inbox retention", "sent items", "deleted items", "email purge"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Retain email for defined period", "Delete after retention expires", "Preserve in litigation scenarios"],
        "workloads": ["Exchange Online"],
        "template_available": True,
        "confidence": 88,
        "expected_effects": [
            "Emails are retained in recoverable items for the configured retention period.",
            "Users cannot permanently delete emails until the retention period expires.",
            "After the retention period, emails are automatically purged from mailboxes.",
            "Legal holds override deletion for emails involved in active litigation.",
            "eDiscovery can locate all retained emails within the defined period.",
        ],
        "troubleshooting_tips": [
            "Differentiate between Exchange retention policies (legacy MRM) and Microsoft Purview retention policies; they interact and can conflict.",
            "Ensure the retention policy scope covers all required mailboxes including shared mailboxes, resource mailboxes, and Teams channel mailboxes.",
        ],
        "doc_search_query": "email retention policy Microsoft Purview Exchange Online mailbox compliance records",
    },
    {
        "id": "retention_event_based",
        "name": "Event-Based Retention",
        "category": "Data Lifecycle Management",
        "subcategory": "Retention",
        "description": (
            "Triggers retention periods based on specific events such as employee departure, "
            "contract end, product launch, or project closure rather than a fixed date."
        ),
        "keywords": [
            "event-based retention", "event trigger", "employee departure", "contract end",
            "project closure", "product launch", "event-driven", "retention trigger",
            "lifecycle event", "termination event", "record trigger", "asset ID"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Start retention clock on event", "Retain for event-relative period", "Trigger disposition review on expiry"],
        "workloads": ["SharePoint Online", "OneDrive for Business", "Exchange Online"],
        "template_available": True,
        "confidence": 83,
        "expected_effects": [
            "Retention period starts when the specified event occurs, not when content is created.",
            "Employee records are retained for the required period after departure.",
            "Contract documents are retained for the required period after contract end.",
            "Disposition review is triggered at the event-relative retention expiry.",
            "Asset IDs link specific records to specific events for precise retention.",
        ],
        "troubleshooting_tips": [
            "Event-based retention requires content to be labeled with a retention label that has event-based retention configured; unlabeled content will not be triggered.",
            "Create the event type in Purview, then configure auto-labeling or manual labeling workflows to apply the correct labels before the event occurs.",
        ],
        "doc_search_query": "event-based retention Microsoft Purview employee departure contract end trigger",
    },
    {
        "id": "retention_records_management",
        "name": "Records Management - Declare as Records",
        "category": "Data Lifecycle Management",
        "subcategory": "Records Management",
        "description": (
            "Formally declares content as immutable records with a full disposition review workflow, "
            "supporting records management programs and regulatory compliance."
        ),
        "keywords": [
            "records management", "declare as record", "immutable record", "file plan",
            "disposition review", "records schedule", "regulatory record", "vital record",
            "records declaration", "records label", "disposition", "business record",
            "content type records", "locked record"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Declare as record", "Lock content from editing", "Initiate disposition review on expiry", "Maintain file plan"],
        "workloads": ["SharePoint Online", "OneDrive for Business", "Exchange Online"],
        "template_available": True,
        "confidence": 87,
        "expected_effects": [
            "Declared records are locked and cannot be edited or deleted until retention expires.",
            "Disposition reviewers are notified to approve or reject deletion at expiry.",
            "Full audit trail tracks declaration, access, and disposition of every record.",
            "File plan provides an organized taxonomy of record types and schedules.",
            "Meets records management program requirements under ISO 15489 and legal obligations.",
        ],
        "troubleshooting_tips": [
            "Once content is declared as a record, it cannot be edited; ensure users understand the implications before enabling automatic record declaration.",
            "Configure multi-stage disposition review if different approvers are needed (e.g., records manager + legal) before permanent deletion.",
        ],
        "doc_search_query": "records management declare as record Microsoft Purview disposition review file plan immutable",
    },
    # ── Communication Compliance ───────────────────────────────────────────────
    {
        "id": "comm_compliance_financial",
        "name": "Financial Services Communication Compliance",
        "category": "Communication Compliance",
        "subcategory": "Financial Services",
        "description": (
            "Monitors financial services communications for FINRA, SEC, and FCA regulatory compliance, "
            "detecting insider trading signals, market manipulation, conflicts of interest, and prohibited conduct."
        ),
        "keywords": [
            "FINRA", "SEC", "FCA", "financial services", "broker-dealer", "investment advisor",
            "insider trading", "market manipulation", "front running", "conflicts of interest",
            "supervisory review", "registered representative", "communication surveillance",
            "securities", "trading communication", "regulated communication"
        ],
        "sensitive_info_types": [],
        "default_actions": ["Flag for compliance review", "Notify supervisory reviewer", "Generate FINRA audit report", "Preserve flagged communications"],
        "workloads": ["Exchange Online", "Microsoft Teams"],
        "template_available": True,
        "confidence": 86,
        "expected_effects": [
            "All regulated communications are monitored for compliance violations.",
            "Insider trading and market manipulation signals are detected by ML models.",
            "Supervisory reviewers receive flagged communications for review within 24 hours.",
            "FINRA/SEC audit reports document review coverage and disposition.",
            "Preserved communications support regulatory examination and eDiscovery.",
        ],
        "troubleshooting_tips": [
            "Configure reviewer groups carefully to ensure supervisors review their own reports' communications, not each other's, for proper separation.",
            "Tune keyword and ML model sensitivity using the simulation/test mode before going live to calibrate alert volume.",
            "Ensure Teams Direct Routing and third-party communication platforms are connected if your firm uses non-native communication tools.",
        ],
        "doc_search_query": "financial services communication compliance FINRA SEC monitoring Microsoft Purview insider trading",
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

TROUBLESHOOTING_GUIDES = [
    {
        "id": "dlp_not_triggering",
        "title": "DLP Policy Not Triggering",
        "category": "DLP",
        "issues": [
            {
                "problem": "DLP policy is published but emails/files with sensitive content are not being blocked or generating alerts.",
                "solution": "Verify the policy is in 'Enforce' mode (not Simulation/Test). Check that the workload locations (Exchange, SharePoint, etc.) are explicitly included in the policy scope and not excluded. Ensure the policy is assigned to the correct users or groups and has fully propagated (allow up to 24 hours after publishing).",
            },
            {
                "problem": "Sensitive information is present in the document but the DLP rule is not matching.",
                "solution": "Check the confidence level and instance count thresholds in the rule condition. Use 'Test with policy tips' mode and the DLP Activity Explorer to see match details. Verify the sensitive info type pattern against your test content using the 'Test' feature in the SIT editor in Microsoft Purview.",
            },
            {
                "problem": "Policy tips are not appearing for users in Outlook or Office apps.",
                "solution": "Confirm that 'User notifications' / 'Policy tips' are enabled in the DLP rule actions. Policy tips in Outlook require the Outlook client to be version 2016 or later. For Outlook on the web, verify the policy is scoped to Exchange Online and that the user's mailbox is in scope.",
            },
        ],
    },
    {
        "id": "label_sync_delays",
        "title": "Sensitivity Label Sync Delays",
        "category": "Information Protection",
        "issues": [
            {
                "problem": "Newly created or updated sensitivity labels are not appearing in Office apps for users.",
                "solution": "Sensitivity label policy changes can take up to 24 hours to propagate to all clients. Ask the user to sign out and back in to their Office apps, or run 'Get-LabelPolicy' and 'Set-LabelPolicy' in PowerShell to force a policy refresh. Check the label policy is published to the correct users/groups.",
            },
            {
                "problem": "Labels appear in the web portal but not in Outlook, Word, or Excel desktop apps.",
                "solution": "Ensure the Azure Information Protection unified labeling client or built-in Office labeling is enabled. For built-in labeling, verify the Microsoft 365 Apps version supports the label features in use. Check for Group Policy or Intune configuration that might be blocking the labeling experience.",
            },
            {
                "problem": "Auto-labeling policy is configured but labels are not being applied to existing content.",
                "solution": "Auto-labeling for existing content (SharePoint/OneDrive) runs as a background crawl that may take several days for large repositories. Check the auto-labeling policy status page in the Purview portal for progress. For Exchange, auto-labeling applies at send/receive time only and does not retroactively label existing emails.",
            },
        ],
    },
    {
        "id": "false_positives",
        "title": "Reducing DLP False Positives",
        "category": "DLP",
        "issues": [
            {
                "problem": "DLP policy is blocking legitimate business emails or documents (false positives).",
                "solution": "Increase the confidence level threshold in the DLP rule condition from 'Low' to 'Medium' or 'High'. Increase the instance count minimum (e.g., require at least 2 matches instead of 1). Add corroborating evidence conditions using keyword proximity to require sensitive data to appear near confirming context words.",
            },
            {
                "problem": "Test data, demo environments, or training materials are triggering DLP policies.",
                "solution": "Create an exception group for test/demo accounts and exclude them from the DLP policy. Use document property or sensitivity label conditions to exempt content explicitly marked as 'test' or 'sample'. Consider a separate simulation-mode policy for non-production environments.",
            },
            {
                "problem": "Specific users or teams frequently trigger false positives due to their legitimate work.",
                "solution": "Add role-based exceptions in the DLP policy for users whose job function legitimately involves the sensitive data types (e.g., HR staff can handle SSNs). Use business justification override instead of blocking for these groups, and audit overrides regularly to ensure they are legitimate.",
            },
        ],
    },
    {
        "id": "policy_conflicts",
        "title": "Policy Conflict Resolution",
        "category": "DLP",
        "issues": [
            {
                "problem": "Multiple DLP policies apply to the same content and it is unclear which one takes precedence.",
                "solution": "Microsoft Purview evaluates all matching DLP policies and applies the most restrictive action. Review the 'DLP policy precedence' order in the Purview portal and set priority order explicitly. Use the DLP rule match details in Activity Explorer to see which specific rule triggered for a given event.",
            },
            {
                "problem": "A retention policy and a DLP policy conflict, causing unexpected content deletion or preservation.",
                "solution": "Legal holds and retention policies always take precedence over deletion; DLP does not delete content. If content is being unexpectedly preserved, check for active legal holds or retention policies applied to the location. Use the Content Explorer to inspect which retention labels or holds are applied to specific content.",
            },
            {
                "problem": "Sensitivity label encryption conflicts with DLP policy actions, causing double encryption or failed access.",
                "solution": "If a sensitivity label applies encryption, ensure the DLP policy's encryption action is not also applied, as double encryption can prevent authorized users from accessing content. Coordinate label-based encryption with DLP actions so each handles its own protection layer without redundancy.",
            },
        ],
    },
    {
        "id": "teams_dlp_issues",
        "title": "Teams DLP Common Issues",
        "category": "DLP",
        "issues": [
            {
                "problem": "DLP policy is applied to Exchange Online but is not protecting Teams messages.",
                "solution": "Teams chat and channel messages require 'Microsoft Teams' to be explicitly selected as a workload in the DLP policy location settings. Exchange Online and Teams are separate workloads; a policy scoped only to Exchange will not protect Teams messages. Edit the policy to include Teams chat and channel messages.",
            },
            {
                "problem": "DLP policy tips are not appearing in Teams for end users.",
                "solution": "Teams DLP policy tips are supported in Teams desktop and web clients for 1:1 chats and channel messages. Policy tips are not supported in Teams mobile app. Ensure the Teams client is updated to a recent version. Verify that user notifications are enabled in the DLP rule for the Teams workload.",
            },
            {
                "problem": "Sensitive content shared in Teams meetings or calls is not being detected.",
                "solution": "DLP policies for Teams currently apply to chat messages and file attachments, not to real-time audio/video content in meetings. For meeting chat messages, ensure the policy covers Teams. For content shared via screen sharing, consider endpoint DLP on managed devices as a compensating control.",
            },
        ],
    },
]

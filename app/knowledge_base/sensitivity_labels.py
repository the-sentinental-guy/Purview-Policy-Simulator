"""Sensitivity labels knowledge base for Microsoft Purview Policy Simulator."""
from typing import Any, Dict, List


def get_sensitivity_labels() -> List[Dict[str, Any]]:
    """Return a comprehensive list of sensitivity labels with full taxonomy."""
    return [
        # ── PUBLIC ───────────────────────────────────────────────────────────
        {
            "id": "public",
            "name": "Public",
            "parent": None,
            "description": (
                "Content that is approved for public consumption and can be shared freely "
                "with anyone inside or outside the organisation. No restrictions on access, "
                "distribution, or disclosure. Suitable for press releases, public websites, "
                "marketing materials, and general announcements."
            ),
            "encryption": {
                "enabled": False,
                "type": None,
                "permissions": [],
                "double_key_encryption": False,
            },
            "content_marking": {
                "header": {"enabled": False, "text": None},
                "footer": {"enabled": False, "text": None},
                "watermark": {"enabled": False, "text": None},
            },
            "scope": ["files", "emails", "meetings", "groups_sites", "power_bi"],
            "auto_labeling": {
                "enabled": False,
                "conditions": [],
                "mode": None,
            },
            "priority": 0,
            "keywords": [
                "public", "press release", "marketing", "general availability",
                "public announcement", "open data", "publicly available",
                "no restriction", "unrestricted", "public website",
            ],
            "color": "#00B050",
        },
        {
            "id": "public_anyone",
            "name": "Public\\Anyone",
            "parent": "public",
            "description": (
                "Explicitly marks content intended for unrestricted distribution to any audience, "
                "including external parties, customers, and the general public. Used for official "
                "public communications, published reports, and externally facing documentation."
            ),
            "encryption": {
                "enabled": False,
                "type": None,
                "permissions": [],
                "double_key_encryption": False,
            },
            "content_marking": {
                "header": {"enabled": True, "text": "PUBLIC"},
                "footer": {"enabled": False, "text": None},
                "watermark": {"enabled": False, "text": None},
            },
            "scope": ["files", "emails"],
            "auto_labeling": {
                "enabled": False,
                "conditions": [],
                "mode": None,
            },
            "priority": 1,
            "keywords": [
                "public document", "public report", "external publication",
                "press kit", "media release", "published content",
            ],
            "color": "#00B050",
        },

        # ── GENERAL ──────────────────────────────────────────────────────────
        {
            "id": "general",
            "name": "General",
            "parent": None,
            "description": (
                "Non-sensitive internal business content intended for all employees. Content that "
                "does not require special handling but is not intended for wide external distribution. "
                "Suitable for internal memos, routine business correspondence, and general "
                "operational materials that would cause minimal harm if disclosed externally."
            ),
            "encryption": {
                "enabled": False,
                "type": None,
                "permissions": [],
                "double_key_encryption": False,
            },
            "content_marking": {
                "header": {"enabled": False, "text": None},
                "footer": {"enabled": True, "text": "GENERAL"},
                "watermark": {"enabled": False, "text": None},
            },
            "scope": ["files", "emails", "meetings", "groups_sites", "power_bi"],
            "auto_labeling": {
                "enabled": False,
                "conditions": [],
                "mode": None,
            },
            "priority": 2,
            "keywords": [
                "general", "internal", "all employees", "routine", "standard",
                "non-sensitive", "business as usual", "operational", "internal memo",
                "general distribution", "unrestricted internal",
            ],
            "color": "#FFFF00",
        },
        {
            "id": "general_all_employees",
            "name": "General\\All Employees",
            "parent": "general",
            "description": (
                "Internal content accessible to all employees without restriction. Includes general "
                "company announcements, HR communications, policy updates, internal newsletters, "
                "and routine operational documents that all staff should be able to access."
            ),
            "encryption": {
                "enabled": False,
                "type": None,
                "permissions": [],
                "double_key_encryption": False,
            },
            "content_marking": {
                "header": {"enabled": False, "text": None},
                "footer": {"enabled": True, "text": "GENERAL - All Employees"},
                "watermark": {"enabled": False, "text": None},
            },
            "scope": ["files", "emails", "meetings"],
            "auto_labeling": {
                "enabled": False,
                "conditions": [],
                "mode": None,
            },
            "priority": 3,
            "keywords": [
                "all staff", "company-wide", "internal announcement", "HR policy",
                "employee communication", "staff notice", "general policy",
            ],
            "color": "#FFFF00",
        },
        {
            "id": "general_anyone",
            "name": "General\\Anyone (unrestricted)",
            "parent": "general",
            "description": (
                "General internal content that may also be shared externally with partners, "
                "vendors, or customers without special handling requirements. Suitable for "
                "product documentation, vendor communications, and partner-facing materials "
                "that contain no sensitive business information."
            ),
            "encryption": {
                "enabled": False,
                "type": None,
                "permissions": [],
                "double_key_encryption": False,
            },
            "content_marking": {
                "header": {"enabled": False, "text": None},
                "footer": {"enabled": True, "text": "GENERAL - Unrestricted"},
                "watermark": {"enabled": False, "text": None},
            },
            "scope": ["files", "emails"],
            "auto_labeling": {
                "enabled": False,
                "conditions": [],
                "mode": None,
            },
            "priority": 4,
            "keywords": [
                "unrestricted", "shareable", "vendor communication", "partner material",
                "external sharing allowed", "product documentation",
            ],
            "color": "#FFFF00",
        },

        # ── CONFIDENTIAL ─────────────────────────────────────────────────────
        {
            "id": "confidential",
            "name": "Confidential",
            "parent": None,
            "description": (
                "Sensitive business content that requires protection from unauthorised access. "
                "Content whose disclosure could adversely affect the organisation, its employees, "
                "customers, or partners. Includes business strategies, financial projections, "
                "personnel data, customer information, and proprietary processes. Access should "
                "be limited to those with a legitimate business need."
            ),
            "encryption": {
                "enabled": True,
                "type": "admin_defined",
                "permissions": [
                    {"role": "Author", "rights": ["View", "Edit", "Print", "Copy", "Reply", "ReplyAll", "Forward", "Extract", "Sign", "Comment"]},
                    {"role": "Co-Author", "rights": ["View", "Edit", "Print", "Reply", "ReplyAll", "Forward"]},
                    {"role": "Co-Owner", "rights": ["View", "Edit", "Print", "Copy", "Reply", "ReplyAll", "Forward", "Extract", "Sign", "Comment", "Owner"]},
                    {"role": "Reviewer", "rights": ["View", "Reply", "ReplyAll", "Forward"]},
                    {"role": "Viewer", "rights": ["View"]},
                ],
                "double_key_encryption": False,
            },
            "content_marking": {
                "header": {"enabled": True, "text": "CONFIDENTIAL"},
                "footer": {"enabled": True, "text": "Confidential – Handle with care"},
                "watermark": {"enabled": False, "text": None},
            },
            "scope": ["files", "emails", "meetings", "groups_sites", "power_bi"],
            "auto_labeling": {
                "enabled": True,
                "conditions": [
                    {"type": "sensitive_info_type", "value": "Credit Card Number", "confidence": 85},
                    {"type": "sensitive_info_type", "value": "Social Security Number", "confidence": 85},
                    {"type": "sensitive_info_type", "value": "Bank Account Number", "confidence": 85},
                    {"type": "keyword", "value": "confidential", "confidence": 75},
                    {"type": "keyword", "value": "proprietary", "confidence": 75},
                ],
                "mode": "recommend",
            },
            "priority": 5,
            "keywords": [
                "confidential", "sensitive", "restricted", "proprietary", "need to know",
                "business sensitive", "internal use only", "limited distribution",
                "not for distribution", "private", "protected information",
                "business strategy", "competitive information",
            ],
            "color": "#FF0000",
        },
        {
            "id": "confidential_all_employees",
            "name": "Confidential\\All Employees",
            "parent": "confidential",
            "description": (
                "Confidential content accessible to all authenticated employees within the "
                "organisation. Cannot be shared externally without explicit authorisation. "
                "Includes internal financial reports, business plans, personnel policies, "
                "organisational charts, and internal strategy documents."
            ),
            "encryption": {
                "enabled": True,
                "type": "admin_defined",
                "permissions": [
                    {"role": "All Employees", "rights": ["View", "Edit", "Reply", "ReplyAll", "Forward"]},
                    {"role": "Author", "rights": ["View", "Edit", "Print", "Copy", "Reply", "ReplyAll", "Forward", "Extract", "Sign", "Comment"]},
                ],
                "double_key_encryption": False,
            },
            "content_marking": {
                "header": {"enabled": True, "text": "CONFIDENTIAL - All Employees"},
                "footer": {"enabled": True, "text": "Confidential – Not for external distribution"},
                "watermark": {"enabled": False, "text": None},
            },
            "scope": ["files", "emails", "meetings"],
            "auto_labeling": {
                "enabled": True,
                "conditions": [
                    {"type": "keyword", "value": "internal only", "confidence": 80},
                    {"type": "keyword", "value": "staff confidential", "confidence": 80},
                    {"type": "sensitive_info_type", "value": "Employee ID", "confidence": 75},
                ],
                "mode": "recommend",
            },
            "priority": 6,
            "keywords": [
                "internal only", "staff confidential", "all employees", "employee data",
                "HR confidential", "internal strategy", "business plan", "financial projection",
                "headcount", "salary band", "organisational chart",
            ],
            "color": "#FF0000",
        },
        {
            "id": "confidential_finance_only",
            "name": "Confidential\\Finance Only",
            "parent": "confidential",
            "description": (
                "Highly sensitive financial data restricted to authorised Finance department "
                "personnel. Includes unpublished earnings, budget forecasts, cost structures, "
                "M&A financial modelling, audit findings, tax strategy, treasury positions, "
                "and other financial data that could materially affect the organisation if "
                "disclosed prematurely or to unauthorised individuals."
            ),
            "encryption": {
                "enabled": True,
                "type": "admin_defined",
                "permissions": [
                    {"role": "Finance Team", "rights": ["View", "Edit", "Print", "Copy", "Reply", "ReplyAll", "Forward", "Extract", "Sign", "Comment"]},
                    {"role": "Finance Leadership", "rights": ["View", "Edit", "Print", "Copy", "Reply", "ReplyAll", "Forward", "Extract", "Sign", "Comment", "Owner"]},
                    {"role": "CFO", "rights": ["View", "Edit", "Print", "Copy", "Reply", "ReplyAll", "Forward", "Extract", "Sign", "Comment", "Owner"]},
                ],
                "double_key_encryption": False,
            },
            "content_marking": {
                "header": {"enabled": True, "text": "CONFIDENTIAL - Finance Only"},
                "footer": {"enabled": True, "text": "Finance Confidential – Restricted Access"},
                "watermark": {"enabled": True, "text": "FINANCE CONFIDENTIAL"},
            },
            "scope": ["files", "emails", "power_bi"],
            "auto_labeling": {
                "enabled": True,
                "conditions": [
                    {"type": "sensitive_info_type", "value": "Financial Account Number", "confidence": 85},
                    {"type": "keyword", "value": "EBITDA", "confidence": 80},
                    {"type": "keyword", "value": "earnings per share", "confidence": 80},
                    {"type": "keyword", "value": "budget forecast", "confidence": 75},
                    {"type": "keyword", "value": "quarterly earnings", "confidence": 80},
                ],
                "mode": "auto_apply",
            },
            "priority": 7,
            "keywords": [
                "finance only", "financial data", "budget", "forecast", "earnings",
                "EBITDA", "revenue", "profit", "loss", "balance sheet", "cash flow",
                "audit", "tax", "treasury", "M&A", "financial model", "cost structure",
                "unpublished results", "quarterly results", "annual results", "CFO",
            ],
            "color": "#FF0000",
        },
        {
            "id": "confidential_legal",
            "name": "Confidential\\Legal",
            "parent": "confidential",
            "description": (
                "Legally privileged or sensitive legal content restricted to the Legal department "
                "and authorised counsel. Includes attorney-client privileged communications, "
                "litigation strategy, legal opinions, contract negotiations, regulatory "
                "investigations, intellectual property filings, and other materials protected "
                "by legal professional privilege."
            ),
            "encryption": {
                "enabled": True,
                "type": "admin_defined",
                "permissions": [
                    {"role": "Legal Team", "rights": ["View", "Edit", "Print", "Copy", "Reply", "ReplyAll", "Forward", "Extract", "Sign", "Comment"]},
                    {"role": "General Counsel", "rights": ["View", "Edit", "Print", "Copy", "Reply", "ReplyAll", "Forward", "Extract", "Sign", "Comment", "Owner"]},
                    {"role": "Outside Counsel", "rights": ["View", "Edit", "Reply", "ReplyAll", "Forward"]},
                ],
                "double_key_encryption": False,
            },
            "content_marking": {
                "header": {"enabled": True, "text": "CONFIDENTIAL - Legal Privileged"},
                "footer": {"enabled": True, "text": "Attorney-Client Privilege – Do Not Distribute"},
                "watermark": {"enabled": True, "text": "LEGAL PRIVILEGED"},
            },
            "scope": ["files", "emails"],
            "auto_labeling": {
                "enabled": True,
                "conditions": [
                    {"type": "keyword", "value": "attorney-client privilege", "confidence": 90},
                    {"type": "keyword", "value": "legal opinion", "confidence": 80},
                    {"type": "keyword", "value": "litigation hold", "confidence": 85},
                    {"type": "keyword", "value": "privileged and confidential", "confidence": 85},
                    {"type": "keyword", "value": "without prejudice", "confidence": 80},
                ],
                "mode": "recommend",
            },
            "priority": 8,
            "keywords": [
                "legal", "attorney-client privilege", "privileged", "legal opinion",
                "litigation", "contract", "regulatory", "intellectual property",
                "patent", "trademark", "legal hold", "discovery", "settlement",
                "outside counsel", "general counsel", "legal advice", "without prejudice",
                "confidential legal", "court order", "regulatory investigation",
            ],
            "color": "#FF0000",
        },

        # ── HIGHLY CONFIDENTIAL ───────────────────────────────────────────────
        {
            "id": "highly_confidential",
            "name": "Highly Confidential",
            "parent": None,
            "description": (
                "The most sensitive category of information requiring the highest level of "
                "protection. Unauthorised disclosure could cause severe damage to the "
                "organisation, individuals, or national security. Includes trade secrets, "
                "board-level decisions, executive compensation, government classified data, "
                "and critical security vulnerabilities. Access strictly limited on a strict "
                "need-to-know basis with full audit trail."
            ),
            "encryption": {
                "enabled": True,
                "type": "admin_defined",
                "permissions": [
                    {"role": "Author", "rights": ["View", "Edit", "Print", "Copy", "Reply", "ReplyAll", "Forward", "Extract", "Sign", "Comment", "Owner"]},
                    {"role": "Highly Confidential Readers", "rights": ["View"]},
                ],
                "double_key_encryption": False,
                "offline_access": "never",
                "content_expiry_days": 30,
            },
            "content_marking": {
                "header": {"enabled": True, "text": "HIGHLY CONFIDENTIAL"},
                "footer": {"enabled": True, "text": "Highly Confidential – Strictly Need to Know"},
                "watermark": {"enabled": True, "text": "HIGHLY CONFIDENTIAL"},
            },
            "scope": ["files", "emails", "meetings", "groups_sites", "power_bi"],
            "auto_labeling": {
                "enabled": True,
                "conditions": [
                    {"type": "sensitive_info_type", "value": "EU Passport Number", "confidence": 90},
                    {"type": "sensitive_info_type", "value": "U.S. Social Security Number", "confidence": 90},
                    {"type": "sensitive_info_type", "value": "Drug Enforcement Agency (DEA) Number", "confidence": 90},
                    {"type": "keyword", "value": "trade secret", "confidence": 85},
                    {"type": "keyword", "value": "board confidential", "confidence": 90},
                    {"type": "keyword", "value": "strictly confidential", "confidence": 85},
                ],
                "mode": "auto_apply",
            },
            "priority": 9,
            "keywords": [
                "highly confidential", "top secret", "strictly confidential", "trade secret",
                "board confidential", "executive only", "need to know", "classified",
                "sensitive compartmented", "critical", "restricted access", "eyes only",
                "not for disclosure", "critical vulnerability", "zero day", "executive compensation",
            ],
            "color": "#C00000",
        },
        {
            "id": "highly_confidential_all_employees",
            "name": "Highly Confidential\\All Employees",
            "parent": "highly_confidential",
            "description": (
                "Highly confidential content that requires access controls for all employees but "
                "must never leave the organisation's control. Includes critical internal security "
                "policies, major unreleased product announcements, significant corporate events, "
                "and sensitive employee matters that affect the entire organisation."
            ),
            "encryption": {
                "enabled": True,
                "type": "admin_defined",
                "permissions": [
                    {"role": "All Employees", "rights": ["View"]},
                    {"role": "Author", "rights": ["View", "Edit", "Print", "Copy", "Reply", "ReplyAll", "Forward", "Extract", "Sign", "Comment", "Owner"]},
                ],
                "double_key_encryption": False,
                "offline_access": "never",
                "content_expiry_days": 90,
            },
            "content_marking": {
                "header": {"enabled": True, "text": "HIGHLY CONFIDENTIAL - All Employees"},
                "footer": {"enabled": True, "text": "Highly Confidential – Internal Distribution Only"},
                "watermark": {"enabled": True, "text": "HIGHLY CONFIDENTIAL"},
            },
            "scope": ["files", "emails", "meetings"],
            "auto_labeling": {
                "enabled": True,
                "conditions": [
                    {"type": "keyword", "value": "company confidential", "confidence": 85},
                    {"type": "keyword", "value": "internal announcement only", "confidence": 85},
                ],
                "mode": "recommend",
            },
            "priority": 10,
            "keywords": [
                "company confidential", "internal announcement", "critical internal",
                "major announcement", "significant event", "corporate action",
                "all employee sensitive", "critical security policy",
            ],
            "color": "#C00000",
        },
        {
            "id": "highly_confidential_external_partners",
            "name": "Highly Confidential\\External Partners",
            "parent": "highly_confidential",
            "description": (
                "Highly confidential content shared under strict NDA with named external partners, "
                "joint venture participants, or authorised third parties. Recipients are explicitly "
                "named and access is time-limited. Includes shared IP development, joint venture "
                "details, M&A due diligence materials, and technology licensing terms shared under "
                "mutual confidentiality agreements."
            ),
            "encryption": {
                "enabled": True,
                "type": "user_defined",
                "permissions": [
                    {"role": "Named External Partner", "rights": ["View"]},
                    {"role": "Author", "rights": ["View", "Edit", "Print", "Copy", "Reply", "ReplyAll", "Forward", "Extract", "Sign", "Comment", "Owner"]},
                ],
                "double_key_encryption": False,
                "offline_access": "never",
                "content_expiry_days": 14,
                "require_authentication": True,
            },
            "content_marking": {
                "header": {"enabled": True, "text": "HIGHLY CONFIDENTIAL - External Partners"},
                "footer": {"enabled": True, "text": "Subject to NDA – Do not further distribute"},
                "watermark": {"enabled": True, "text": "HC EXTERNAL - NDA PROTECTED"},
            },
            "scope": ["files", "emails"],
            "auto_labeling": {
                "enabled": False,
                "conditions": [],
                "mode": None,
            },
            "priority": 11,
            "keywords": [
                "NDA", "external partner", "joint venture", "due diligence", "M&A",
                "technology licensing", "mutual confidentiality", "third party confidential",
                "partner NDA", "under agreement", "shared IP", "joint development",
            ],
            "color": "#C00000",
        },
        {
            "id": "highly_confidential_board",
            "name": "Highly Confidential\\Board",
            "parent": "highly_confidential",
            "description": (
                "Exclusively for board of directors and C-suite executives. Contains the most "
                "sensitive corporate governance materials including board meeting minutes, "
                "executive session notes, CEO performance reviews, succession planning, "
                "major strategic pivots, and material non-public information (MNPI). "
                "Disclosure of this content could violate securities regulations or cause "
                "irreparable reputational harm."
            ),
            "encryption": {
                "enabled": True,
                "type": "admin_defined",
                "permissions": [
                    {"role": "Board Members", "rights": ["View", "Print"]},
                    {"role": "C-Suite", "rights": ["View", "Print"]},
                    {"role": "Board Secretary", "rights": ["View", "Edit", "Print", "Copy", "Sign", "Comment", "Owner"]},
                ],
                "double_key_encryption": True,
                "offline_access": "never",
                "content_expiry_days": 7,
                "require_authentication": True,
            },
            "content_marking": {
                "header": {"enabled": True, "text": "HIGHLY CONFIDENTIAL - BOARD ONLY"},
                "footer": {"enabled": True, "text": "Board Confidential – MNPI – Not for Distribution"},
                "watermark": {"enabled": True, "text": "BOARD CONFIDENTIAL"},
            },
            "scope": ["files", "emails", "meetings"],
            "auto_labeling": {
                "enabled": False,
                "conditions": [],
                "mode": None,
            },
            "priority": 12,
            "keywords": [
                "board only", "board meeting", "board minutes", "executive session",
                "MNPI", "material non-public", "C-suite", "CEO", "CFO", "succession",
                "governance", "board resolution", "board approval", "strategic pivot",
                "executive compensation", "board confidential",
            ],
            "color": "#C00000",
        },
        {
            "id": "highly_confidential_dke",
            "name": "Highly Confidential\\Double Key Encrypted",
            "parent": "highly_confidential",
            "description": (
                "Maximum protection using Double Key Encryption (DKE), requiring both Microsoft's "
                "key and the organisation's own encryption key to decrypt. Content cannot be "
                "accessed by Microsoft, cloud administrators, or government agencies without the "
                "organisation's key. Intended for the most sensitive regulated data, sovereign "
                "secrets, critical national infrastructure details, and content subject to the "
                "strictest sovereignty requirements."
            ),
            "encryption": {
                "enabled": True,
                "type": "double_key_encryption",
                "permissions": [
                    {"role": "DKE Authorised Users", "rights": ["View", "Edit"]},
                    {"role": "DKE Owners", "rights": ["View", "Edit", "Print", "Copy", "Sign", "Comment", "Owner"]},
                ],
                "double_key_encryption": True,
                "dke_service_url": "https://dke.contoso.com",
                "offline_access": "never",
                "require_authentication": True,
            },
            "content_marking": {
                "header": {"enabled": True, "text": "HIGHLY CONFIDENTIAL - DKE PROTECTED"},
                "footer": {"enabled": True, "text": "Double Key Encrypted – Sovereign Protection"},
                "watermark": {"enabled": True, "text": "DKE PROTECTED - SOVEREIGN"},
            },
            "scope": ["files", "emails"],
            "auto_labeling": {
                "enabled": False,
                "conditions": [],
                "mode": None,
            },
            "priority": 13,
            "keywords": [
                "double key encryption", "DKE", "sovereign", "sovereignty", "national secret",
                "critical infrastructure", "government classified", "highest sensitivity",
                "cloud sovereign", "data sovereignty", "regulatory sovereign",
                "maximum protection", "DKE protected",
            ],
            "color": "#7030A0",
        },
    ]


def get_label_policies() -> List[Dict[str, Any]]:
    """Return common sensitivity label policy configurations."""
    return [
        {
            "id": "default_labeling_policy",
            "name": "Default Labeling Policy",
            "description": (
                "Organisation-wide labeling policy that applies sensitivity labels to all "
                "Microsoft 365 apps and services. Enforces mandatory labeling for emails and "
                "documents, recommends the General label as default for new content, and "
                "provides users with the full label taxonomy for manual selection."
            ),
            "published_labels": [
                "public", "public_anyone",
                "general", "general_all_employees", "general_anyone",
                "confidential", "confidential_all_employees", "confidential_finance_only",
                "confidential_legal",
                "highly_confidential", "highly_confidential_all_employees",
                "highly_confidential_external_partners", "highly_confidential_board",
                "highly_confidential_dke",
            ],
            "settings": {
                "mandatory_labeling": True,
                "mandatory_labeling_scope": ["emails", "documents"],
                "default_label": "general_all_employees",
                "default_label_for_emails": "general_all_employees",
                "default_label_for_meetings": "general",
                "require_justification_to_lower": True,
                "require_justification_to_remove": True,
                "show_help_link": True,
                "help_link_url": "https://aka.ms/sensitivitylabels",
                "label_bar_visible_in_apps": True,
                "audit_labeling_activities": True,
            },
            "assigned_to": ["All Users", "All Groups"],
            "scope": ["files", "emails", "meetings", "groups_sites", "power_bi"],
            "keywords": [
                "default policy", "mandatory labeling", "organisation-wide",
                "all users", "label taxonomy", "general default",
            ],
        },
        {
            "id": "finance_labeling_policy",
            "name": "Finance Department Labeling Policy",
            "description": (
                "Enhanced labeling policy for Finance department users that enforces stricter "
                "default labels and mandatory labeling. Sets the default label to "
                "Confidential\\Finance Only for all new documents created by Finance users. "
                "Requires justification for any label downgrade and enables auto-labeling "
                "for financial content types."
            ),
            "published_labels": [
                "general", "general_all_employees",
                "confidential", "confidential_all_employees", "confidential_finance_only",
                "highly_confidential", "highly_confidential_all_employees",
            ],
            "settings": {
                "mandatory_labeling": True,
                "mandatory_labeling_scope": ["emails", "documents"],
                "default_label": "confidential_finance_only",
                "default_label_for_emails": "confidential_finance_only",
                "require_justification_to_lower": True,
                "require_justification_to_remove": True,
                "show_help_link": True,
                "help_link_url": "https://aka.ms/financelabeling",
                "label_bar_visible_in_apps": True,
                "audit_labeling_activities": True,
                "prevent_guest_access_to_labeled_sites": True,
            },
            "assigned_to": ["Finance Department", "Finance Leadership", "CFO Office"],
            "scope": ["files", "emails", "power_bi"],
            "keywords": [
                "finance policy", "finance labeling", "financial data", "finance department",
                "mandatory finance label", "CFO", "finance default label",
            ],
        },
        {
            "id": "legal_labeling_policy",
            "name": "Legal Department Labeling Policy",
            "description": (
                "Specialised labeling policy for Legal department personnel enforcing attorney-client "
                "privilege and legal confidentiality labels. Sets default label to "
                "Confidential\\Legal for all content created by legal staff. Enables audit logging "
                "of all label changes and requires senior approval to downgrade labels on legal docs."
            ),
            "published_labels": [
                "general", "general_all_employees",
                "confidential", "confidential_all_employees", "confidential_legal",
                "highly_confidential", "highly_confidential_all_employees",
                "highly_confidential_board",
            ],
            "settings": {
                "mandatory_labeling": True,
                "mandatory_labeling_scope": ["emails", "documents"],
                "default_label": "confidential_legal",
                "default_label_for_emails": "confidential_legal",
                "require_justification_to_lower": True,
                "require_justification_to_remove": True,
                "show_help_link": True,
                "help_link_url": "https://aka.ms/legallabeling",
                "label_bar_visible_in_apps": True,
                "audit_labeling_activities": True,
                "prevent_guest_access_to_labeled_sites": True,
            },
            "assigned_to": ["Legal Department", "General Counsel", "Outside Counsel"],
            "scope": ["files", "emails"],
            "keywords": [
                "legal policy", "legal labeling", "attorney-client", "legal department",
                "privilege label", "legal default", "outside counsel policy",
            ],
        },
        {
            "id": "board_labeling_policy",
            "name": "Board and Executive Labeling Policy",
            "description": (
                "Highest-restriction labeling policy for board members, C-suite executives, and "
                "board secretariat. All content defaults to Highly Confidential\\Board. Enables "
                "Double Key Encryption capability. Enforces watermarks and content markings on "
                "all labelled documents. Disables all external sharing from labelled containers."
            ),
            "published_labels": [
                "confidential", "confidential_all_employees",
                "highly_confidential", "highly_confidential_all_employees",
                "highly_confidential_board", "highly_confidential_dke",
            ],
            "settings": {
                "mandatory_labeling": True,
                "mandatory_labeling_scope": ["emails", "documents", "meetings"],
                "default_label": "highly_confidential_board",
                "default_label_for_emails": "highly_confidential_board",
                "default_label_for_meetings": "highly_confidential_board",
                "require_justification_to_lower": True,
                "require_justification_to_remove": True,
                "show_help_link": True,
                "help_link_url": "https://aka.ms/boardlabeling",
                "label_bar_visible_in_apps": True,
                "audit_labeling_activities": True,
                "prevent_guest_access_to_labeled_sites": True,
                "block_external_sharing": True,
                "enforce_content_markings": True,
            },
            "assigned_to": ["Board Members", "C-Suite", "Board Secretariat"],
            "scope": ["files", "emails", "meetings"],
            "keywords": [
                "board policy", "executive labeling", "C-suite", "board member",
                "governance labeling", "board documents", "executive default label",
                "board secretary", "MNPI labeling",
            ],
        },
        {
            "id": "auto_labeling_policy_client_data",
            "name": "Auto-Labeling Policy – Customer PII",
            "description": (
                "Server-side auto-labeling policy that automatically applies Confidential\\All Employees "
                "to any content at rest in SharePoint, OneDrive, or Exchange that contains customer "
                "personally identifiable information (PII). Runs continuously in simulation mode "
                "first, then enforces after review. Covers customer names, addresses, email addresses, "
                "phone numbers, national ID numbers, and financial account identifiers."
            ),
            "published_labels": ["confidential_all_employees"],
            "settings": {
                "auto_labeling_enabled": True,
                "simulation_mode": False,
                "apply_label": "confidential_all_employees",
                "conditions": [
                    {"type": "sensitive_info_type", "value": "Person's Name", "instance_count_min": 1, "confidence": 85},
                    {"type": "sensitive_info_type", "value": "Physical Addresses", "instance_count_min": 1, "confidence": 85},
                    {"type": "sensitive_info_type", "value": "EU Social Security Number", "instance_count_min": 1, "confidence": 85},
                    {"type": "sensitive_info_type", "value": "UK National Insurance Number", "instance_count_min": 1, "confidence": 85},
                    {"type": "sensitive_info_type", "value": "Credit Card Number", "instance_count_min": 1, "confidence": 85},
                ],
                "condition_operator": "OR",
                "locations": ["SharePoint", "OneDrive", "Exchange"],
                "audit_labeling_activities": True,
                "notify_user": True,
            },
            "assigned_to": ["All Locations"],
            "scope": ["files", "emails"],
            "keywords": [
                "auto-labeling", "automatic label", "PII", "customer data", "personal data",
                "GDPR", "sensitive info type", "server-side labeling", "data at rest",
                "SharePoint auto-label", "OneDrive auto-label",
            ],
        },
    ]

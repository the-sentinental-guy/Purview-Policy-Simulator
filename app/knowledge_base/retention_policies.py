"""Retention policies and records management knowledge base for Microsoft Purview Policy Simulator."""
from typing import Any, Dict, List


def get_retention_labels() -> List[Dict[str, Any]]:
    """Return a comprehensive list of retention labels covering all retention behaviours."""
    return [
        # ── RETAIN ONLY ──────────────────────────────────────────────────────
        {
            "id": "retain_7yr_financial",
            "name": "Retain 7 Years – Financial Records",
            "behavior": "retain_only",
            "retention_period_years": 7,
            "retention_trigger": "creation_date",
            "event_based": False,
            "description": (
                "Retains financial records for a minimum of 7 years from creation date in "
                "compliance with statutory accounting and tax requirements. Applies to general "
                "ledgers, accounts payable/receivable, bank statements, tax filings, invoices, "
                "expense reports, payroll records, and financial audit documentation. "
                "Prevents premature deletion but does not enforce automatic deletion at end of period."
            ),
            "applies_to": ["SharePoint", "OneDrive", "Exchange", "Teams"],
            "regulatory_basis": ["SOX", "IRS Rev. Proc. 98-25", "Companies Act 2006", "HMRC"],
            "record_type": None,
            "immutable": False,
            "disposition_review": False,
            "auto_apply_conditions": [
                {"type": "keyword", "value": "invoice", "confidence": 80},
                {"type": "keyword", "value": "financial statement", "confidence": 80},
                {"type": "keyword", "value": "tax return", "confidence": 85},
                {"type": "keyword", "value": "audit report", "confidence": 80},
                {"type": "sensitive_info_type", "value": "Financial Account Number", "confidence": 80},
            ],
            "priority": 5,
            "keywords": [
                "financial records", "7 year retention", "accounting records", "tax records",
                "invoice retention", "audit trail", "SOX compliance", "financial compliance",
                "general ledger", "accounts payable", "accounts receivable", "payroll",
                "expense report", "bank statement", "financial audit",
            ],
        },
        {
            "id": "retain_3yr_contracts",
            "name": "Retain 3 Years – General Contracts",
            "behavior": "retain_only",
            "retention_period_years": 3,
            "retention_trigger": "modification_date",
            "event_based": False,
            "description": (
                "Retains general commercial contracts and agreements for 3 years after last "
                "modification. Covers vendor agreements, service contracts, non-disclosure "
                "agreements, licence agreements, and standard purchase orders. Ensures contractual "
                "obligations and dispute resolution evidence remains available throughout the "
                "limitation period for breach of contract claims."
            ),
            "applies_to": ["SharePoint", "OneDrive", "Exchange"],
            "regulatory_basis": ["Limitation Act 1980", "UCC Article 2"],
            "record_type": None,
            "immutable": False,
            "disposition_review": False,
            "auto_apply_conditions": [
                {"type": "keyword", "value": "agreement", "confidence": 70},
                {"type": "keyword", "value": "contract", "confidence": 75},
                {"type": "keyword", "value": "NDA", "confidence": 80},
                {"type": "keyword", "value": "terms and conditions", "confidence": 75},
                {"type": "keyword", "value": "service level agreement", "confidence": 80},
            ],
            "priority": 4,
            "keywords": [
                "contract retention", "3 year", "agreement", "NDA", "vendor contract",
                "service contract", "licence agreement", "purchase order", "SLA",
                "limitation period", "contractual obligation",
            ],
        },
        {
            "id": "retain_permanent_corporate",
            "name": "Retain Permanently – Corporate Records",
            "behavior": "retain_only",
            "retention_period_years": None,
            "retention_trigger": None,
            "event_based": False,
            "description": (
                "Permanently retains foundational corporate records that must be preserved for "
                "the life of the organisation and potentially beyond. Includes articles of "
                "incorporation, memoranda of association, board resolutions, shareholder meeting "
                "minutes, share registers, corporate seals, regulatory licences, and founding "
                "documents. These records establish the legal existence and governance history "
                "of the organisation."
            ),
            "applies_to": ["SharePoint", "OneDrive"],
            "regulatory_basis": ["Companies Act 2006", "Delaware General Corporation Law", "Corporations Act 2001"],
            "record_type": "regulatory_record",
            "immutable": True,
            "disposition_review": False,
            "auto_apply_conditions": [
                {"type": "keyword", "value": "articles of incorporation", "confidence": 90},
                {"type": "keyword", "value": "board resolution", "confidence": 80},
                {"type": "keyword", "value": "memorandum of association", "confidence": 90},
                {"type": "keyword", "value": "shareholder minutes", "confidence": 85},
            ],
            "priority": 10,
            "keywords": [
                "permanent retention", "corporate records", "articles of incorporation",
                "board minutes", "shareholder records", "founding documents",
                "memorandum of association", "share register", "regulatory licence",
                "indefinite retention", "corporate governance", "legal entity",
            ],
        },

        # ── DELETE ONLY ───────────────────────────────────────────────────────
        {
            "id": "delete_after_1yr_temp",
            "name": "Delete After 1 Year – Temporary Files",
            "behavior": "delete_only",
            "retention_period_years": 1,
            "retention_trigger": "creation_date",
            "event_based": False,
            "description": (
                "Automatically deletes temporary working files, draft documents, and transient "
                "data 1 year after creation. Targets working copies, temporary exports, scratch "
                "files, meeting notes with no archival value, and intermediate processing outputs. "
                "Helps manage storage consumption and reduces data subject to breach risk. "
                "Does not prevent earlier user-initiated deletion."
            ),
            "applies_to": ["SharePoint", "OneDrive", "Teams"],
            "regulatory_basis": ["GDPR Article 5(1)(e) – Storage Limitation"],
            "record_type": None,
            "immutable": False,
            "disposition_review": False,
            "auto_apply_conditions": [
                {"type": "keyword", "value": "draft", "confidence": 65},
                {"type": "keyword", "value": "temporary", "confidence": 70},
                {"type": "keyword", "value": "working copy", "confidence": 75},
                {"type": "keyword", "value": "scratch", "confidence": 70},
            ],
            "priority": 2,
            "keywords": [
                "delete only", "auto delete", "temporary files", "draft deletion",
                "1 year delete", "storage management", "transient data",
                "working copy", "scratch file", "intermediate file", "purge",
            ],
        },
        {
            "id": "delete_after_30days_personal",
            "name": "Delete After 30 Days – Personal Data Minimisation",
            "behavior": "delete_only",
            "retention_period_years": None,
            "retention_period_days": 30,
            "retention_trigger": "creation_date",
            "event_based": False,
            "description": (
                "Enforces data minimisation principle under GDPR by automatically deleting "
                "personal data-containing files 30 days after creation where there is no "
                "legitimate ongoing processing purpose. Applies to one-off data exports, "
                "ad-hoc personal data queries, recruitment screening outputs, and temporary "
                "customer data files created for single-use purposes."
            ),
            "applies_to": ["SharePoint", "OneDrive", "Exchange"],
            "regulatory_basis": ["GDPR Article 5(1)(c) – Data Minimisation", "GDPR Article 5(1)(e) – Storage Limitation"],
            "record_type": None,
            "immutable": False,
            "disposition_review": False,
            "auto_apply_conditions": [
                {"type": "sensitive_info_type", "value": "Person's Name", "confidence": 80},
                {"type": "keyword", "value": "data export", "confidence": 75},
                {"type": "keyword", "value": "ad-hoc report", "confidence": 70},
            ],
            "priority": 3,
            "keywords": [
                "30 day delete", "data minimisation", "GDPR delete", "personal data",
                "storage limitation", "short-term retention", "temporary personal data",
                "data export deletion", "one-time use", "ad-hoc data",
            ],
        },

        # ── RETAIN THEN DELETE ────────────────────────────────────────────────
        {
            "id": "retain_7yr_delete_financial",
            "name": "Retain 7 Years then Delete – Financial Records",
            "behavior": "retain_then_delete",
            "retention_period_years": 7,
            "retention_trigger": "creation_date",
            "event_based": False,
            "description": (
                "Retains financial records for exactly 7 years from creation date and then "
                "automatically deletes them unless a disposition review overrides the deletion. "
                "Balances regulatory retention requirements with data minimisation obligations. "
                "Applies to routine financial transactions, expense claims, supplier invoices, "
                "standard purchase orders, and routine accounting entries that have no ongoing "
                "evidentiary or strategic value after the retention period."
            ),
            "applies_to": ["SharePoint", "OneDrive", "Exchange"],
            "regulatory_basis": ["SOX", "Companies Act 2006", "GDPR Article 5(1)(e)"],
            "record_type": None,
            "immutable": False,
            "disposition_review": True,
            "disposition_reviewers": ["Finance Records Manager", "Compliance Officer"],
            "auto_apply_conditions": [
                {"type": "keyword", "value": "invoice", "confidence": 80},
                {"type": "keyword", "value": "expense claim", "confidence": 80},
                {"type": "keyword", "value": "purchase order", "confidence": 80},
                {"type": "sensitive_info_type", "value": "Financial Account Number", "confidence": 75},
            ],
            "priority": 6,
            "keywords": [
                "7 year retain then delete", "financial retention", "auto delete financial",
                "SOX retention", "accounting records", "financial compliance",
                "invoice disposal", "financial record lifecycle", "retain delete",
            ],
        },
        {
            "id": "retain_6yr_delete_gdpr",
            "name": "Retain 6 Years then Delete – GDPR Personal Data",
            "behavior": "retain_then_delete",
            "retention_period_years": 6,
            "retention_trigger": "creation_date",
            "event_based": False,
            "description": (
                "Retains personal data subject to a 6-year limitation period for contractual "
                "claims, then automatically deletes in compliance with GDPR storage limitation "
                "principle. Covers customer contracts, employee records post-employment, client "
                "correspondence, and service delivery records. Triggers disposition review before "
                "deletion to allow legal hold exceptions and ensures documented destruction."
            ),
            "applies_to": ["SharePoint", "OneDrive", "Exchange", "Teams"],
            "regulatory_basis": ["GDPR Article 5(1)(e)", "Limitation Act 1980", "UK GDPR"],
            "record_type": None,
            "immutable": False,
            "disposition_review": True,
            "disposition_reviewers": ["Data Protection Officer", "Records Manager"],
            "auto_apply_conditions": [
                {"type": "sensitive_info_type", "value": "Person's Name", "confidence": 80},
                {"type": "sensitive_info_type", "value": "EU Social Security Number", "confidence": 85},
                {"type": "keyword", "value": "customer record", "confidence": 75},
                {"type": "keyword", "value": "employee record", "confidence": 75},
            ],
            "priority": 7,
            "keywords": [
                "GDPR retention", "6 year", "personal data lifecycle", "UK GDPR",
                "data subject", "customer records", "employee records", "limitation period",
                "storage limitation", "data deletion", "personal data disposal",
                "DPO", "data protection", "right to erasure",
            ],
        },
        {
            "id": "retain_event_employment_end",
            "name": "Retain 7 Years – Employee Records (Event-Based)",
            "behavior": "retain_then_delete",
            "retention_period_years": 7,
            "retention_trigger": "event",
            "event_based": True,
            "event_type": "Employee Termination",
            "description": (
                "Event-based retention label triggered when an employee leaves the organisation. "
                "Retains all HR records, performance reviews, disciplinary records, payroll data, "
                "training records, and employment contracts for 7 years after the employment end "
                "event. The retention clock starts only when the 'Employee Termination' event is "
                "recorded in the HR system, not from document creation date. Ensures compliance "
                "with employment law record-keeping requirements across multiple jurisdictions."
            ),
            "applies_to": ["SharePoint", "OneDrive", "Exchange"],
            "regulatory_basis": ["Employment Rights Act 1996", "FLSA", "GDPR", "UK GDPR"],
            "record_type": None,
            "immutable": False,
            "disposition_review": True,
            "disposition_reviewers": ["HR Records Manager", "Legal Counsel"],
            "auto_apply_conditions": [
                {"type": "keyword", "value": "employment contract", "confidence": 80},
                {"type": "keyword", "value": "performance review", "confidence": 75},
                {"type": "keyword", "value": "disciplinary", "confidence": 75},
                {"type": "keyword", "value": "payroll", "confidence": 75},
                {"type": "keyword", "value": "HR record", "confidence": 80},
            ],
            "priority": 8,
            "keywords": [
                "employee records", "HR retention", "event-based", "employment termination",
                "personnel file", "performance review", "disciplinary records",
                "payroll retention", "7 year HR", "post-employment", "employment law",
                "workforce records", "training records",
            ],
        },
        {
            "id": "retain_event_contract_expiry",
            "name": "Retain 6 Years – Contracts (Event-Based: Contract End)",
            "behavior": "retain_then_delete",
            "retention_period_years": 6,
            "retention_trigger": "event",
            "event_based": True,
            "event_type": "Contract Expiry",
            "description": (
                "Event-based retention triggered at contract end date. Retains all contract "
                "documents, amendments, statements of work, correspondence related to the "
                "contract, and delivery documentation for 6 years after the contract expiry "
                "or termination event. The retention period begins when the 'Contract Expiry' "
                "event is registered, providing accurate limitation period coverage for "
                "contractual disputes regardless of when documents were created."
            ),
            "applies_to": ["SharePoint", "OneDrive", "Exchange"],
            "regulatory_basis": ["Limitation Act 1980", "UCC", "GDPR Article 5(1)(e)"],
            "record_type": None,
            "immutable": False,
            "disposition_review": True,
            "disposition_reviewers": ["Contracts Manager", "Legal Team"],
            "auto_apply_conditions": [
                {"type": "keyword", "value": "statement of work", "confidence": 80},
                {"type": "keyword", "value": "contract amendment", "confidence": 80},
                {"type": "keyword", "value": "master services agreement", "confidence": 85},
                {"type": "keyword", "value": "MSA", "confidence": 75},
            ],
            "priority": 7,
            "keywords": [
                "contract retention", "event-based contract", "contract expiry",
                "6 year contract", "SOW retention", "MSA", "limitation period",
                "contract lifecycle", "post-contract", "contract disposal",
            ],
        },
        {
            "id": "retain_event_product_discontinue",
            "name": "Retain 10 Years – Product Records (Event-Based: Product End-of-Life)",
            "behavior": "retain_then_delete",
            "retention_period_years": 10,
            "retention_trigger": "event",
            "event_based": True,
            "event_type": "Product End-of-Life",
            "description": (
                "Event-based retention for product documentation, triggered when a product is "
                "officially discontinued. Retains product specifications, design documents, "
                "test records, safety assessments, regulatory submissions, manufacturing records, "
                "and field complaint data for 10 years after product end-of-life. Essential for "
                "product liability defence, regulatory audits, and post-market surveillance "
                "requirements in regulated industries."
            ),
            "applies_to": ["SharePoint", "OneDrive"],
            "regulatory_basis": ["ISO 9001", "FDA 21 CFR Part 820", "EU MDR 2017/745", "Product Liability Directive"],
            "record_type": "regulatory_record",
            "immutable": True,
            "disposition_review": True,
            "disposition_reviewers": ["Quality Manager", "Regulatory Affairs", "Legal Counsel"],
            "auto_apply_conditions": [
                {"type": "keyword", "value": "product specification", "confidence": 75},
                {"type": "keyword", "value": "design document", "confidence": 70},
                {"type": "keyword", "value": "safety assessment", "confidence": 80},
                {"type": "keyword", "value": "regulatory submission", "confidence": 85},
            ],
            "priority": 9,
            "keywords": [
                "product records", "end-of-life", "product lifecycle", "10 year retention",
                "product liability", "regulatory submission", "design records",
                "safety records", "manufacturing records", "field complaints",
                "post-market surveillance", "ISO 9001", "FDA records", "MDR",
            ],
        },

        # ── REGULATORY RECORDS ────────────────────────────────────────────────
        {
            "id": "regulatory_record_clinical",
            "name": "Regulatory Record – Clinical Trial Data (Permanent)",
            "behavior": "retain_only",
            "retention_period_years": None,
            "retention_trigger": "creation_date",
            "event_based": False,
            "description": (
                "Marks clinical trial data as a regulatory record with permanent, immutable "
                "retention. Once labelled, content cannot be edited or deleted except by "
                "authorised records managers with explicit regulatory justification. Applies to "
                "clinical study reports, case report forms, informed consent records, adverse "
                "event data, protocol amendments, and investigator brochures. Required under "
                "ICH E6 GCP guidelines and FDA 21 CFR Part 312."
            ),
            "applies_to": ["SharePoint", "OneDrive"],
            "regulatory_basis": ["ICH E6 GCP", "FDA 21 CFR Part 312", "EU Clinical Trials Regulation"],
            "record_type": "regulatory_record",
            "immutable": True,
            "disposition_review": False,
            "auto_apply_conditions": [
                {"type": "keyword", "value": "clinical trial", "confidence": 90},
                {"type": "keyword", "value": "case report form", "confidence": 90},
                {"type": "keyword", "value": "informed consent", "confidence": 85},
                {"type": "keyword", "value": "adverse event", "confidence": 85},
                {"type": "keyword", "value": "investigator brochure", "confidence": 90},
            ],
            "priority": 10,
            "keywords": [
                "clinical trial", "regulatory record", "GCP", "clinical data",
                "case report form", "CRF", "informed consent", "adverse event",
                "investigator brochure", "FDA 21 CFR", "ICH", "immutable record",
                "clinical study report", "protocol", "trial master file",
            ],
        },
    ]


def get_retention_policies() -> List[Dict[str, Any]]:
    """Return retention policies with static and adaptive scope configurations."""
    return [
        {
            "id": "org_wide_email_retention",
            "name": "Organisation-Wide Email Retention – 3 Years",
            "scope_type": "static",
            "description": (
                "Organisation-wide retention policy applied to all Exchange mailboxes, "
                "Microsoft Teams channel messages, and Teams chats. Retains all email and "
                "Teams messaging content for a minimum of 3 years to satisfy e-discovery "
                "requirements and baseline business communication record-keeping obligations. "
                "After 3 years, content is eligible for deletion unless a more specific "
                "retention label or legal hold overrides this policy."
            ),
            "locations": [
                {"service": "Exchange", "scope": "All mailboxes", "inclusion": "all"},
                {"service": "Teams Channel Messages", "scope": "All teams", "inclusion": "all"},
                {"service": "Teams Chats", "scope": "All users", "inclusion": "all"},
            ],
            "retention_period_years": 3,
            "retention_action": "retain_then_delete",
            "retention_trigger": "creation_date",
            "policy_basis": "baseline_compliance",
            "regulatory_basis": ["FRCP", "MiFID II", "GDPR Article 5"],
            "priority": 3,
            "overridden_by_labels": True,
            "keywords": [
                "email retention", "Teams retention", "3 year", "communication records",
                "e-discovery", "messaging retention", "Exchange policy", "baseline retention",
                "organisation-wide", "all mailboxes",
            ],
        },
        {
            "id": "sharepoint_onedrive_retention",
            "name": "SharePoint and OneDrive Retention – 5 Years",
            "scope_type": "static",
            "description": (
                "Retains all content in SharePoint sites and OneDrive for Business accounts "
                "for 5 years. Ensures that business documents, collaboration content, and "
                "project files are preserved for e-discovery and audit purposes. Specific "
                "retention labels applied to content take precedence over this policy. "
                "After 5 years, unlabelled content is automatically deleted."
            ),
            "locations": [
                {"service": "SharePoint", "scope": "All sites", "inclusion": "all"},
                {"service": "OneDrive", "scope": "All accounts", "inclusion": "all"},
            ],
            "retention_period_years": 5,
            "retention_action": "retain_then_delete",
            "retention_trigger": "modification_date",
            "policy_basis": "baseline_compliance",
            "regulatory_basis": ["GDPR", "SOX", "ISO 27001"],
            "priority": 3,
            "overridden_by_labels": True,
            "keywords": [
                "SharePoint retention", "OneDrive retention", "5 year", "document retention",
                "file retention", "collaboration content", "project files", "site retention",
                "business documents", "content lifecycle",
            ],
        },
        {
            "id": "financial_records_policy",
            "name": "Finance Department – Statutory Financial Records Retention",
            "scope_type": "static",
            "description": (
                "Targeted retention policy for Finance department SharePoint sites, OneDrive "
                "accounts of Finance staff, and Finance distribution group mailboxes. Enforces "
                "7-year retention for all financial content in these locations as required by "
                "statutory accounting, tax, and securities regulations. Overrides the default "
                "organisation-wide policies for Finance locations."
            ),
            "locations": [
                {"service": "SharePoint", "scope": "Finance department sites", "inclusion": "specific", "sites": ["Finance-Hub", "Accounting", "Treasury", "FP&A", "TaxAndAudit"]},
                {"service": "OneDrive", "scope": "Finance staff", "inclusion": "specific_group", "group": "Finance Department"},
                {"service": "Exchange", "scope": "Finance mailboxes", "inclusion": "specific_group", "group": "Finance Department"},
            ],
            "retention_period_years": 7,
            "retention_action": "retain_then_delete",
            "retention_trigger": "creation_date",
            "policy_basis": "regulatory_requirement",
            "regulatory_basis": ["SOX", "Companies Act 2006", "IRS", "HMRC", "MiFID II"],
            "priority": 7,
            "overridden_by_labels": True,
            "keywords": [
                "finance retention", "financial records", "7 year", "SOX", "statutory",
                "accounting records", "tax records", "Finance department",
                "regulatory financial", "HMRC", "Companies Act",
            ],
        },
        {
            "id": "hr_records_policy",
            "name": "HR Department – Employee Records Retention",
            "scope_type": "static",
            "description": (
                "Retention policy covering HR department SharePoint sites and HR staff OneDrive "
                "accounts. Retains all HR content for 7 years to comply with employment law "
                "record-keeping requirements. Covers recruitment records, onboarding documentation, "
                "performance management, training records, disciplinary files, and payroll data. "
                "Event-based retention labels applied to individual employee folders take precedence."
            ),
            "locations": [
                {"service": "SharePoint", "scope": "HR department sites", "inclusion": "specific", "sites": ["HR-Hub", "Recruitment", "Payroll", "LearningAndDevelopment"]},
                {"service": "OneDrive", "scope": "HR staff", "inclusion": "specific_group", "group": "HR Department"},
                {"service": "Exchange", "scope": "HR mailboxes", "inclusion": "specific_group", "group": "HR Department"},
            ],
            "retention_period_years": 7,
            "retention_action": "retain_then_delete",
            "retention_trigger": "modification_date",
            "policy_basis": "regulatory_requirement",
            "regulatory_basis": ["Employment Rights Act 1996", "FLSA", "GDPR", "EEOC"],
            "priority": 7,
            "overridden_by_labels": True,
            "keywords": [
                "HR retention", "employee records", "7 year HR", "employment law",
                "personnel records", "recruitment records", "payroll retention",
                "training records", "disciplinary records", "onboarding",
            ],
        },
        {
            "id": "adaptive_scope_high_value_projects",
            "name": "High-Value Projects – Adaptive Scope Retention",
            "scope_type": "adaptive",
            "description": (
                "Adaptive-scope retention policy that dynamically targets SharePoint sites "
                "classified as 'High Value Project' sites and OneDrive accounts of users with "
                "the 'Project Lead' or 'Senior Manager' role attribute. The scope automatically "
                "expands and contracts as sites gain or lose the classification and as users "
                "change roles. Retains all project content for 10 years to support long-term "
                "project audits, IP protection, and warranty claims."
            ),
            "locations": [
                {"service": "SharePoint", "scope": "Adaptive – sites with classification=HighValueProject"},
                {"service": "OneDrive", "scope": "Adaptive – users with jobTitle contains 'Project Lead' OR 'Senior Manager'"},
            ],
            "adaptive_scope_query": {
                "sharepoint": "SiteTemplate eq 'TEAMCHANNEL#1' AND SiteClassification eq 'HighValueProject'",
                "onedrive": "JobTitle -like '*Project Lead*' -or JobTitle -like '*Senior Manager*'",
            },
            "retention_period_years": 10,
            "retention_action": "retain_then_delete",
            "retention_trigger": "creation_date",
            "policy_basis": "business_requirement",
            "regulatory_basis": ["ISO 9001", "IP Protection", "GDPR"],
            "priority": 6,
            "overridden_by_labels": True,
            "keywords": [
                "adaptive scope", "dynamic retention", "high value project", "project retention",
                "10 year", "adaptive policy", "role-based retention", "site classification",
                "IP protection", "project audit", "senior manager", "project lead",
            ],
        },
        {
            "id": "adaptive_scope_regulated_users",
            "name": "Regulated Users – Adaptive Scope Compliance Retention",
            "scope_type": "adaptive",
            "description": (
                "Adaptive retention policy targeting users in regulated roles such as financial "
                "advisers, brokers, compliance officers, and healthcare professionals. The scope "
                "dynamically includes Exchange mailboxes and Teams messages of users whose "
                "department attribute matches regulated categories. Enforces 7-year retention "
                "of all communications to meet MiFID II, FINRA, FCA, and equivalent regulatory "
                "communication retention requirements."
            ),
            "locations": [
                {"service": "Exchange", "scope": "Adaptive – regulated role users"},
                {"service": "Teams Channel Messages", "scope": "Adaptive – regulated role users"},
                {"service": "Teams Chats", "scope": "Adaptive – regulated role users"},
            ],
            "adaptive_scope_query": {
                "users": "Department -in ('Financial Advisory','Compliance','Investment Banking','Healthcare','Brokerage')",
            },
            "retention_period_years": 7,
            "retention_action": "retain_only",
            "retention_trigger": "creation_date",
            "policy_basis": "regulatory_requirement",
            "regulatory_basis": ["MiFID II", "FINRA Rule 4511", "FCA COBS 11.8", "HIPAA"],
            "priority": 8,
            "overridden_by_labels": True,
            "keywords": [
                "adaptive scope", "regulated users", "MiFID II", "FINRA", "FCA",
                "financial adviser", "broker", "compliance officer", "7 year communications",
                "regulated communications", "broker-dealer", "investment banking",
                "healthcare communications", "HIPAA retention",
            ],
        },
        {
            "id": "teams_meetings_recordings",
            "name": "Teams Meetings and Recordings – 1 Year Retention",
            "scope_type": "static",
            "description": (
                "Retains Microsoft Teams meeting recordings, transcripts, and voicemail messages "
                "for 1 year. Balances the value of recorded meetings for reference purposes "
                "against storage costs and privacy obligations under GDPR. After 1 year, "
                "recordings are automatically deleted unless a specific retention label has been "
                "manually applied or a legal hold is in place. Users are notified 30 days before "
                "automatic deletion."
            ),
            "locations": [
                {"service": "Teams Meetings", "scope": "All meeting recordings", "inclusion": "all"},
                {"service": "OneDrive", "scope": "Meeting recordings folder", "inclusion": "all"},
                {"service": "SharePoint", "scope": "Teams channel meeting recordings", "inclusion": "all"},
            ],
            "retention_period_years": 1,
            "retention_action": "retain_then_delete",
            "retention_trigger": "creation_date",
            "policy_basis": "business_requirement",
            "regulatory_basis": ["GDPR Article 5(1)(e)"],
            "priority": 4,
            "overridden_by_labels": True,
            "keywords": [
                "Teams recordings", "meeting recordings", "1 year", "video retention",
                "transcript retention", "voicemail retention", "Teams meetings",
                "recording lifecycle", "meeting transcript", "auto delete recordings",
            ],
        },
    ]


def get_records_management_config() -> Dict[str, Any]:
    """Return records management configuration settings."""
    return {
        "id": "records_management_config",
        "name": "Records Management Configuration",
        "description": (
            "Comprehensive records management configuration for Microsoft Purview. Defines "
            "record types, declassification workflows, file plan structure, and records "
            "declaration settings. Supports both manual and automatic record declaration, "
            "regulatory records with immutability, and integration with SharePoint document "
            "libraries through file plan taxonomy."
        ),
        "record_declaration": {
            "description": (
                "Controls how items are declared as records. Items declared as records cannot "
                "be edited or deleted by users. Only records managers with explicit permissions "
                "can unlock records for editing. Regulatory records offer even stronger "
                "protections, preventing deletion even by global administrators."
            ),
            "allow_manual_declaration": True,
            "allow_auto_declaration_via_labels": True,
            "record_types": [
                {
                    "type": "record",
                    "description": "Standard record – locked from editing/deletion by regular users; records managers can unlock.",
                    "editable_by": ["Records Manager", "Compliance Administrator"],
                    "deletable_by": ["Records Manager", "Compliance Administrator"],
                },
                {
                    "type": "regulatory_record",
                    "description": "Regulatory record – immutable; cannot be edited or deleted by anyone including global admins during retention period.",
                    "editable_by": [],
                    "deletable_by": [],
                    "requires_privileged_role": True,
                },
            ],
            "keywords": [
                "record declaration", "immutable", "locked record", "regulatory record",
                "records manager", "record type", "declare record", "lock content",
            ],
        },
        "file_plan": {
            "description": (
                "File plan provides a hierarchical taxonomy for organising retention labels "
                "within the context of the organisation's business functions, record categories, "
                "and regulatory requirements. Each file plan entry maps a retention label to "
                "a business function, record category, and regulatory citation."
            ),
            "enabled": True,
            "descriptors": [
                "Business Function",
                "Category",
                "Sub-category",
                "Authority Type",
                "Provision/Citation",
                "Jurisdiction",
            ],
            "example_entries": [
                {
                    "label": "retain_7yr_financial",
                    "business_function": "Finance and Accounting",
                    "category": "Financial Records",
                    "sub_category": "Accounts and Ledgers",
                    "authority_type": "Regulatory",
                    "citation": "Companies Act 2006, s.386",
                    "jurisdiction": "United Kingdom",
                },
                {
                    "label": "retain_event_employment_end",
                    "business_function": "Human Resources",
                    "category": "Employee Records",
                    "sub_category": "Personnel Files",
                    "authority_type": "Regulatory",
                    "citation": "Employment Rights Act 1996",
                    "jurisdiction": "United Kingdom",
                },
            ],
            "keywords": [
                "file plan", "retention taxonomy", "record category", "business function",
                "regulatory citation", "file plan descriptor", "retention schedule",
                "record classification", "jurisdiction",
            ],
        },
        "disposition": {
            "description": (
                "Disposition management controls what happens to content at the end of its "
                "retention period. Content can be automatically deleted, sent for disposition "
                "review, relabelled to a new retention label, or permanently marked as a record. "
                "Disposition proof records are maintained for regulatory audit purposes."
            ),
            "auto_disposition_enabled": True,
            "disposition_proof_enabled": True,
            "proof_storage_years": 7,
            "multi_stage_review_enabled": True,
            "max_review_stages": 5,
            "reviewer_notification_days_before": 30,
            "reminder_days": [30, 14, 7, 1],
            "actions_available": [
                "Permanently delete",
                "Apply new label (relabel)",
                "Extend retention period",
                "Declare as record",
                "Export disposition report",
            ],
            "keywords": [
                "disposition", "disposition review", "end of retention", "delete at end",
                "disposition proof", "audit of destruction", "multi-stage review",
                "relabel", "extend retention", "records disposal",
            ],
        },
        "import_export": {
            "description": "Supports bulk import of retention labels via CSV and export of file plan to Excel.",
            "csv_import_enabled": True,
            "excel_export_enabled": True,
            "supported_formats": ["CSV", "XLSX"],
            "keywords": [
                "import labels", "export file plan", "bulk import", "CSV retention",
                "migration", "label import", "file plan export",
            ],
        },
        "keywords": [
            "records management", "file plan", "record declaration", "regulatory record",
            "immutable record", "disposition", "retention label", "records taxonomy",
            "compliance records", "information governance", "records lifecycle",
        ],
    }


def get_disposition_workflows() -> List[Dict[str, Any]]:
    """Return disposition review workflow configurations."""
    return [
        {
            "id": "single_stage_finance_disposition",
            "name": "Single-Stage Finance Records Disposition Review",
            "stages": 1,
            "description": (
                "Single-stage disposition review workflow for routine financial records reaching "
                "end of their 7-year retention period. The Finance Records Manager reviews items "
                "flagged for disposal and either approves deletion or extends the retention period "
                "with documented justification. All disposition decisions are captured in the "
                "disposition proof report for audit purposes."
            ),
            "applies_to_labels": [
                "retain_7yr_delete_financial",
                "retain_7yr_financial",
            ],
            "stage_1": {
                "reviewers": ["Finance Records Manager", "Finance Compliance Officer"],
                "review_period_days": 30,
                "actions": ["Approve deletion", "Extend retention", "Relabel"],
                "notification_template": "FinanceDispositionReview",
                "escalation_after_days": 25,
                "escalation_to": "Chief Financial Officer",
            },
            "disposition_proof": True,
            "proof_retention_years": 7,
            "keywords": [
                "single stage", "finance disposition", "financial records disposal",
                "7 year financial", "records manager review", "deletion approval",
                "disposition proof", "audit of destruction",
            ],
        },
        {
            "id": "multi_stage_legal_disposition",
            "name": "Multi-Stage Legal Records Disposition Review",
            "stages": 3,
            "description": (
                "Three-stage disposition review for legal records and contracts. Stage 1 involves "
                "the Legal Records team screening for ongoing litigation holds and active matters. "
                "Stage 2 involves the General Counsel or deputy confirming no privilege or ongoing "
                "legal requirement exists. Stage 3 involves the Compliance Officer providing final "
                "sign-off and confirming regulatory obligations are satisfied. Ensures thorough "
                "review of potentially sensitive legal materials before destruction."
            ),
            "applies_to_labels": [
                "retain_event_contract_expiry",
                "confidential_legal",
            ],
            "stage_1": {
                "name": "Legal Records Screening",
                "reviewers": ["Legal Records Manager", "Paralegal Team"],
                "review_period_days": 20,
                "actions": ["Pass to Stage 2", "Place on Legal Hold", "Extend retention"],
                "notification_template": "LegalDispositionStage1",
                "escalation_after_days": 15,
                "escalation_to": "General Counsel",
            },
            "stage_2": {
                "name": "General Counsel Review",
                "reviewers": ["General Counsel", "Deputy General Counsel"],
                "review_period_days": 15,
                "actions": ["Approve for Stage 3", "Place on Legal Hold", "Relabel as Permanent"],
                "notification_template": "LegalDispositionStage2",
                "escalation_after_days": 12,
                "escalation_to": "Chief Legal Officer",
            },
            "stage_3": {
                "name": "Compliance Final Sign-Off",
                "reviewers": ["Chief Compliance Officer", "Compliance Officer"],
                "review_period_days": 10,
                "actions": ["Approve deletion", "Escalate to Board", "Relabel"],
                "notification_template": "LegalDispositionStage3",
                "escalation_after_days": 8,
                "escalation_to": "General Counsel",
            },
            "disposition_proof": True,
            "proof_retention_years": 10,
            "keywords": [
                "multi-stage", "legal disposition", "3 stage review", "legal records",
                "contract disposal", "General Counsel", "compliance sign-off",
                "legal hold check", "privilege review", "legal records manager",
            ],
        },
        {
            "id": "two_stage_hr_disposition",
            "name": "Two-Stage HR Employee Records Disposition Review",
            "stages": 2,
            "description": (
                "Two-stage disposition workflow for employee records at end of the post-employment "
                "retention period. Stage 1 involves the HR Records team verifying no active "
                "employment tribunal proceedings, EEOC complaints, or ongoing compensation claims "
                "reference the employee. Stage 2 involves the Data Protection Officer confirming "
                "GDPR data subject rights have been satisfied and deletion is compliant. "
                "Generates documented destruction certificate for each employee's records."
            ),
            "applies_to_labels": [
                "retain_event_employment_end",
                "retain_6yr_delete_gdpr",
            ],
            "stage_1": {
                "name": "HR Records Verification",
                "reviewers": ["HR Records Manager", "HR Business Partner"],
                "review_period_days": 21,
                "actions": ["Clear for DPO review", "Place on hold – active claim", "Extend retention"],
                "notification_template": "HRDispositionStage1",
                "escalation_after_days": 18,
                "escalation_to": "HR Director",
            },
            "stage_2": {
                "name": "DPO GDPR Compliance Review",
                "reviewers": ["Data Protection Officer", "Deputy DPO"],
                "review_period_days": 14,
                "actions": ["Approve deletion", "Issue erasure confirmation", "Extend retention with GDPR justification"],
                "notification_template": "HRDispositionStage2",
                "escalation_after_days": 10,
                "escalation_to": "Chief Privacy Officer",
            },
            "disposition_proof": True,
            "proof_retention_years": 7,
            "destruction_certificate": True,
            "keywords": [
                "HR disposition", "employee records disposal", "two stage", "DPO review",
                "GDPR deletion", "data subject rights", "employment records",
                "destruction certificate", "HR records manager", "post-employment",
                "GDPR compliant deletion",
            ],
        },
        {
            "id": "product_records_disposition",
            "name": "Regulated Product Records Disposition Review",
            "stages": 2,
            "description": (
                "Disposition review workflow for product records at end-of-life following the "
                "10-year post-discontinuation retention period. Stage 1 involves the Quality "
                "and Regulatory Affairs team confirming no outstanding product liability claims, "
                "regulatory investigations, or post-market surveillance obligations. Stage 2 "
                "involves the Chief Quality Officer providing final approval with documented "
                "regulatory justification. Generates a regulatory-grade destruction record."
            ),
            "applies_to_labels": [
                "retain_event_product_discontinue",
                "regulatory_record_clinical",
            ],
            "stage_1": {
                "name": "Quality and Regulatory Screening",
                "reviewers": ["Quality Records Manager", "Regulatory Affairs Manager"],
                "review_period_days": 30,
                "actions": ["Clear for CQO review", "Hold – active investigation", "Extend – regulatory obligation"],
                "notification_template": "ProductDispositionStage1",
                "escalation_after_days": 25,
                "escalation_to": "VP Quality",
            },
            "stage_2": {
                "name": "Chief Quality Officer Approval",
                "reviewers": ["Chief Quality Officer"],
                "review_period_days": 14,
                "actions": ["Approve deletion with regulatory certificate", "Extend", "Escalate to Legal"],
                "notification_template": "ProductDispositionStage2",
                "escalation_after_days": 10,
                "escalation_to": "General Counsel",
            },
            "disposition_proof": True,
            "proof_retention_years": 10,
            "destruction_certificate": True,
            "regulatory_grade_record": True,
            "keywords": [
                "product records disposition", "regulatory disposal", "10 year product",
                "quality records", "CQO approval", "regulatory certificate",
                "product liability", "post-market surveillance", "FDA records",
                "medical device records", "regulated records disposal",
            ],
        },
    ]

"""DLP policy templates knowledge base for Microsoft Purview Policy Simulator."""
from typing import List

from app.models.policy import PolicyTemplate


def get_dlp_templates() -> List[PolicyTemplate]:
    """Return a comprehensive list of DLP policy templates."""
    return [
        # ── FINANCIAL (8 templates) ──────────────────────────────────────────
        PolicyTemplate(
            id="pci_dss_cardholder_data",
            name="PCI DSS – Cardholder Data Protection",
            category="Financial",
            description=(
                "Detects and protects payment card industry data including credit card numbers, "
                "CVV codes, expiry dates, and cardholder names to ensure PCI DSS compliance."
            ),
            keywords=[
                "credit card", "payment card", "PCI DSS", "cardholder data", "payment data",
                "financial data", "card number", "CVV", "expiry", "debit card",
                "Visa", "Mastercard", "American Express", "card verification", "PAN",
                "primary account number", "magnetic stripe", "chip and pin", "contactless payment",
                "merchant data",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=[
                "Credit Card Number", "Credit Card Expiration Date",
                "Credit Card Security Code", "Debit Card Number",
            ],
            actions=[
                "Block sharing outside organisation",
                "Notify user with policy tip",
                "Alert compliance administrator",
                "Encrypt document at rest",
            ],
            compliance_frameworks=["PCI-DSS"],
            severity="high",
            tags=["payment", "credit-card", "PCI", "financial", "cardholder"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference#pci-data-security-standard-pci-dss',
            specific_blocked_actions=[
                'Block email containing credit card numbers to external recipients in Exchange Online',
                'Block upload of files containing cardholder data to SharePoint and OneDrive',
                'Block copy of payment card data to USB devices on managed endpoints',
            ],
            specific_audit_actions=[
                'Log all detected cardholder data (PAN, CVV, expiry) in the DLP activity explorer',
                'Record user, timestamp, and file details for PCI-DSS audit evidence',
            ],
            specific_notifications=[
                'Notify the PCI compliance officer when cardholder data is detected outside approved systems',
                'Alert the security operations centre for every cardholder data policy match',
            ],
            specific_user_experience="Users attempting to send or share content containing credit card numbers receive a policy tip: 'This message contains payment card data protected under PCI-DSS. External sharing has been blocked.'",
            specific_admin_experience='Compliance administrators see PCI-DSS incidents in the DLP activity explorer with cardholder data context and matched SITs. Real-time alerts are sent; incidents are auto-escalated to the PCI compliance officer.',
            specific_policy_tips=[
                'This content contains payment card data (PAN/CVV) protected under PCI-DSS. External sharing has been blocked.',
                'To share this data with an authorised party, use the approved secure file transfer system.',
            ],
        ),
        PolicyTemplate(
            id="sox_financial_statements",
            name="SOX – Financial Statements and Controls",
            category="Financial",
            description=(
                "Protects financial statements, audit trails, and internal controls documentation "
                "required under the Sarbanes-Oxley Act (SOX) for publicly traded companies."
            ),
            keywords=[
                "SOX", "Sarbanes-Oxley", "financial statement", "balance sheet", "income statement",
                "cash flow", "audit trail", "internal controls", "material weakness",
                "quarterly report", "annual report", "10-K", "10-Q", "SEC filing",
                "PCAOB", "auditor report", "earnings release", "revenue recognition",
                "financial disclosure", "management assessment",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams"],
            sensitive_info_types=[
                "Financial Statement", "Audit Report", "SEC Filing",
            ],
            actions=[
                "Block external sharing",
                "Notify compliance officer",
                "Require justification for access",
                "Log all access attempts",
            ],
            compliance_frameworks=["SOX"],
            severity="high",
            tags=["SOX", "financial", "audit", "compliance", "SEC"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block external sharing of financial statements and earnings data in Exchange, SharePoint, and OneDrive',
                'Block forwarding of SOX-controlled documents to personal email addresses',
            ],
            specific_audit_actions=[
                'Log all access to financial statements and internal controls documentation',
                'Capture full audit trail required for SOX Section 302 and 404 compliance',
            ],
            specific_notifications=[
                'Notify the CFO and compliance officer when financial statements are shared externally',
                'Alert the legal team when SEC filing documents are detected in unapproved locations',
            ],
            specific_user_experience='Users attempting to share SOX-controlled financial documents externally are blocked and see a policy tip that the document is subject to SOX controls and must only be shared through approved investor relations channels.',
            specific_admin_experience='Compliance administrators see SOX incidents in the DLP activity explorer. Daily digest alerts are sent; high-severity incidents involving pre-announcement earnings data are escalated immediately.',
            specific_policy_tips=[
                'This document contains SOX-controlled financial data. External sharing is restricted to approved channels only.',
                'If you need to share this with auditors or investors, contact the Investor Relations team.',
            ],
        ),
        PolicyTemplate(
            id="glba_customer_financial_info",
            name="GLBA – Customer Financial Information",
            category="Financial",
            description=(
                "Protects non-public personal financial information of customers as required by "
                "the Gramm-Leach-Bliley Act (GLBA), covering financial institutions."
            ),
            keywords=[
                "GLBA", "Gramm-Leach-Bliley", "non-public personal information", "NPI",
                "customer financial", "account number", "loan information", "mortgage",
                "investment account", "insurance policy", "credit history", "financial profile",
                "banking information", "savings account", "checking account",
                "financial institution", "privacy notice", "opt-out", "safeguards rule",
                "pretexting protection",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=[
                "Bank Account Number", "Credit Card Number", "Financial Account Number",
            ],
            actions=[
                "Block external sharing",
                "Apply encryption",
                "Notify data protection officer",
                "Generate audit log",
            ],
            compliance_frameworks=["GLBA"],
            severity="high",
            tags=["GLBA", "financial", "banking", "NPI", "consumer"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block external sharing of customer non-public personal financial information (NPI)',
                'Block transmission of account numbers and financial profiles via unsecured email',
            ],
            specific_audit_actions=[
                'Log all detected NPI disclosures for GLBA Safeguards Rule compliance',
                'Record access events for customer financial records for annual GLBA audit',
            ],
            specific_notifications=[
                'Notify the Data Protection Officer when NPI is detected outside approved systems',
                'Alert the Chief Privacy Officer on GLBA policy violations',
            ],
            specific_user_experience="Users are blocked from sharing customer financial information externally. A policy tip states: 'This content contains customer financial information protected under GLBA. Please use the secure customer portal for sharing.'",
            specific_admin_experience='Compliance administrators see GLBA incidents with customer financial data details. Daily digest alerts are sent; incidents involving account numbers are escalated to the Data Protection Officer immediately.',
            specific_policy_tips=[
                'This content contains customer financial information protected under GLBA. External sharing is not permitted.',
                'Use the approved secure portal to share this information with authorised parties.',
            ],
        ),
        PolicyTemplate(
            id="credit_card_numbers",
            name="Credit Card Number Detection",
            category="Financial",
            description=(
                "Detects credit card numbers from major card networks including Visa, Mastercard, "
                "American Express, Discover, and others in documents and communications."
            ),
            keywords=[
                "credit card", "card number", "Visa", "Mastercard", "Amex", "American Express",
                "Discover", "Diners Club", "JCB", "UnionPay", "card details",
                "payment information", "card data", "PAN", "16-digit", "4-digit",
                "billing details", "card expiry", "CVV", "CVC",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices", "PowerBI"],
            sensitive_info_types=["Credit Card Number"],
            actions=[
                "Block send/share",
                "Apply sensitivity label",
                "Alert security operations",
            ],
            compliance_frameworks=["PCI-DSS", "GDPR"],
            severity="high",
            tags=["credit-card", "payment", "PCI", "financial"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block sending emails containing credit card numbers to external recipients',
                'Block uploading files with credit card numbers to unapproved cloud storage',
                'Block copying credit card data to USB removable storage on endpoints',
            ],
            specific_audit_actions=[
                'Log all credit card number detections with matched content evidence',
                'Record sender, recipients, and file name in the DLP audit log',
            ],
            specific_notifications=[
                'Notify the security team when credit card numbers are detected in email or documents',
                'Alert the compliance administrator for each credit card detection event',
            ],
            specific_user_experience="Users see a policy tip when credit card numbers are detected: 'This content may contain payment card data. Sharing externally has been blocked.'",
            specific_admin_experience='Security administrators receive real-time alerts for each credit card detection. Full incident details including matched content and user context are available in the DLP activity explorer.',
            specific_policy_tips=[
                'This content contains credit card numbers. External sharing has been blocked to protect payment data.',
                'If you need to send payment information, use the approved payment processing system.',
            ],
        ),
        PolicyTemplate(
            id="bank_account_numbers",
            name="Bank Account Number Protection",
            category="Financial",
            description=(
                "Identifies and protects bank account numbers, routing numbers, and IBAN numbers "
                "to prevent financial fraud and unauthorised transfers."
            ),
            keywords=[
                "bank account", "account number", "routing number", "IBAN", "SWIFT",
                "sort code", "BSB number", "direct deposit", "wire transfer", "ACH",
                "bank details", "account holder", "financial account", "debit card",
                "savings account", "checking account", "transit number", "beneficiary account",
                "payment instruction", "bank transfer",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=[
                "Bank Account Number", "IBAN", "ABA Routing Number",
            ],
            actions=[
                "Block external sharing",
                "Notify sender",
                "Encrypt message",
                "Alert fraud prevention team",
            ],
            compliance_frameworks=["PCI-DSS", "GLBA"],
            severity="high",
            tags=["bank", "account-number", "financial", "fraud-prevention"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block sending bank account numbers and routing details to external recipients',
                'Block uploading banking information to personal cloud storage or unsanctioned apps',
            ],
            specific_audit_actions=[
                'Log all bank account number detections for fraud prevention audit trail',
                'Record access events involving IBAN and routing number content',
            ],
            specific_notifications=[
                'Notify the fraud prevention team when bank account details are detected in email',
                'Alert the finance security team for potential BEC-related bank detail sharing',
            ],
            specific_user_experience="Users are blocked from sending bank account details externally and see: 'This message contains banking information. External sharing has been blocked to prevent financial fraud.'",
            specific_admin_experience='Security administrators see bank account detection incidents in the activity explorer. Real-time alerts are sent to the fraud prevention team for every match.',
            specific_policy_tips=[
                'This content contains bank account details. Sending externally has been blocked to prevent fraud.',
                'Contact the finance team if you need to share payment instructions securely.',
            ],
        ),
        PolicyTemplate(
            id="swift_codes_financial_transfers",
            name="SWIFT Code and Wire Transfer Protection",
            category="Financial",
            description=(
                "Detects SWIFT/BIC codes and wire transfer instructions to prevent unauthorised "
                "international financial transactions and business email compromise (BEC) fraud."
            ),
            keywords=[
                "SWIFT code", "BIC code", "wire transfer", "international transfer",
                "IBAN", "correspondent bank", "beneficiary bank", "remittance",
                "forex", "foreign exchange", "cross-border payment", "SEPA",
                "CHAPS", "FEDWIRE", "RTGS", "payment instruction", "transfer details",
                "bank identifier", "nostro account", "vostro account",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams"],
            sensitive_info_types=["SWIFT Code", "IBAN", "Bank Account Number"],
            actions=[
                "Block external sending",
                "Require manager approval",
                "Alert finance and security teams",
                "Quarantine message for review",
            ],
            compliance_frameworks=["PCI-DSS"],
            severity="high",
            tags=["SWIFT", "wire-transfer", "BEC", "financial", "international"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block emails containing SWIFT codes and wire transfer instructions to unverified recipients',
                'Quarantine messages with wire transfer details for compliance review',
                'Require manager approval before releasing wire transfer instruction emails',
            ],
            specific_audit_actions=[
                'Log all SWIFT code and wire transfer instruction detections',
                'Retain evidence of all wire transfer communications for fraud investigation',
            ],
            specific_notifications=[
                'Notify the finance security team immediately when wire transfer instructions are detected',
                'Alert the CFO and fraud team when SWIFT codes are sent to external parties',
            ],
            specific_user_experience="Users attempting to send wire transfer instructions are blocked and see: 'This message contains wire transfer details. It has been quarantined and requires manager approval to prevent BEC fraud.'",
            specific_admin_experience='Finance security administrators receive real-time alerts for every wire transfer detection. Messages are quarantined for review and full incident details are available in the DLP activity explorer.',
            specific_policy_tips=[
                'This message contains wire transfer instructions. It requires manager approval before sending.',
                'Wire transfer requests must be verified by phone using a known number before releasing.',
            ],
        ),
        PolicyTemplate(
            id="aba_routing_numbers",
            name="ABA Routing Number Detection",
            category="Financial",
            description=(
                "Identifies ABA routing transit numbers used in US banking transactions to "
                "prevent fraud and protect financial transaction integrity."
            ),
            keywords=[
                "ABA routing", "routing number", "transit number", "routing transit number",
                "RTN", "ACH routing", "bank routing", "US bank", "Federal Reserve",
                "electronic funds transfer", "EFT", "direct deposit", "payroll",
                "bank code", "check routing", "MICR", "fractional routing", "9-digit",
                "routing and account", "financial routing",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=["ABA Routing Number", "Bank Account Number"],
            actions=[
                "Alert security operations",
                "Apply sensitivity label",
                "Notify user",
            ],
            compliance_frameworks=["GLBA", "PCI-DSS"],
            severity="medium",
            tags=["ABA", "routing", "banking", "US", "financial"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block external sharing of ABA routing numbers combined with account numbers',
            ],
            specific_audit_actions=[
                'Log all ABA routing number detections in email and documents',
                'Record user and context for ACH fraud prevention audit',
            ],
            specific_notifications=[
                'Notify the fraud prevention team when ABA routing numbers are detected in external communications',
            ],
            specific_user_experience="Users see a policy tip when ABA routing numbers are detected: 'This content contains US banking routing information. External sharing has been restricted.'",
            specific_admin_experience='Security administrators see ABA routing number detections in the DLP activity explorer. Daily digest alerts are sent to the fraud prevention team.',
            specific_policy_tips=[
                'This content contains ABA routing numbers. External sharing is restricted to prevent ACH fraud.',
            ],
        ),
        PolicyTemplate(
            id="financial_statements_reports",
            name="Financial Reports and Earnings Data",
            category="Financial",
            description=(
                "Protects sensitive financial reports, earnings data, and forecasts that could "
                "constitute material non-public information (MNPI) under insider trading regulations."
            ),
            keywords=[
                "earnings per share", "EPS", "revenue forecast", "financial projection",
                "MNPI", "insider information", "material non-public", "pre-announcement",
                "merger", "acquisition", "M&A", "financial results", "profit warning",
                "guidance", "analyst briefing", "investor relations", "quarterly earnings",
                "annual results", "profit and loss", "EBITDA",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams"],
            sensitive_info_types=["Financial Statement", "Earnings Report"],
            actions=[
                "Block external sharing",
                "Notify legal and compliance",
                "Apply strict access controls",
                "Watermark document",
            ],
            compliance_frameworks=["SOX", "SEC Regulation FD"],
            severity="high",
            tags=["MNPI", "insider", "earnings", "financial", "SEC"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block external sharing of earnings forecasts and financial projections before public announcement',
                'Block forwarding of MNPI-classified documents to personal or external email accounts',
            ],
            specific_audit_actions=[
                'Log all access to financial reports and earnings data for insider trading compliance',
                'Record every disclosure of material non-public information (MNPI) for SEC reporting',
            ],
            specific_notifications=[
                'Notify the General Counsel and Investor Relations when MNPI is detected in external communications',
                'Alert the compliance officer for all financial data disclosures outside authorised channels',
            ],
            specific_user_experience="Users are blocked from sharing financial reports externally. A policy tip states: 'This content may contain MNPI. External sharing is prohibited prior to public announcement under Regulation FD and SOX.'",
            specific_admin_experience='Compliance administrators see MNPI incidents in the DLP activity explorer. Real-time alerts are sent to legal and compliance; all incidents are logged for SEC Regulation FD audit purposes.',
            specific_policy_tips=[
                'This document may contain material non-public information (MNPI). External sharing is prohibited before public announcement.',
                'Contact Investor Relations or Legal if you need to share financial data with authorised parties.',
            ],
        ),

        # ── HEALTHCARE (6 templates) ─────────────────────────────────────────
        PolicyTemplate(
            id="hipaa_phi_protection",
            name="HIPAA – Protected Health Information (PHI)",
            category="Healthcare",
            description=(
                "Comprehensive HIPAA compliance template that detects all 18 PHI identifiers "
                "including patient names, dates, geographic data, phone numbers, and medical records."
            ),
            keywords=[
                "HIPAA", "PHI", "protected health information", "patient data", "medical record",
                "health record", "diagnosis", "treatment", "prescription", "patient name",
                "date of birth", "medical condition", "insurance information", "provider",
                "covered entity", "business associate", "health plan", "EHR", "EMR",
                "clinical data",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=[
                "U.S. Individual Taxpayer Identification Number (ITIN)",
                "Medical Record Number", "Health Insurance Claim Number",
                "Drug Enforcement Agency (DEA) Number",
                "U.S. Social Security Number (SSN)",
            ],
            actions=[
                "Block external sharing",
                "Encrypt communication",
                "Alert HIPAA privacy officer",
                "Require business associate agreement acknowledgement",
                "Log access for audit",
            ],
            compliance_frameworks=["HIPAA", "HITECH"],
            severity="high",
            tags=["HIPAA", "PHI", "healthcare", "patient", "medical"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference#us-health-insurance-act-hipaa',
            specific_blocked_actions=[
                'Block email containing PHI (patient name, DOB, diagnosis, or MRN) to non-covered entities',
                'Block upload of PHI to personal cloud storage (non-HIPAA-compliant platforms)',
                'Block copying PHI to USB devices on managed endpoints',
            ],
            specific_audit_actions=[
                'Log all PHI disclosures with the 18 HIPAA identifiers for HIPAA audit trail',
                'Record access events for patient records per HIPAA minimum necessary standard',
                'Capture evidence for HIPAA breach notification assessment',
            ],
            specific_notifications=[
                'Notify the HIPAA Privacy Officer when PHI is detected in SharePoint/OneDrive outside approved sites',
                'Alert the HIPAA Security Officer when PHI is sent to external recipients',
                'Page the compliance officer immediately for PHI detected on unsanctioned cloud services',
            ],
            specific_user_experience="Users are blocked from sharing PHI outside the covered entity network and see: 'This content contains protected health information (PHI) under HIPAA. Sharing outside authorised systems is blocked. Contact your HIPAA Privacy Officer for assistance.'",
            specific_admin_experience='HIPAA Privacy Officers see all PHI incidents in the DLP activity explorer with full breach assessment context. Real-time alerts are sent; incidents are automatically logged for 6-year HIPAA record retention. Potential breach events are escalated for 60-day breach notification assessment.',
            specific_policy_tips=[
                'This content contains Protected Health Information (PHI) under HIPAA. Sharing outside authorised systems is blocked.',
                'PHI may only be shared with covered entities and business associates under an executed BAA.',
                'For authorised PHI transfers, use the HIPAA-compliant secure message or file transfer system.',
            ],
        ),
        PolicyTemplate(
            id="medical_record_numbers",
            name="Medical Record Number (MRN) Detection",
            category="Healthcare",
            description=(
                "Detects medical record numbers (MRNs) and patient identifiers used in "
                "electronic health records to prevent unauthorised disclosure of patient data."
            ),
            keywords=[
                "medical record number", "MRN", "patient identifier", "patient ID",
                "health record ID", "chart number", "encounter number", "admission number",
                "hospital number", "patient account", "visit number", "registration number",
                "EHR ID", "EMR number", "clinical identifier", "patient record",
                "case number", "healthcare ID", "member ID", "patient file",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=["Medical Record Number"],
            actions=[
                "Block sharing outside healthcare network",
                "Notify privacy officer",
                "Apply PHI sensitivity label",
            ],
            compliance_frameworks=["HIPAA", "HITECH"],
            severity="high",
            tags=["MRN", "patient", "healthcare", "PHI", "medical"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference#us-health-insurance-act-hipaa',
            specific_blocked_actions=[
                'Block sharing of medical record numbers (MRNs) outside the healthcare provider network',
                'Block email containing MRNs to non-healthcare recipients',
            ],
            specific_audit_actions=[
                'Log all MRN detections for HIPAA minimum necessary compliance',
                'Record all MRN disclosures for patient data breach assessment',
            ],
            specific_notifications=[
                'Notify the HIPAA Privacy Officer when MRNs are detected outside approved clinical systems',
                'Alert the health information management team on MRN policy violations',
            ],
            specific_user_experience="Users see a policy tip when MRNs are detected: 'This content contains a Medical Record Number (MRN). Sharing outside the clinical network is blocked under HIPAA.'",
            specific_admin_experience='HIPAA administrators see MRN incidents in the DLP activity explorer. Daily digest alerts are sent to the Privacy Officer; potential breaches are escalated.',
            specific_policy_tips=[
                'This content contains a Medical Record Number (MRN). Sharing is restricted to authorised clinical systems.',
            ],
        ),
        PolicyTemplate(
            id="health_insurance_claim_numbers",
            name="Health Insurance Claim Number (HICN) Protection",
            category="Healthcare",
            description=(
                "Detects Medicare health insurance claim numbers and insurance member IDs "
                "to protect beneficiary information and prevent healthcare fraud."
            ),
            keywords=[
                "health insurance claim", "HICN", "Medicare number", "Medicaid number",
                "insurance claim", "beneficiary identifier", "MBI", "Medicare Beneficiary",
                "insurance member ID", "group number", "subscriber ID", "payer ID",
                "claim number", "EOB", "explanation of benefits", "insurance card",
                "coverage number", "plan ID", "enrollment ID", "policy number",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=["Health Insurance Claim Number", "Medicare Number"],
            actions=[
                "Block external transmission",
                "Alert compliance team",
                "Encrypt at rest and in transit",
            ],
            compliance_frameworks=["HIPAA", "CMS"],
            severity="high",
            tags=["HICN", "Medicare", "insurance", "healthcare", "fraud"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference#us-health-insurance-act-hipaa',
            specific_blocked_actions=[
                'Block external sharing of health insurance claim numbers and Medicare IDs',
            ],
            specific_audit_actions=[
                'Log all HICN and Medicare ID detections for HIPAA compliance audit',
            ],
            specific_notifications=[
                'Notify the HIPAA Privacy Officer when health insurance claim numbers are detected in external communications',
            ],
            specific_user_experience="Users are blocked from sharing health insurance claim numbers externally. A policy tip states: 'This content contains a health insurance claim number. Sharing externally is blocked.'",
            specific_admin_experience='Compliance administrators see HICN incidents in the DLP activity explorer. Alerts are sent to the Privacy Officer for each detection.',
            specific_policy_tips=[
                'This content contains a health insurance claim number (HICN). External sharing is restricted under HIPAA.',
            ],
        ),
        PolicyTemplate(
            id="dea_numbers",
            name="Drug Enforcement Agency (DEA) Number Protection",
            category="Healthcare",
            description=(
                "Detects DEA registration numbers assigned to healthcare practitioners "
                "authorised to prescribe controlled substances."
            ),
            keywords=[
                "DEA number", "drug enforcement", "controlled substance", "prescription",
                "narcotic", "Schedule II", "Schedule III", "opioid", "DEA registration",
                "practitioner number", "prescriber ID", "pharmacy", "controlled drug",
                "DEA registrant", "formulary", "dispensing", "healthcare provider",
                "medical license", "NPI", "prescribing authority",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=["Drug Enforcement Agency (DEA) Number"],
            actions=[
                "Block external sharing",
                "Notify DEA compliance officer",
                "Restrict to authorised personnel",
            ],
            compliance_frameworks=["HIPAA", "DEA Regulations", "CSA"],
            severity="high",
            tags=["DEA", "prescription", "controlled-substance", "healthcare"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block external sharing of DEA registration numbers and controlled substance prescriptions',
            ],
            specific_audit_actions=[
                'Log all DEA number detections for DEA compliance audit',
                'Record prescription data access for controlled substance monitoring',
            ],
            specific_notifications=[
                'Notify the pharmacy compliance officer when DEA numbers are detected in external communications',
            ],
            specific_user_experience="Users see a policy tip: 'This content contains a DEA number or controlled substance prescription. External sharing is blocked under DEA regulations.'",
            specific_admin_experience='Compliance administrators see DEA number incidents in the activity explorer. Real-time alerts are sent to the pharmacy compliance officer.',
            specific_policy_tips=[
                'This content contains a DEA registration number. External sharing is restricted under DEA regulations.',
            ],
        ),
        PolicyTemplate(
            id="healthcare_privacy_general",
            name="Healthcare Privacy – General Patient Data",
            category="Healthcare",
            description=(
                "Broad healthcare privacy policy to detect combinations of patient identifiers "
                "including names, dates of birth, diagnoses, and contact information."
            ),
            keywords=[
                "patient", "diagnosis", "treatment plan", "medical history", "clinical note",
                "discharge summary", "lab result", "radiology", "pathology", "medication",
                "allergy", "immunisation", "vital signs", "blood type", "mental health",
                "substance abuse", "HIV status", "genetic information", "family history",
                "referring physician",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices", "PowerBI"],
            sensitive_info_types=[
                "Medical Record Number", "Patient Name with Date of Birth",
                "Health Insurance Claim Number",
            ],
            actions=[
                "Apply PHI label",
                "Block unapproved external sharing",
                "Notify privacy officer",
            ],
            compliance_frameworks=["HIPAA", "HITECH", "State Privacy Laws"],
            severity="medium",
            tags=["healthcare", "patient", "privacy", "clinical", "PHI"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference#us-health-insurance-act-hipaa',
            specific_blocked_actions=[
                'Block sharing of patient health data outside the covered entity network',
                'Block upload of patient records to non-HIPAA-compliant cloud services',
            ],
            specific_audit_actions=[
                'Log all patient data disclosures for healthcare privacy compliance',
                'Record access to clinical information for HIPAA audit trail',
            ],
            specific_notifications=[
                'Notify the Privacy Officer when patient health information is detected in external communications',
            ],
            specific_user_experience='Users are blocked from sharing patient data outside approved healthcare systems. A policy tip explains that patient privacy regulations restrict external sharing.',
            specific_admin_experience='Healthcare compliance administrators see patient data incidents in the DLP activity explorer. Alerts are sent daily to the Privacy Officer; high-severity incidents are escalated.',
            specific_policy_tips=[
                'This content contains patient health information. Sharing outside authorised healthcare systems is blocked.',
            ],
        ),
        PolicyTemplate(
            id="hipaa_minimum_necessary",
            name="HIPAA – Minimum Necessary Standard",
            category="Healthcare",
            description=(
                "Enforces the HIPAA minimum necessary standard by detecting bulk PHI transfers "
                "or access to PHI beyond what is required for the intended purpose."
            ),
            keywords=[
                "minimum necessary", "HIPAA", "bulk patient data", "mass export",
                "large dataset", "de-identification", "limited data set", "data aggregation",
                "population health", "research dataset", "IRB", "data use agreement",
                "authorisation form", "consent", "treatment purpose", "payment purpose",
                "healthcare operations", "access request", "data request", "ROI",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Devices", "PowerBI"],
            sensitive_info_types=["Medical Record Number", "Health Insurance Claim Number"],
            actions=[
                "Require justification",
                "Alert privacy officer for large transfers",
                "Block bulk exports without approval",
                "Audit all access",
            ],
            compliance_frameworks=["HIPAA"],
            severity="medium",
            tags=["HIPAA", "minimum-necessary", "PHI", "bulk-data", "healthcare"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference#us-health-insurance-act-hipaa',
            specific_blocked_actions=[
                'Block sharing of PHI that exceeds the minimum necessary standard for the stated purpose',
            ],
            specific_audit_actions=[
                'Log all PHI access events to verify minimum necessary compliance',
                'Record user role and access justification for HIPAA minimum necessary audits',
            ],
            specific_notifications=[
                'Notify the HIPAA Privacy Officer when PHI is shared beyond the minimum necessary amount',
            ],
            specific_user_experience="Users see a policy tip when accessing PHI beyond their role-based minimum necessary access: 'HIPAA minimum necessary standard applies. Only access the PHI required for your specific task.'",
            specific_admin_experience='Privacy Officers see minimum necessary violations in the DLP activity explorer. Alerts are sent for every over-sharing incident; role-based access reviews are triggered.',
            specific_policy_tips=[
                'HIPAA minimum necessary standard: only access and share the minimum PHI required for your specific healthcare task.',
            ],
        ),

        # ── PRIVACY / PII (8 templates) ──────────────────────────────────────
        PolicyTemplate(
            id="gdpr_eu_personal_data",
            name="GDPR – EU Personal Data Protection",
            category="Privacy",
            description=(
                "Comprehensive GDPR compliance template detecting personal data of EU residents "
                "including names, email addresses, location data, and special category data."
            ),
            keywords=[
                "GDPR", "General Data Protection Regulation", "personal data", "data subject",
                "EU resident", "lawful basis", "consent", "data processing", "data controller",
                "data processor", "right to erasure", "right to access", "data portability",
                "privacy notice", "DPA", "data protection authority", "supervisory authority",
                "cross-border transfer", "standard contractual clauses", "SCC",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices", "PowerBI"],
            sensitive_info_types=[
                "EU Debit Card Number", "EU Driver's License Number",
                "EU National Identification Number", "EU Passport Number",
                "EU Social Security Number", "EU Tax Identification Number",
            ],
            actions=[
                "Block transfer outside EEA without safeguards",
                "Apply GDPR sensitivity label",
                "Notify Data Protection Officer",
                "Require privacy impact assessment",
            ],
            compliance_frameworks=["GDPR"],
            severity="high",
            tags=["GDPR", "EU", "personal-data", "privacy", "data-protection"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference#eu-general-data-protection-regulation-gdpr',
            specific_blocked_actions=[
                'Block transfer of EU personal data to third countries without adequate GDPR safeguards',
                'Block sharing of EU special category data (health, race, religion) without explicit consent',
                'Block upload of EU personal data to cloud services outside the EEA without SCCs',
            ],
            specific_audit_actions=[
                'Log all EU personal data transfers for GDPR Article 30 records of processing activities',
                'Record lawful basis for each personal data disclosure for GDPR accountability',
                'Capture evidence for GDPR data subject access request (DSAR) response',
            ],
            specific_notifications=[
                'Notify the Data Protection Officer (DPO) when EU personal data is transferred internationally',
                'Alert the privacy team when GDPR special category data is detected outside approved systems',
                'Notify the DPO of potential GDPR breaches for 72-hour supervisory authority notification assessment',
            ],
            specific_user_experience="Users are blocked from transferring EU personal data to unapproved destinations and see: 'This content contains EU personal data protected under GDPR. Transfer outside the EEA requires authorisation from your Data Protection Officer.'",
            specific_admin_experience='The DPO and privacy team see GDPR incidents in the DLP activity explorer with personal data context and transfer details. Real-time alerts are sent for international transfers; potential breaches are flagged for 72-hour Article 33 notification assessment.',
            specific_policy_tips=[
                'This content contains EU personal data under GDPR. International transfers require adequate safeguards (SCCs, BCRs, or adequacy decision).',
                'Special category data (health, biometric, racial origin) requires explicit consent or another Article 9 legal basis.',
                'Contact your Data Protection Officer before transferring EU personal data outside the EEA.',
            ],
        ),
        PolicyTemplate(
            id="ccpa_california_consumer_privacy",
            name="CCPA – California Consumer Privacy Act",
            category="Privacy",
            description=(
                "Protects personal information of California residents as defined under CCPA/CPRA, "
                "including identifiers, commercial information, and sensitive personal information."
            ),
            keywords=[
                "CCPA", "CPRA", "California Consumer Privacy", "California resident",
                "personal information", "opt-out", "right to know", "right to delete",
                "sensitive personal information", "SPI", "sale of data", "sharing of data",
                "data broker", "consumer rights", "privacy rights", "do not sell",
                "third party disclosure", "business purpose", "service provider",
                "California Privacy Rights Act",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices", "PowerBI"],
            sensitive_info_types=[
                "U.S. Social Security Number (SSN)", "U.S. Driver's License Number",
                "U.S. Individual Taxpayer Identification Number (ITIN)",
            ],
            actions=[
                "Block sale or sharing without consent",
                "Apply CCPA sensitivity label",
                "Notify privacy compliance team",
                "Honour opt-out requests",
            ],
            compliance_frameworks=["CCPA", "CPRA"],
            severity="high",
            tags=["CCPA", "CPRA", "California", "privacy", "consumer"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block selling or sharing California consumer personal information without opt-out compliance',
                'Block transfer of CCPA-covered data to third parties without data processing agreements',
            ],
            specific_audit_actions=[
                'Log all California consumer personal information disclosures for CCPA compliance',
                'Record data flows for CCPA data mapping and privacy impact assessments',
            ],
            specific_notifications=[
                'Notify the Privacy Officer when California consumer data is shared with third parties',
                'Alert the legal team on CCPA opt-out requests involving detected personal data',
            ],
            specific_user_experience="Users see a policy tip when CCPA-covered data is detected: 'This content contains California consumer personal information under CCPA. Sharing with third parties requires opt-out compliance verification.'",
            specific_admin_experience='Privacy administrators see CCPA incidents in the DLP activity explorer. Alerts are sent to the Privacy Officer; incidents are logged for CCPA audit.',
            specific_policy_tips=[
                'This content contains California consumer personal information under CCPA. Third-party sharing requires opt-out compliance.',
            ],
        ),
        PolicyTemplate(
            id="lgpd_brazil_personal_data",
            name="LGPD – Brazil Personal Data Protection",
            category="Privacy",
            description=(
                "Protects personal data of Brazilian citizens under the Lei Geral de Proteção "
                "de Dados (LGPD), Brazil's comprehensive data protection regulation."
            ),
            keywords=[
                "LGPD", "Lei Geral de Proteção de Dados", "Brazilian personal data",
                "dado pessoal", "titular", "CPF", "RG", "Brazilian ID", "ANPD",
                "data processing Brazil", "sensitive data Brazil", "biometric data",
                "health data Brazil", "ethnic origin", "political opinion", "religious belief",
                "legitimate interest", "data protection Brazil", "privacy Brazil",
                "consent Brazil",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=[
                "Brazil CPF Number", "Brazil RG Number", "Brazil National ID",
            ],
            actions=[
                "Block international transfer without DPA",
                "Apply LGPD label",
                "Notify Data Protection Officer",
            ],
            compliance_frameworks=["LGPD"],
            severity="high",
            tags=["LGPD", "Brazil", "personal-data", "privacy", "ANPD"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block international transfer of Brazilian personal data without LGPD compliance',
            ],
            specific_audit_actions=[
                'Log all Brazilian personal data disclosures for LGPD compliance records',
            ],
            specific_notifications=[
                'Notify the Data Protection Officer when Brazilian personal data is transferred internationally',
            ],
            specific_user_experience="Users see a policy tip: 'This content contains Brazilian personal data protected under LGPD. International transfer requires DPO approval.'",
            specific_admin_experience='Compliance administrators see LGPD incidents in the DLP activity explorer. Alerts are sent to the DPO for international data transfers.',
            specific_policy_tips=[
                'This content contains Brazilian personal data under LGPD. International transfers require ANPD-compliant safeguards.',
            ],
        ),
        PolicyTemplate(
            id="popia_south_africa",
            name="POPIA – South Africa Personal Information Protection",
            category="Privacy",
            description=(
                "Protects personal information under South Africa's Protection of Personal "
                "Information Act (POPIA), including special personal information."
            ),
            keywords=[
                "POPIA", "Protection of Personal Information", "personal information",
                "South Africa", "data subject", "responsible party", "operator",
                "Information Regulator", "SARS number", "South African ID", "SAID",
                "special personal information", "biometric information", "race",
                "gender", "pregnancy", "national origin", "trade union membership",
                "criminal behaviour", "religious belief", "lawful processing",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=[
                "South Africa ID Number", "South Africa Tax Identification Number",
            ],
            actions=[
                "Block transfer outside South Africa without safeguards",
                "Apply POPIA label",
                "Notify Information Officer",
            ],
            compliance_frameworks=["POPIA"],
            severity="high",
            tags=["POPIA", "South-Africa", "personal-information", "privacy"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block transfer of South African personal information outside South Africa without POPIA compliance',
            ],
            specific_audit_actions=[
                'Log all South African personal information disclosures for POPIA compliance',
            ],
            specific_notifications=[
                'Notify the Information Officer when South African personal information is shared externally',
            ],
            specific_user_experience="Users see a policy tip: 'This content contains South African personal information under POPIA. Cross-border transfers require adequate protection standards.'",
            specific_admin_experience='Compliance administrators see POPIA incidents in the DLP activity explorer. Alerts are sent to the Information Officer.',
            specific_policy_tips=[
                'This content contains South African personal information under POPIA. Cross-border transfers require compliance verification.',
            ],
        ),
        PolicyTemplate(
            id="pdpa_singapore",
            name="PDPA – Singapore Personal Data Protection",
            category="Privacy",
            description=(
                "Protects personal data of Singapore residents under the Personal Data "
                "Protection Act (PDPA), covering collection, use, and disclosure."
            ),
            keywords=[
                "PDPA", "Personal Data Protection Act", "Singapore personal data",
                "NRIC", "FIN", "Singapore identity", "PDPC", "Personal Data Protection Commission",
                "consent obligation", "notification obligation", "access and correction",
                "data breach notification", "do not call", "DNC registry",
                "legitimate interests", "transfer limitation", "data intermediary",
                "mandatory breach notification", "enhanced financial penalty",
                "significant scale",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=[
                "Singapore National Registration Identity Card (NRIC) Number",
                "Singapore Passport Number",
            ],
            actions=[
                "Block unauthorised disclosure",
                "Notify data protection officer",
                "Apply PDPA sensitivity label",
            ],
            compliance_frameworks=["PDPA"],
            severity="high",
            tags=["PDPA", "Singapore", "NRIC", "personal-data", "privacy"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block transfer of Singapore personal data outside Singapore without PDPA compliance',
            ],
            specific_audit_actions=[
                'Log all Singapore personal data disclosures for PDPA mandatory breach notification compliance',
            ],
            specific_notifications=[
                'Notify the Data Protection Officer when Singapore personal data is transferred internationally',
            ],
            specific_user_experience="Users see a policy tip: 'This content contains Singapore personal data under PDPA. International transfers must comply with PDPA transfer limitation obligations.'",
            specific_admin_experience='Compliance administrators see PDPA incidents in the DLP activity explorer. Alerts are sent to the DPO; data breaches are flagged for mandatory PDPC notification.',
            specific_policy_tips=[
                'This content contains Singapore personal data under PDPA. International transfers require PDPA-compliant safeguards.',
            ],
        ),
        PolicyTemplate(
            id="us_social_security_numbers",
            name="US Social Security Number (SSN) Protection",
            category="Privacy",
            description=(
                "Detects US Social Security Numbers in documents, emails, and files to prevent "
                "identity theft and ensure compliance with federal and state privacy laws."
            ),
            keywords=[
                "social security number", "SSN", "social security", "tax ID", "ITIN",
                "government ID", "federal ID", "identity number", "nine-digit",
                "XXX-XX-XXXX", "taxpayer ID", "employment authorisation", "W-2",
                "1099", "tax form", "employee number", "benefits number",
                "Medicare number", "retirement account", "wage report",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices", "PowerBI"],
            sensitive_info_types=[
                "U.S. Social Security Number (SSN)",
                "U.S. Individual Taxpayer Identification Number (ITIN)",
            ],
            actions=[
                "Block send/share externally",
                "Alert security team",
                "Apply restricted sensitivity label",
                "Notify sender",
            ],
            compliance_frameworks=["GLBA", "CCPA", "State Privacy Laws"],
            severity="high",
            tags=["SSN", "US", "identity", "PII", "social-security"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block sending Social Security Numbers (SSNs) to external recipients in email',
                'Block upload of files containing SSNs to non-approved cloud storage',
                'Block copying SSN data to USB devices on managed endpoints',
            ],
            specific_audit_actions=[
                'Log all SSN detections with matched content evidence for identity theft prevention',
                'Record sender, recipients, and file context for SSN exposure incident response',
            ],
            specific_notifications=[
                'Notify the privacy and security team when SSNs are detected in external communications',
                'Alert the identity theft response team for SSN exposure incidents',
            ],
            specific_user_experience="Users are blocked from sharing SSNs externally and see: 'This content contains a US Social Security Number. External sharing is blocked to prevent identity theft. Use the secure HR portal for SSN processing.'",
            specific_admin_experience='Security administrators see SSN exposure incidents in the DLP activity explorer. Real-time alerts are sent to the identity theft response team; incidents with more than 10 SSNs are escalated for state breach notification assessment.',
            specific_policy_tips=[
                'This content contains a US Social Security Number (SSN). External sharing is blocked to prevent identity theft.',
                'SSNs should only be processed in approved HR and payroll systems with access controls.',
            ],
        ),
        PolicyTemplate(
            id="passport_numbers",
            name="Passport Number Detection",
            category="Privacy",
            description=(
                "Detects passport numbers from multiple countries to protect government-issued "
                "travel documents and prevent identity fraud."
            ),
            keywords=[
                "passport number", "passport", "travel document", "government ID",
                "international travel", "visa application", "border control",
                "immigration document", "nationality", "citizenship", "country of issue",
                "expiry date", "biometric passport", "e-passport", "ICAO",
                "MRZ", "machine readable zone", "passport holder", "foreign national",
                "consular document",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=[
                "U.S. Passport Number", "EU Passport Number", "UK Passport Number",
                "Australia Passport Number", "Canada Passport Number",
            ],
            actions=[
                "Block external sharing",
                "Apply highly confidential label",
                "Alert HR and security",
            ],
            compliance_frameworks=["GDPR", "CCPA", "POPIA"],
            severity="high",
            tags=["passport", "travel-document", "identity", "PII", "government-ID"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block external sharing of passport numbers without authorisation',
            ],
            specific_audit_actions=[
                'Log all passport number detections for privacy compliance audit',
            ],
            specific_notifications=[
                'Notify the privacy team when passport numbers are detected in external email or documents',
            ],
            specific_user_experience="Users see a policy tip when passport numbers are detected: 'This content contains a passport number. External sharing requires authorisation.'",
            specific_admin_experience='Privacy administrators see passport number incidents in the DLP activity explorer. Alerts are sent to the privacy team for each detection.',
            specific_policy_tips=[
                'This content contains a passport number. Sharing is restricted to approved identity verification processes.',
            ],
        ),
        PolicyTemplate(
            id="drivers_license_numbers",
            name="Driver's License Number Protection",
            category="Privacy",
            description=(
                "Identifies driver's license numbers from US states and international jurisdictions "
                "to prevent identity theft and comply with state privacy regulations."
            ),
            keywords=[
                "driver's license", "driving license", "drivers licence", "DL number",
                "state ID", "motor vehicle", "DMV", "DVLA", "license number",
                "photo ID", "government identification", "license expiry", "license class",
                "CDL", "commercial driver", "vehicle operator", "state-issued ID",
                "license plate", "registration", "identity document",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=[
                "U.S. Driver's License Number", "EU Driver's License Number",
                "UK Driver's License Number",
            ],
            actions=[
                "Block external transmission",
                "Notify sender with policy tip",
                "Apply PII sensitivity label",
            ],
            compliance_frameworks=["CCPA", "GDPR", "State Privacy Laws"],
            severity="high",
            tags=["drivers-license", "state-ID", "identity", "PII", "DMV"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block external sharing of driver licence numbers without authorisation',
            ],
            specific_audit_actions=[
                'Log all driver licence number detections for privacy compliance',
            ],
            specific_notifications=[
                'Notify the privacy team when driver licence numbers are detected in external communications',
            ],
            specific_user_experience="Users see a policy tip: 'This content contains a driver licence number. External sharing is restricted to approved identity verification processes.'",
            specific_admin_experience='Privacy administrators see driver licence incidents in the DLP activity explorer. Daily digest alerts are sent to the privacy team.',
            specific_policy_tips=[
                'This content contains a driver licence number. External sharing is restricted to authorised identity processes.',
            ],
        ),

        # ── REGIONAL (5 templates) ────────────────────────────────────────────
        PolicyTemplate(
            id="uk_data_protection_act",
            name="UK Data Protection Act 2018 / UK GDPR",
            category="Regional",
            description=(
                "Protects personal data of UK residents under the Data Protection Act 2018 "
                "and UK GDPR, which retained EU GDPR principles post-Brexit."
            ),
            keywords=[
                "UK GDPR", "Data Protection Act", "DPA 2018", "ICO", "Information Commissioner",
                "UK personal data", "UK resident", "special category data", "NI number",
                "National Insurance", "UK passport", "UK driving licence", "UKDL",
                "adequacy decision", "international transfer UK", "legitimate interest",
                "accountability principle", "UK data controller", "data protection officer",
                "lawful basis UK",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=[
                "UK National Insurance Number", "UK Passport Number",
                "UK Driver's License Number", "UK NHS Number",
            ],
            actions=[
                "Block transfer outside UK without adequacy",
                "Apply UK GDPR label",
                "Notify UK Data Protection Officer",
                "Generate ICO-compliant audit log",
            ],
            compliance_frameworks=["UK GDPR", "DPA 2018"],
            severity="high",
            tags=["UK-GDPR", "DPA", "UK", "ICO", "personal-data"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block transfer of UK personal data outside the UK without UK GDPR-equivalent safeguards',
                'Block sharing of UK special category data without explicit consent or legal basis',
            ],
            specific_audit_actions=[
                'Log all UK personal data disclosures for UK GDPR Article 30 records',
                'Record lawful basis for each UK personal data transfer',
            ],
            specific_notifications=[
                'Notify the UK Data Protection Officer when UK personal data is transferred internationally',
                'Alert the DPO of potential UK GDPR breaches for ICO notification assessment',
            ],
            specific_user_experience="Users are blocked from transferring UK personal data without adequate safeguards. A policy tip states: 'This content contains UK personal data under the UK GDPR/DPA 2018. International transfer requires approved safeguards.'",
            specific_admin_experience='The UK DPO sees incidents in the DLP activity explorer. Real-time alerts are sent for international transfers; breaches are flagged for 72-hour ICO notification assessment.',
            specific_policy_tips=[
                'This content contains UK personal data under the Data Protection Act 2018 / UK GDPR. International transfers require ICO-approved safeguards.',
            ],
        ),
        PolicyTemplate(
            id="australia_privacy_act",
            name="Australia Privacy Act – Australian Privacy Principles",
            category="Regional",
            description=(
                "Protects personal and sensitive information under Australia's Privacy Act 1988 "
                "and the 13 Australian Privacy Principles (APPs)."
            ),
            keywords=[
                "Australia Privacy Act", "APP", "Australian Privacy Principles", "OAIC",
                "Office of the Australian Information Commissioner", "TFN", "tax file number",
                "Medicare number Australia", "ABN", "ACN", "Australian business number",
                "Australian personal information", "sensitive information Australia",
                "notifiable data breach", "NDB scheme", "health information Australia",
                "racial or ethnic origin", "political opinions", "religious beliefs",
                "sexual orientation", "criminal record",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=[
                "Australia Tax File Number", "Australia Medicare Number",
                "Australia Passport Number", "Australia Bank Account Number",
            ],
            actions=[
                "Block overseas disclosure without consent",
                "Apply Australian Privacy label",
                "Notify Privacy Officer",
                "Log breach for NDB scheme",
            ],
            compliance_frameworks=["Australia Privacy Act", "APPs"],
            severity="high",
            tags=["Australia", "Privacy-Act", "APP", "OAIC", "TFN"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block cross-border transfer of Australian personal information without APP 8 compliance',
            ],
            specific_audit_actions=[
                'Log all Australian personal information disclosures for Privacy Act APP compliance',
            ],
            specific_notifications=[
                'Notify the Privacy Officer when Australian personal information is transferred overseas',
            ],
            specific_user_experience="Users see a policy tip: 'This content contains Australian personal information under the Privacy Act. Overseas disclosure requires APP 8 compliance.'",
            specific_admin_experience='Privacy administrators see Australian personal information incidents in the DLP activity explorer. Alerts are sent to the Privacy Officer; notifiable data breaches are flagged for OAIC notification.',
            specific_policy_tips=[
                'This content contains Australian personal information under the Privacy Act 1988. Overseas transfers require APP 8 compliance.',
            ],
        ),
        PolicyTemplate(
            id="canada_pipeda",
            name="Canada PIPEDA – Personal Information Protection",
            category="Regional",
            description=(
                "Protects personal information of Canadians under PIPEDA (Personal Information "
                "Protection and Electronic Documents Act) and provincial privacy laws."
            ),
            keywords=[
                "PIPEDA", "Personal Information Protection Electronic Documents Act",
                "Canada personal information", "OPC", "Privacy Commissioner Canada",
                "SIN", "social insurance number", "Canadian passport", "provincial ID",
                "health card number", "PHIPA Ontario", "PIPA Alberta", "PIPA BC",
                "Canadian resident", "meaningful consent", "access to information",
                "right to correction", "challenging compliance", "safeguarding principle",
                "breach of security safeguards",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=[
                "Canada Social Insurance Number", "Canada Passport Number",
                "Canada Bank Account Number", "Canada Health Service Number",
            ],
            actions=[
                "Block cross-border transfer without consent",
                "Apply PIPEDA label",
                "Notify Chief Privacy Officer",
            ],
            compliance_frameworks=["PIPEDA", "PIPEDA Provincial Equivalents"],
            severity="high",
            tags=["PIPEDA", "Canada", "SIN", "personal-information", "privacy"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block transfer of Canadian personal information to third parties without PIPEDA consent',
            ],
            specific_audit_actions=[
                'Log all Canadian personal information disclosures for PIPEDA compliance',
            ],
            specific_notifications=[
                'Notify the Privacy Officer when Canadian personal information is shared without consent',
            ],
            specific_user_experience="Users see a policy tip: 'This content contains Canadian personal information under PIPEDA. Sharing with third parties requires individual consent.'",
            specific_admin_experience='Compliance administrators see PIPEDA incidents in the DLP activity explorer. Alerts are sent to the Privacy Officer; breaches are flagged for OPC notification.',
            specific_policy_tips=[
                'This content contains Canadian personal information under PIPEDA. Third-party sharing requires consent.',
            ],
        ),
        PolicyTemplate(
            id="japan_appi",
            name="Japan APPI – Act on Protection of Personal Information",
            category="Regional",
            description=(
                "Protects personal information of Japanese residents under the Act on "
                "the Protection of Personal Information (APPI), including sensitive personal info."
            ),
            keywords=[
                "APPI", "Act on Protection of Personal Information", "Japan personal information",
                "PPC", "Personal Information Protection Commission Japan",
                "My Number", "Individual Number Japan", "Japanese ID", "sensitive personal info",
                "special care-required", "third-party provision", "foreign transfer Japan",
                "anonymously processed information", "pseudonymously processed",
                "retained personal data", "purpose of use", "consent Japan",
                "data breach Japan", "opt-out provision",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=[
                "Japan My Number", "Japan Passport Number", "Japan Resident Registration Number",
            ],
            actions=[
                "Block overseas transfer without safeguards",
                "Apply APPI sensitivity label",
                "Notify Personal Information Protection Manager",
            ],
            compliance_frameworks=["APPI"],
            severity="high",
            tags=["APPI", "Japan", "My-Number", "personal-information", "privacy"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block transfer of Japanese personal information to third parties without APPI consent',
            ],
            specific_audit_actions=[
                'Log all Japanese personal information disclosures for APPI compliance',
            ],
            specific_notifications=[
                'Notify the Privacy Officer when Japanese personal information is transferred to third parties',
            ],
            specific_user_experience="Users see a policy tip: 'This content contains Japanese personal information under APPI. Third-party provision requires data subject consent.'",
            specific_admin_experience='Compliance administrators see APPI incidents in the DLP activity explorer. Alerts are sent to the Privacy Officer; leakage incidents are flagged for PPC notification.',
            specific_policy_tips=[
                'This content contains Japanese personal information under APPI. Third-party transfers require consent or APPI exception.',
            ],
        ),
        PolicyTemplate(
            id="india_pdp_bill",
            name="India DPDP Act – Digital Personal Data Protection",
            category="Regional",
            description=(
                "Protects personal data of Indian residents under the Digital Personal Data "
                "Protection Act (DPDPA) 2023, covering processing and cross-border transfers."
            ),
            keywords=[
                "India DPDP", "Digital Personal Data Protection", "DPDPA", "India personal data",
                "data fiduciary", "data principal", "data processor India", "Aadhaar",
                "PAN card India", "Aadhaar number", "Indian passport", "UIDAI",
                "consent manager India", "significant data fiduciary", "CERT-In",
                "data localisation India", "data embassy", "cross-border India",
                "right to correction India", "right to erasure India",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=[
                "India Aadhaar Number", "India Permanent Account Number (PAN)",
                "India Passport Number",
            ],
            actions=[
                "Block transfer to restricted countries",
                "Apply India data protection label",
                "Notify Data Protection Officer India",
            ],
            compliance_frameworks=["DPDPA 2023"],
            severity="high",
            tags=["DPDPA", "India", "Aadhaar", "PAN", "personal-data"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block cross-border transfer of Indian personal data to non-approved countries',
            ],
            specific_audit_actions=[
                'Log all Indian personal data disclosures for DPDP Act compliance',
            ],
            specific_notifications=[
                'Notify the Data Protection Officer when Indian personal data is transferred internationally',
            ],
            specific_user_experience="Users see a policy tip: 'This content contains Indian personal data under the DPDP Act. Cross-border transfers require compliance with approved transfer mechanisms.'",
            specific_admin_experience='Compliance administrators see DPDP incidents in the DLP activity explorer. Alerts are sent to the DPO; data breaches are flagged for DPBI notification.',
            specific_policy_tips=[
                'This content contains Indian personal data under the Digital Personal Data Protection Act. Cross-border transfers require government approval.',
            ],
        ),

        # ── IP PROTECTION (4 templates) ──────────────────────────────────────
        PolicyTemplate(
            id="source_code_protection",
            name="Source Code and Software IP Protection",
            category="IP Protection",
            description=(
                "Detects source code, API keys, cryptographic secrets, and software intellectual "
                "property to prevent exfiltration of proprietary software assets."
            ),
            keywords=[
                "source code", "API key", "secret key", "private key", "access token",
                "OAuth token", "connection string", "password hash", "repository",
                "Git", "GitHub", "proprietary code", "trade secret software",
                "algorithm", "software architecture", "API endpoint", "database schema",
                "configuration file", "environment variable", "credential",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=[
                "Azure SAS Token", "Azure Storage Account Key",
                "General Software Authorship Rights",
            ],
            actions=[
                "Block external sharing",
                "Alert security operations immediately",
                "Apply highly confidential label",
                "Revoke access and investigate",
            ],
            compliance_frameworks=["Trade Secret Law", "DMCA"],
            severity="high",
            tags=["source-code", "API-key", "software-IP", "trade-secret", "developer"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block upload of source code repositories and API keys to personal cloud storage or external services',
                'Block email of source code archives or API credentials to external recipients',
                'Block copy of source code to USB devices on developer endpoints',
            ],
            specific_audit_actions=[
                'Log all source code and credential detection events for IP theft investigation',
                'Record developer identity and destination for all code exfiltration attempts',
            ],
            specific_notifications=[
                'Alert the security operations centre immediately when source code or API keys are detected outside approved repositories',
                'Notify the CTO and legal team when proprietary algorithms are detected in external channels',
            ],
            specific_user_experience="Developers are blocked from sharing source code or API credentials externally and see: 'This content contains proprietary source code or credentials. External sharing is blocked. Use the approved code review platform for external collaboration.'",
            specific_admin_experience='Security administrators receive real-time alerts for source code exfiltration attempts. Full incident details including repository name, file type, and destination are logged in the DLP activity explorer. Incidents involving credentials are escalated to the security team for immediate credential rotation.',
            specific_policy_tips=[
                'This content contains proprietary source code or API credentials. External sharing is blocked.',
                'API keys and secrets detected outside approved secret managers require immediate rotation.',
            ],
        ),
        PolicyTemplate(
            id="trade_secrets",
            name="Trade Secret and Confidential Business Information",
            category="IP Protection",
            description=(
                "Identifies and protects trade secrets, confidential business strategies, "
                "and proprietary business information from unauthorised disclosure."
            ),
            keywords=[
                "trade secret", "confidential", "proprietary", "NDA", "non-disclosure",
                "competitive intelligence", "business strategy", "strategic plan",
                "product roadmap", "market analysis", "customer list", "pricing strategy",
                "manufacturing process", "formula", "invention", "know-how",
                "confidential information", "commercially sensitive", "restricted",
                "under embargo",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=["Confidential Document", "Trade Secret"],
            actions=[
                "Block external sharing without NDA",
                "Apply trade secret label",
                "Alert legal team",
                "Require justification",
            ],
            compliance_frameworks=["DTSA", "UTSA", "Trade Secret Law"],
            severity="high",
            tags=["trade-secret", "NDA", "confidential", "business-IP", "proprietary"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block external sharing of trade secrets and confidential business strategy documents',
                'Block forwarding of NDA-protected documents to unapproved parties',
            ],
            specific_audit_actions=[
                'Log all trade secret access and disclosure events for IP litigation support',
                'Record all NDA-protected document access for legal due diligence',
            ],
            specific_notifications=[
                'Alert the legal team immediately when trade secrets are detected in external communications',
                'Notify the CISO when proprietary business strategy documents are shared externally',
            ],
            specific_user_experience="Users are blocked from sharing trade secrets externally and see: 'This document contains confidential trade secret information. External sharing requires a signed NDA and legal team approval.'",
            specific_admin_experience='Legal and compliance administrators see trade secret incidents in the DLP activity explorer. Real-time alerts go to the legal team; all incidents are preserved as potential litigation evidence.',
            specific_policy_tips=[
                'This content contains confidential trade secret information. External sharing requires NDA and legal approval.',
                'Contact the Legal team before sharing any proprietary business strategies or processes externally.',
            ],
        ),
        PolicyTemplate(
            id="patent_documents",
            name="Patent Applications and IP Documentation",
            category="IP Protection",
            description=(
                "Protects patent applications, invention disclosures, and pre-publication IP "
                "documentation that must remain confidential before patent filing."
            ),
            keywords=[
                "patent application", "invention disclosure", "patent pending", "prior art",
                "claims", "specification", "USPTO", "EPO", "WIPO", "PCT application",
                "patent filing", "provisional patent", "utility patent", "design patent",
                "patent attorney", "patent examiner", "patent portfolio", "IP disclosure",
                "confidential invention", "trade secret vs patent",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=["Patent Application", "IP Disclosure"],
            actions=[
                "Restrict to IP legal team only",
                "Prevent premature public disclosure",
                "Alert patent counsel",
                "Log all access",
            ],
            compliance_frameworks=["Patent Law", "35 USC", "EPC"],
            severity="high",
            tags=["patent", "invention", "IP", "USPTO", "EPO"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block external sharing of patent applications and invention disclosures before filing',
                'Block access to pre-filing patent documents outside the IP legal team',
            ],
            specific_audit_actions=[
                'Log all patent application access events for IP portfolio management',
                'Record all pre-filing patent document disclosures for patent invalidation risk assessment',
            ],
            specific_notifications=[
                'Notify patent counsel immediately when invention disclosure or patent application is detected externally',
            ],
            specific_user_experience="Users are blocked from sharing patent documents and see: 'This document contains a patent application or invention disclosure. External sharing before filing could invalidate patent rights. Contact patent counsel.'",
            specific_admin_experience='Patent counsel receives real-time alerts when patent documents are accessed outside the IP team. All incidents are logged for patent portfolio risk assessment.',
            specific_policy_tips=[
                'This document contains a patent application or invention disclosure. Premature external disclosure could invalidate patent rights.',
                'Contact patent counsel before sharing any pre-filing IP documentation.',
            ],
        ),
        PolicyTemplate(
            id="confidential_markings",
            name="Confidential Document Marking Detection",
            category="IP Protection",
            description=(
                "Detects documents marked as Confidential, Restricted, Top Secret, or similar "
                "sensitivity markings to enforce handling policies automatically."
            ),
            keywords=[
                "confidential", "restricted", "top secret", "secret", "internal only",
                "do not distribute", "not for external distribution", "private",
                "sensitive", "classified", "under embargo", "proprietary", "strictly confidential",
                "attorney-client privilege", "attorney work product", "privileged",
                "for internal use only", "business confidential", "company confidential",
                "draft – do not distribute",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices", "PowerBI"],
            sensitive_info_types=["Confidential Document Marking", "Restricted Classification"],
            actions=[
                "Enforce handling based on label",
                "Block external sharing of restricted and above",
                "Notify user of policy requirements",
            ],
            compliance_frameworks=["ISO 27001", "NIST SP 800-53"],
            severity="medium",
            tags=["confidential", "marking", "classification", "label", "restricted"],
            source_url='https://learn.microsoft.com/en-us/purview/sensitivity-labels',
            specific_blocked_actions=[
                "Block external sharing of documents marked 'Restricted' or above",
                "Enforce encryption on documents marked 'Confidential' or 'Highly Confidential'",
            ],
            specific_audit_actions=[
                'Log all access to documents with sensitivity markings for information governance',
                'Record label changes and override justifications for compliance audit',
            ],
            specific_notifications=[
                'Notify the information security team when restricted documents are shared externally',
            ],
            specific_user_experience="Users see a policy tip based on document marking: 'This document is marked Confidential/Restricted. Handling requirements apply. External sharing has been blocked or requires justification.'",
            specific_admin_experience='Information security administrators see marking-based policy violations in the DLP activity explorer. Alerts are sent based on marking severity.',
            specific_policy_tips=[
                'This document carries a sensitivity marking. Handling restrictions apply based on the classification level.',
            ],
        ),

        # ── ENDPOINT DLP (4 templates) ───────────────────────────────────────
        PolicyTemplate(
            id="endpoint_usb_blocking",
            name="Endpoint DLP – Removable Storage (USB) Blocking",
            category="Endpoint DLP",
            description=(
                "Prevents copying of sensitive data to removable storage devices such as USB "
                "drives, external hard disks, and SD cards on Windows and macOS endpoints."
            ),
            keywords=[
                "USB", "removable storage", "flash drive", "thumb drive", "external hard drive",
                "SD card", "removable media", "portable storage", "data exfiltration endpoint",
                "copy to USB", "write to external", "removable device", "portable device",
                "endpoint DLP", "device control", "storage device", "mass storage",
                "USB block", "data transfer endpoint", "BYOD storage",
            ],
            locations=["Devices"],
            sensitive_info_types=[
                "Credit Card Number", "U.S. Social Security Number (SSN)",
                "Medical Record Number", "Confidential Document Marking",
            ],
            actions=[
                "Block copy to removable storage",
                "Alert endpoint security team",
                "Audit user activity",
                "Allow with justification for approved users",
            ],
            compliance_frameworks=["ISO 27001", "NIST SP 800-53", "PCI-DSS"],
            severity="high",
            tags=["USB", "endpoint", "removable-storage", "device-control", "exfiltration"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block copy of sensitive data to USB drives, external hard disks, and SD cards on Windows/macOS endpoints',
                'Block write operations to removable storage devices for users handling PCI, HIPAA, or PII data',
            ],
            specific_audit_actions=[
                'Log all USB copy attempts including file names, user identity, and device serial number',
                'Record all removable media insertions on managed endpoints for security audit',
            ],
            specific_notifications=[
                'Alert the endpoint security team immediately when sensitive data copy to USB is attempted',
                'Notify the manager and security team when a user attempts to copy more than 10 files to USB',
            ],
            specific_user_experience="Endpoint users are blocked from copying sensitive files to USB devices and see: 'Copying sensitive data to removable storage is blocked by your organisation's DLP policy. Contact IT security if you have a legitimate business need.'",
            specific_admin_experience='Endpoint security administrators see USB blocking incidents in the DLP activity explorer and Microsoft Defender for Endpoint. Real-time alerts are sent to the security team; users with repeated violations are flagged for insider risk investigation.',
            specific_policy_tips=[
                "Copying sensitive data to USB storage is blocked by your organisation's endpoint DLP policy.",
                'Contact IT security to request an approved removable storage exception for your business use case.',
            ],
        ),
        PolicyTemplate(
            id="endpoint_print_blocking",
            name="Endpoint DLP – Print and Screenshot Restrictions",
            category="Endpoint DLP",
            description=(
                "Restricts printing of sensitive documents and screenshots on managed endpoints "
                "to prevent physical and screen-capture based data leakage."
            ),
            keywords=[
                "print restriction", "print block", "screenshot", "screen capture",
                "print sensitive", "printer control", "document printing", "hard copy",
                "print prevention", "snipping tool", "screen recording", "PrtScn",
                "endpoint print policy", "DLP print", "print audit", "printer DLP",
                "print classified", "printing confidential", "printer policy",
                "print management",
            ],
            locations=["Devices"],
            sensitive_info_types=[
                "Credit Card Number", "U.S. Social Security Number (SSN)",
                "Confidential Document Marking",
            ],
            actions=[
                "Block printing of sensitive documents",
                "Block screenshot tools",
                "Notify user",
                "Log print attempts",
            ],
            compliance_frameworks=["ISO 27001", "HIPAA", "PCI-DSS"],
            severity="medium",
            tags=["print", "screenshot", "endpoint", "DLP", "screen-capture"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block printing of sensitive documents on managed Windows and macOS endpoints',
                'Block screenshot and screen capture tools when sensitive data is displayed',
            ],
            specific_audit_actions=[
                'Log all print attempts on sensitive documents with printer name and document details',
                'Record all screen capture attempts when sensitive content is on screen',
            ],
            specific_notifications=[
                'Notify the security team when a user attempts to print or screenshot sensitive documents',
            ],
            specific_user_experience="Users are blocked from printing sensitive documents and see: 'Printing this document is blocked by your organisation's DLP policy. This document contains sensitive data that must not be reproduced in hard copy.'",
            specific_admin_experience='Endpoint security administrators see print blocking incidents in the DLP activity explorer. Alerts are sent to the security team; repeated attempts trigger insider risk review.',
            specific_policy_tips=[
                "Printing of sensitive documents is blocked by your organisation's endpoint DLP policy.",
                'If you need a printed copy for a legitimate business purpose, contact your manager for an exception.',
            ],
        ),
        PolicyTemplate(
            id="endpoint_clipboard_restrictions",
            name="Endpoint DLP – Clipboard Restrictions",
            category="Endpoint DLP",
            description=(
                "Prevents copying of sensitive data via the system clipboard to unapproved "
                "applications, reducing risk of accidental and intentional data leakage."
            ),
            keywords=[
                "clipboard", "copy paste", "clipboard restriction", "copy protection",
                "paste block", "clipboard DLP", "clipboard monitoring", "data leakage clipboard",
                "copy to unapproved app", "paste sensitive data", "clipboard exfiltration",
                "clipboard control", "copy restriction endpoint", "sensitive copy",
                "clipboard policy", "restrict clipboard", "app boundary", "data boundary",
                "clipboard audit", "copy block",
            ],
            locations=["Devices"],
            sensitive_info_types=[
                "Credit Card Number", "U.S. Social Security Number (SSN)",
                "Medical Record Number",
            ],
            actions=[
                "Block paste into unapproved applications",
                "Warn user before paste",
                "Log clipboard activity for sensitive data",
            ],
            compliance_frameworks=["ISO 27001", "HIPAA", "PCI-DSS"],
            severity="medium",
            tags=["clipboard", "copy-paste", "endpoint", "DLP", "data-boundary"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block paste of sensitive data from clipboard into unapproved applications on managed endpoints',
                'Block clipboard sharing of sensitive content across application boundaries',
            ],
            specific_audit_actions=[
                'Log all clipboard restriction events with source application and destination application context',
            ],
            specific_notifications=[
                'Notify the endpoint security team when clipboard restrictions are triggered on sensitive data',
            ],
            specific_user_experience="Endpoint users see a notification when clipboard paste is blocked: 'Pasting sensitive data into this application is blocked by your DLP policy. This restriction prevents accidental data leakage through clipboard channels.'",
            specific_admin_experience='Endpoint security administrators see clipboard restriction events in the DLP activity explorer. Daily digest alerts are sent for clipboard policy violations.',
            specific_policy_tips=[
                'Pasting sensitive data into unapproved applications is blocked by your endpoint DLP policy.',
            ],
        ),
        PolicyTemplate(
            id="endpoint_browser_upload_restrictions",
            name="Endpoint DLP – Browser Upload Restrictions",
            category="Endpoint DLP",
            description=(
                "Prevents uploading of sensitive documents and data to unapproved websites and "
                "cloud services via managed browsers on corporate endpoints."
            ),
            keywords=[
                "browser upload", "web upload", "file upload browser", "sensitive upload",
                "unauthorised cloud", "personal cloud storage", "consumer cloud",
                "browser DLP", "upload block", "upload restriction", "egress browser",
                "data leakage browser", "web DLP", "Chrome DLP", "Edge DLP",
                "browser exfiltration", "cloud upload restriction", "unapproved website",
                "browser policy", "CASB",
            ],
            locations=["Devices"],
            sensitive_info_types=[
                "Credit Card Number", "U.S. Social Security Number (SSN)",
                "Confidential Document Marking",
            ],
            actions=[
                "Block upload to unapproved sites",
                "Allow upload to approved business sites",
                "Notify user",
                "Log all browser upload attempts",
            ],
            compliance_frameworks=["ISO 27001", "NIST SP 800-53"],
            severity="medium",
            tags=["browser", "upload", "endpoint", "DLP", "cloud-egress"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block upload of sensitive files to non-approved websites and web applications from managed endpoints',
                'Block browser-based file uploads to personal cloud storage (Google Drive, Dropbox, WeTransfer)',
            ],
            specific_audit_actions=[
                'Log all browser upload attempts with website URL, file name, and sensitive data type',
                'Record all egress attempts via web browser for data exfiltration monitoring',
            ],
            specific_notifications=[
                'Alert the security team when sensitive files are uploaded to unapproved websites',
                'Notify the security operations centre when browser uploads to personal cloud storage are attempted',
            ],
            specific_user_experience="Endpoint users are blocked from uploading sensitive files via browsers and see: 'Uploading sensitive files to this website is blocked by your organisation's DLP policy. Use the approved secure file transfer portal for external file sharing.'",
            specific_admin_experience='Endpoint security administrators see browser upload blocking incidents in the DLP activity explorer and Microsoft Defender for Endpoint. Real-time alerts are sent to the security team; uploads to known exfiltration sites are escalated to the insider risk team.',
            specific_policy_tips=[
                'Uploading sensitive files to this website is blocked by your endpoint DLP policy.',
                'Use the approved secure file transfer portal for legitimate external file sharing.',
            ],
        ),

        # ── GENERAL (5 templates) ─────────────────────────────────────────────
        PolicyTemplate(
            id="general_pii_protection",
            name="General PII Detection and Protection",
            category="General",
            description=(
                "Broad personally identifiable information (PII) detection policy covering "
                "names, addresses, phone numbers, email addresses, and national ID numbers."
            ),
            keywords=[
                "PII", "personally identifiable information", "personal information",
                "full name", "email address", "phone number", "home address",
                "date of birth", "national ID", "government ID", "identity document",
                "personal details", "contact information", "demographic data",
                "biometric data", "geolocation", "IP address", "cookie identifier",
                "online identifier", "personal profile",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices", "PowerBI"],
            sensitive_info_types=[
                "Person's Name", "Email Address", "Phone Number",
                "Physical Address", "Date of Birth",
            ],
            actions=[
                "Warn user before sharing",
                "Apply PII sensitivity label",
                "Block bulk external transfer",
                "Notify privacy team",
            ],
            compliance_frameworks=["GDPR", "CCPA", "ISO 27001"],
            severity="medium",
            tags=["PII", "general", "personal-information", "privacy", "identity"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block external sharing of PII (names combined with SSN, financial account, or biometric data)',
                'Block upload of bulk PII datasets to unapproved cloud services',
            ],
            specific_audit_actions=[
                'Log all PII detections for privacy compliance and breach notification readiness',
                'Record access to PII datasets for data mapping and DPIA purposes',
            ],
            specific_notifications=[
                'Notify the privacy team when bulk PII is detected in external communications',
                'Alert the Privacy Officer for PII exposure incidents requiring breach notification assessment',
            ],
            specific_user_experience="Users see a policy tip when PII is detected: 'This content contains personally identifiable information (PII). External sharing is restricted. Use approved data handling procedures.'",
            specific_admin_experience='Privacy administrators see PII incidents in the DLP activity explorer. Alerts are sent to the privacy team; bulk PII exposure incidents are escalated for breach notification assessment under applicable privacy laws.',
            specific_policy_tips=[
                'This content contains personally identifiable information (PII). External sharing requires privacy compliance review.',
                'Bulk PII transfers must be approved by the Privacy Officer and documented for data processing records.',
            ],
        ),
        PolicyTemplate(
            id="confidential_documents_general",
            name="Confidential Documents – General Policy",
            category="General",
            description=(
                "General policy for documents labelled or containing indicators of confidential "
                "business information, enforcing appropriate handling and sharing restrictions."
            ),
            keywords=[
                "confidential document", "internal document", "sensitive document",
                "restricted document", "business confidential", "company confidential",
                "do not forward", "internal use only", "not for distribution",
                "management only", "executive", "board document", "C-suite",
                "sensitive business", "privileged document", "need to know",
                "information classification", "document control", "document handling",
                "version controlled",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=["Confidential Document Marking"],
            actions=[
                "Apply sensitivity label automatically",
                "Block external sharing without approval",
                "Notify document owner",
            ],
            compliance_frameworks=["ISO 27001"],
            severity="medium",
            tags=["confidential", "document-control", "general", "classification"],
            source_url='https://learn.microsoft.com/en-us/purview/sensitivity-labels',
            specific_blocked_actions=[
                'Block external sharing of documents labelled Confidential without authorisation',
                'Enforce encryption and access controls on all Confidential labelled documents',
            ],
            specific_audit_actions=[
                'Log all access and sharing events for confidential documents',
                'Record sensitivity label changes for information governance audit',
            ],
            specific_notifications=[
                'Notify the information security team when confidential documents are shared externally',
            ],
            specific_user_experience="Users see a policy tip when confidential documents are shared: 'This document is labelled Confidential. External sharing requires business justification and manager approval.'",
            specific_admin_experience='Information security administrators see confidential document policy violations in the DLP activity explorer. Alerts are sent to the security team; override justifications are recorded.',
            specific_policy_tips=[
                'This document is labelled Confidential. External sharing requires manager approval and a business justification.',
            ],
        ),
        PolicyTemplate(
            id="intellectual_property_general",
            name="General Intellectual Property Protection",
            category="General",
            description=(
                "Protects all forms of intellectual property including copyrights, trademarks, "
                "trade dress, and proprietary business methodologies."
            ),
            keywords=[
                "intellectual property", "IP", "copyright", "trademark", "trade dress",
                "proprietary methodology", "proprietary process", "business method",
                "copyrighted material", "all rights reserved", "registered trademark",
                "service mark", "brand guidelines", "design rights", "moral rights",
                "work for hire", "IP assignment", "IP ownership", "licensing agreement",
                "IP infringement",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=["Confidential Document Marking", "IP Document"],
            actions=[
                "Block external sharing",
                "Alert IP legal team",
                "Apply IP protection label",
            ],
            compliance_frameworks=["DMCA", "Trade Secret Law", "Copyright Law"],
            severity="medium",
            tags=["IP", "copyright", "trademark", "general", "proprietary"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block external sharing of IP-protected documents without NDA or legal approval',
                'Block upload of proprietary product and technical documentation to unapproved services',
            ],
            specific_audit_actions=[
                'Log all IP document access and disclosure events for IP portfolio protection',
            ],
            specific_notifications=[
                'Alert the legal and IP team when proprietary documentation is detected in external communications',
            ],
            specific_user_experience="Users see a policy tip: 'This document contains intellectual property. External sharing requires a signed NDA and approval from the Legal team.'",
            specific_admin_experience='Legal and IP administrators see IP protection incidents in the DLP activity explorer. Real-time alerts go to the legal team for IP exposure events.',
            specific_policy_tips=[
                'This content contains intellectual property. External sharing requires a signed NDA and legal team approval.',
            ],
        ),
        PolicyTemplate(
            id="customer_data_protection",
            name="Customer Data Protection Policy",
            category="General",
            description=(
                "Protects customer PII, account information, purchase history, and behavioural "
                "data to comply with privacy regulations and maintain customer trust."
            ),
            keywords=[
                "customer data", "customer information", "customer PII", "customer record",
                "CRM data", "account information", "purchase history", "order history",
                "customer profile", "loyalty data", "customer segment", "customer list",
                "client data", "client information", "consumer data", "customer analytics",
                "customer behaviour", "transaction data", "customer contact",
                "customer database",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices", "PowerBI"],
            sensitive_info_types=[
                "Person's Name", "Email Address", "Phone Number",
                "Credit Card Number", "Physical Address",
            ],
            actions=[
                "Block sharing outside approved systems",
                "Apply customer data label",
                "Restrict bulk exports",
                "Notify customer data steward",
            ],
            compliance_frameworks=["GDPR", "CCPA", "ISO 27001"],
            severity="medium",
            tags=["customer", "CRM", "personal-data", "consumer", "general"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block external sharing of customer personal data and contact information without data processing agreement',
                'Block export of customer databases or lists to personal cloud storage',
            ],
            specific_audit_actions=[
                'Log all customer data access and disclosure events for data processor compliance',
                'Record customer data transfers for data processing register and DPIA documentation',
            ],
            specific_notifications=[
                'Notify the Data Protection Officer when customer personal data is shared with unapproved third parties',
            ],
            specific_user_experience="Users see a policy tip when customer data is detected: 'This content contains customer personal data. Third-party sharing requires a Data Processing Agreement and DPO approval.'",
            specific_admin_experience='Privacy administrators see customer data incidents in the DLP activity explorer. Alerts are sent to the DPO; bulk customer data export attempts are escalated.',
            specific_policy_tips=[
                'This content contains customer personal data. Third-party sharing requires a Data Processing Agreement.',
            ],
        ),
        PolicyTemplate(
            id="employee_data_protection",
            name="Employee HR Data Protection Policy",
            category="General",
            description=(
                "Protects employee personnel records, payroll data, performance reviews, and "
                "sensitive HR information to comply with employment and privacy laws."
            ),
            keywords=[
                "employee data", "HR data", "personnel record", "employee file",
                "payroll", "salary information", "compensation", "performance review",
                "disciplinary record", "medical leave", "FMLA", "ADA accommodation",
                "background check", "employee ID", "benefits information",
                "W-2 form", "tax withholding", "direct deposit", "employee PII",
                "workforce data",
            ],
            locations=["Exchange", "SharePoint", "OneDrive", "Teams", "Devices"],
            sensitive_info_types=[
                "U.S. Social Security Number (SSN)", "Bank Account Number",
                "Person's Name", "Date of Birth",
            ],
            actions=[
                "Restrict to HR department only",
                "Block sharing outside HR systems",
                "Apply HR confidential label",
                "Notify HR data steward",
            ],
            compliance_frameworks=["GDPR", "CCPA", "FLSA", "Employment Law"],
            severity="medium",
            tags=["employee", "HR", "payroll", "personnel", "workforce"],
            source_url='https://learn.microsoft.com/en-us/purview/dlp-policy-reference',
            specific_blocked_actions=[
                'Block external sharing of employee personal data (SSN, salary, performance, medical) without HR approval',
                'Block export of HR records and employee data to personal or unapproved third-party systems',
            ],
            specific_audit_actions=[
                'Log all employee personal data access and disclosure events for HR compliance',
                'Record access to payroll and performance data for employment law compliance audit',
            ],
            specific_notifications=[
                'Notify the HR Director and DPO when employee personal data is shared externally',
                'Alert the CISO when bulk employee records are detected in external communications',
            ],
            specific_user_experience="Users are blocked from sharing employee personal data externally and see: 'This content contains employee personal data. External sharing is restricted under employment law and your organisation's HR data protection policy.'",
            specific_admin_experience='HR and privacy administrators see employee data incidents in the DLP activity explorer. Real-time alerts go to the HR Director and DPO; bulk HR data exposure is escalated for employment law compliance review.',
            specific_policy_tips=[
                'This content contains employee personal data. External sharing is restricted to authorised HR and legal processes.',
                'Employee data must only be shared with third parties (payroll providers, benefit administrators) under signed agreements.',
            ],
        ),
    ]

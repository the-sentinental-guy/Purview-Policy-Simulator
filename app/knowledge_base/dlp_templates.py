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
        ),
    ]

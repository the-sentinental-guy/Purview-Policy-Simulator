import re
from typing import Dict, List, Any


class NLPProcessor:
    INTENT_KEYWORDS = {
        "protect": ["protect", "prevent", "block", "stop", "restrict", "secure", "safeguard", "guard"],
        "detect": ["detect", "find", "identify", "scan", "discover", "check", "monitor", "watch"],
        "classify": ["classify", "label", "tag", "mark", "categorize", "organize"],
        "retain": ["retain", "keep", "store", "archive", "preserve", "hold", "save"],
        "monitor": ["monitor", "track", "audit", "log", "report", "alert", "observe"],
        "encrypt": ["encrypt", "scramble", "obfuscate"],
    }

    DATA_TYPE_KEYWORDS = {
        "credit_cards": ["credit card", "debit card", "card number", "cvv", "pci", "payment card", "visa", "mastercard", "amex"],
        "ssn": ["ssn", "social security", "social security number", "sin", "national id"],
        "health_records": ["health", "medical", "phi", "hipaa", "patient", "diagnosis", "prescription", "clinical", "ehr", "emr"],
        "financial_data": ["financial", "bank account", "routing number", "swift", "iban", "sox", "financial statement", "tax", "glba"],
        "pii": ["pii", "personal information", "personally identifiable", "gdpr", "ccpa", "privacy"],
        "source_code": ["source code", "code", "git", "repository", "intellectual property", "ip", "trade secret"],
        "passport": ["passport", "travel document", "border crossing"],
        "drivers_license": ["driver license", "driving licence", "driver's license"],
        "biometric": ["biometric", "fingerprint", "facial recognition", "iris scan"],
        "employee_data": ["employee", "hr data", "personnel", "payroll", "salary", "compensation"],
        "legal": ["legal", "contract", "agreement", "litigation", "attorney", "privileged"],
        "executive": ["executive", "board", "m&a", "merger", "acquisition", "confidential"],
    }

    LOCATION_KEYWORDS = {
        "email": ["email", "exchange", "outlook", "mail", "smtp"],
        "sharepoint": ["sharepoint", "share point", "sp", "document library"],
        "teams": ["teams", "microsoft teams", "chat", "channel", "meeting"],
        "onedrive": ["onedrive", "one drive", "personal storage", "my files"],
        "endpoints": ["endpoint", "device", "laptop", "desktop", "usb", "removable"],
        "cloud_apps": ["cloud app", "third party", "cloud service", "saas"],
    }

    COMPLIANCE_KEYWORDS = {
        "hipaa": ["hipaa", "health insurance portability", "phi", "covered entity"],
        "gdpr": ["gdpr", "general data protection", "eu privacy", "data subject", "right to erasure"],
        "pci_dss": ["pci", "pci dss", "payment card industry", "cardholder data"],
        "sox": ["sox", "sarbanes oxley", "sarbanes-oxley", "financial reporting"],
        "glba": ["glba", "gramm leach bliley", "financial privacy", "safeguards rule"],
        "ccpa": ["ccpa", "california consumer privacy", "california privacy"],
        "ferpa": ["ferpa", "educational records", "student data"],
        "coppa": ["coppa", "children", "child privacy", "under 13"],
        "iso27001": ["iso 27001", "iso27001", "information security management"],
        "nist": ["nist", "nist framework", "cybersecurity framework"],
    }

    RISK_SCENARIO_KEYWORDS = {
        "departing_employee": ["departing", "leaving", "resign", "termination", "offboard", "exit"],
        "insider_threat": ["insider", "internal threat", "malicious insider", "rogue"],
        "data_leak": ["leak", "exfiltration", "data loss", "dlp", "leakage"],
        "privilege_abuse": ["privilege", "admin abuse", "unauthorized access"],
        "accidental_share": ["accidental", "mistaken", "wrong recipient", "misdirected"],
    }

    def process(self, query: str) -> Dict[str, Any]:
        query_lower = query.lower()

        intents = [intent for intent, kws in self.INTENT_KEYWORDS.items()
                   if any(kw in query_lower for kw in kws)]
        if not intents:
            intents = ["protect"]

        data_types = [dt for dt, kws in self.DATA_TYPE_KEYWORDS.items()
                      if any(kw in query_lower for kw in kws)]

        locations = [loc for loc, kws in self.LOCATION_KEYWORDS.items()
                     if any(kw in query_lower for kw in kws)]

        compliance = [comp for comp, kws in self.COMPLIANCE_KEYWORDS.items()
                      if any(kw in query_lower for kw in kws)]

        risk_scenarios = [rs for rs, kws in self.RISK_SCENARIO_KEYWORDS.items()
                          if any(kw in query_lower for kw in kws)]

        stop_words = {"the", "a", "an", "in", "on", "for", "of", "with", "to", "from", "and", "or", "is", "are", "be"}
        words = re.findall(r'\b[a-z]{3,}\b', query_lower)
        keywords = [w for w in words if w not in stop_words]

        return {
            "intent": intents,
            "data_types": data_types,
            "locations": locations,
            "compliance": compliance,
            "risk_scenarios": risk_scenarios,
            "keywords": keywords,
        }

DOCUMENTATION_REFS = {
    "Financial": [
        {
            "title": "DLP Financial Data Protection",
            "url": "https://learn.microsoft.com/en-us/microsoft-365/compliance/dlp-policy-reference",
            "description": "DLP policy reference for financial data",
        },
        {
            "title": "PCI DSS Compliance in Microsoft 365",
            "url": "https://learn.microsoft.com/en-us/compliance/regulatory/offering-pci-dss",
            "description": "PCI DSS compliance offering details",
        },
        {
            "title": "SOX Compliance in Microsoft 365",
            "url": "https://learn.microsoft.com/en-us/compliance/regulatory/offering-sox",
            "description": "SOX compliance overview",
        },
    ],
    "Healthcare": [
        {
            "title": "HIPAA in Microsoft 365",
            "url": "https://learn.microsoft.com/en-us/compliance/regulatory/offering-hipaa-hitech",
            "description": "HIPAA compliance guidance",
        },
        {
            "title": "Healthcare DLP Templates",
            "url": "https://learn.microsoft.com/en-us/microsoft-365/compliance/dlp-policy-reference#healthcare",
            "description": "Healthcare-specific DLP templates",
        },
    ],
    "Privacy/PII": [
        {
            "title": "GDPR Compliance",
            "url": "https://learn.microsoft.com/en-us/compliance/regulatory/gdpr",
            "description": "GDPR compliance in Microsoft services",
        },
        {
            "title": "CCPA Compliance",
            "url": "https://learn.microsoft.com/en-us/compliance/regulatory/offering-ccpa",
            "description": "California Consumer Privacy Act compliance",
        },
        {
            "title": "Sensitive Information Types Reference",
            "url": "https://learn.microsoft.com/en-us/microsoft-365/compliance/sensitive-information-type-entity-definitions",
            "description": "Full catalog of built-in SITs",
        },
    ],
    "Regional Compliance": [
        {
            "title": "Global Compliance Offerings",
            "url": "https://learn.microsoft.com/en-us/compliance/regulatory/offering-home",
            "description": "Microsoft compliance offerings by regulation",
        },
        {
            "title": "GDPR Resource Center",
            "url": "https://learn.microsoft.com/en-us/compliance/regulatory/gdpr",
            "description": "GDPR compliance resources",
        },
    ],
    "Intellectual Property": [
        {
            "title": "Protecting Sensitive Data with DLP",
            "url": "https://learn.microsoft.com/en-us/microsoft-365/compliance/dlp-learn-about-dlp",
            "description": "DLP overview for IP protection",
        },
        {
            "title": "Insider Risk Management",
            "url": "https://learn.microsoft.com/en-us/microsoft-365/compliance/insider-risk-management",
            "description": "Protect IP from insider threats",
        },
    ],
    "General": [
        {
            "title": "Get started with DLP",
            "url": "https://learn.microsoft.com/en-us/microsoft-365/compliance/get-started-with-dlp-policy-recommendations",
            "description": "DLP getting started guide",
        },
        {
            "title": "DLP Policy Reference",
            "url": "https://learn.microsoft.com/en-us/microsoft-365/compliance/dlp-policy-reference",
            "description": "Complete DLP policy reference",
        },
        {
            "title": "Insider Risk Management",
            "url": "https://learn.microsoft.com/en-us/microsoft-365/compliance/insider-risk-management",
            "description": "Insider risk management overview",
        },
        {
            "title": "Sensitivity Labels",
            "url": "https://learn.microsoft.com/en-us/microsoft-365/compliance/sensitivity-labels",
            "description": "Sensitivity labels overview and setup",
        },
    ],
}


def get_docs_for_category(category: str) -> list:
    """Return documentation references for the given policy category."""
    refs = DOCUMENTATION_REFS.get(category, DOCUMENTATION_REFS["General"])
    return [
        {
            "title": r["title"],
            "url": r["url"],
            "description": r["description"],
            "source": "Microsoft Learn",
        }
        for r in refs
    ]

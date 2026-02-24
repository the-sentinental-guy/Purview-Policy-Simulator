PURVIEW_ARCHITECTURE = {
    "compliance_portal": {
        "name": "Microsoft Purview Compliance Portal",
        "url": "https://compliance.microsoft.com",
        "description": "Central management hub for all Microsoft Purview compliance solutions",
        "components": [
            "DLP",
            "Information Protection",
            "Data Lifecycle Management",
            "Insider Risk Management",
            "eDiscovery",
            "Audit",
            "Communication Compliance",
        ],
    },
    "dlp_platform": {
        "name": "Data Loss Prevention Platform",
        "description": "Cross-workload DLP enforcement engine",
        "workloads": {
            "Exchange": "Email and calendar protection via transport rules",
            "SharePoint": "Document protection at rest and in motion",
            "OneDrive": "Personal file storage protection",
            "Teams": "Chat and channel message protection",
            "Endpoints": "Device-level activity monitoring via MDE",
            "Cloud Apps": "CASB-based third-party app protection",
        },
    },
    "information_protection": {
        "name": "Microsoft Purview Information Protection",
        "components": {
            "sensitivity_labels": "Classification and protection labels",
            "label_policies": "Publishing labels to users and apps",
            "auto_labeling": "Automatic label application based on content",
            "aip_scanner": "On-premises file scanning and labeling",
        },
    },
    "insider_risk": {
        "name": "Microsoft Purview Insider Risk Management",
        "description": "Intelligent risk detection for internal threats",
        "data_sources": [
            "Microsoft 365 activity",
            "HR connectors",
            "Microsoft Defender signals",
            "Communication Compliance signals",
        ],
    },
    "data_lifecycle": {
        "name": "Microsoft Purview Data Lifecycle Management",
        "description": "Retention and disposition of organizational data",
        "components": {
            "retention_policies": "Org-wide or location-specific retention",
            "retention_labels": "Item-level retention with record management",
            "disposition_review": "Human review before content deletion",
            "records_management": "Immutable records for regulatory compliance",
        },
    },
    "ediscovery": {
        "name": "Microsoft Purview eDiscovery",
        "tiers": {
            "content_search": "Basic search across M365 workloads (E3)",
            "ediscovery_standard": "Case management and hold (E3)",
            "ediscovery_premium": "Advanced analytics, custodians, review sets (E5)",
        },
    },
}

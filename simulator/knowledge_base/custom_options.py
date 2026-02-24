LOCATION_OPTIONS = {
    "Exchange": {
        "description": "Email and calendar items in Exchange Online",
        "license_required": "Microsoft 365 E3+",
    },
    "SharePoint": {
        "description": "Files and content in SharePoint Online",
        "license_required": "Microsoft 365 E3+",
    },
    "OneDrive": {
        "description": "Files in OneDrive for Business",
        "license_required": "Microsoft 365 E3+",
    },
    "Teams": {
        "description": "Messages in Microsoft Teams",
        "license_required": "Microsoft 365 E5 Compliance",
    },
    "Endpoints": {
        "description": "Files on Windows 10/11 endpoints via MDE",
        "license_required": "Microsoft 365 E5 or MDE P2",
    },
    "Cloud Apps": {
        "description": "Third-party cloud apps connected to Defender for Cloud Apps",
        "license_required": "Microsoft 365 E5 Security",
    },
    "On-premises repositories": {
        "description": "On-premises file shares and SharePoint",
        "license_required": "AIP Scanner",
    },
    "Power BI": {
        "description": "Power BI workspaces and reports",
        "license_required": "Microsoft 365 E5 Compliance",
    },
}

CONDITION_OPERATORS = [
    "contains",
    "does not contain",
    "matches",
    "does not match",
    "is",
    "is not",
    "starts with",
    "ends with",
]

EXCEPTION_TYPES = [
    "Sender is",
    "Sender domain is",
    "Recipient is",
    "Recipient domain is",
    "Document property is",
    "Document is password protected",
    "Document size is",
    "Content is not labeled",
    "Sender IP range is",
    "Subject contains words",
]

VOLUME_THRESHOLDS = {
    "Low sensitivity": {"min_count": 5, "description": "5 or more instances"},
    "Medium sensitivity": {"min_count": 3, "description": "3 or more instances"},
    "High sensitivity": {"min_count": 1, "description": "Any single instance"},
    "Custom": {"min_count": None, "description": "Configurable threshold"},
}

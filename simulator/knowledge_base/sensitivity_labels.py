SENSITIVITY_LABELS = [
    {
        "name": "Public",
        "description": "Content intended for public consumption. No restrictions apply.",
        "encryption": {"enabled": False},
        "content_marking": {"header": None, "footer": None, "watermark": None},
        "auto_labeling": {"enabled": False},
        "color": "#107C10",
        "priority": 0,
        "sublabels": [],
    },
    {
        "name": "General",
        "description": "Non-public information for internal use. Not sensitive but not public.",
        "encryption": {"enabled": False},
        "content_marking": {"header": "GENERAL", "footer": None, "watermark": None},
        "auto_labeling": {"enabled": False},
        "color": "#0078D4",
        "priority": 1,
        "sublabels": [],
    },
    {
        "name": "Confidential",
        "description": "Business-sensitive information. Restricted to authorized users.",
        "encryption": {"enabled": True, "permissions": ["View", "Edit", "Print"]},
        "content_marking": {
            "header": "CONFIDENTIAL",
            "footer": "CONFIDENTIAL - Do not distribute",
            "watermark": "CONFIDENTIAL",
        },
        "auto_labeling": {
            "enabled": True,
            "conditions": ["Credit Card Number", "SSN", "Bank Account"],
        },
        "color": "#FF8C00",
        "priority": 2,
        "sublabels": [
            {"name": "Confidential - Finance", "description": "Financial data restricted to Finance team"},
            {"name": "Confidential - HR", "description": "HR data restricted to HR team"},
            {"name": "Confidential - Legal", "description": "Legal documents restricted to Legal team"},
        ],
    },
    {
        "name": "Highly Confidential",
        "description": "Most sensitive information. Strictly controlled access.",
        "encryption": {
            "enabled": True,
            "permissions": ["View"],
            "do_not_forward": True,
            "no_print": True,
        },
        "content_marking": {
            "header": "HIGHLY CONFIDENTIAL",
            "footer": "HIGHLY CONFIDENTIAL - Authorized access only",
            "watermark": "HIGHLY CONFIDENTIAL",
        },
        "auto_labeling": {
            "enabled": True,
            "conditions": ["PHI", "PCI", "Trade Secret", "M&A"],
        },
        "color": "#D13438",
        "priority": 3,
        "sublabels": [
            {
                "name": "Highly Confidential - Executive",
                "description": "Executive communications and board materials",
            },
            {
                "name": "Highly Confidential - Legal Hold",
                "description": "Legal hold materials",
            },
            {
                "name": "Highly Confidential - Mergers & Acquisitions",
                "description": "M&A sensitive data",
            },
        ],
    },
]

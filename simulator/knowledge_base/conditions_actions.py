DLP_CONDITIONS = [
    {
        "name": "Content contains sensitive info type",
        "description": "Match based on built-in or custom sensitive information types",
    },
    {
        "name": "Content is shared",
        "description": "Detect when content is shared inside or outside organization",
    },
    {"name": "Sender is", "description": "Match based on sender identity"},
    {"name": "Recipient is", "description": "Match based on recipient identity"},
    {"name": "Sender domain is", "description": "Match based on sender email domain"},
    {
        "name": "Document property is",
        "description": "Match based on SharePoint document metadata",
    },
    {
        "name": "Content is labeled",
        "description": "Match content with specific sensitivity labels",
    },
    {
        "name": "Document size is",
        "description": "Match documents above/below size threshold",
    },
    {
        "name": "Document name contains",
        "description": "Match on document name patterns",
    },
    {
        "name": "Message type is",
        "description": "Match on email message type (mail, calendar, etc.)",
    },
    {
        "name": "Content contains words or phrases",
        "description": "Match on specific keywords in content",
    },
    {
        "name": "Attachment file extension is",
        "description": "Match on file attachment types",
    },
    {
        "name": "Recipient count exceeds",
        "description": "Match when email has too many recipients",
    },
    {
        "name": "Sender IP address is in range",
        "description": "Match based on sender IP address",
    },
    {
        "name": "Any email attachment is password protected",
        "description": "Match password-protected attachments",
    },
]

DLP_ACTIONS = [
    {
        "name": "Block access to content",
        "description": "Prevent users from accessing the content",
        "scope": ["SharePoint", "OneDrive"],
    },
    {
        "name": "Block everyone except the content owner",
        "description": "Restrict access to content owner only",
    },
    {
        "name": "Send incident report",
        "description": "Generate and send incident report to compliance team",
    },
    {
        "name": "Notify user with policy tip",
        "description": "Show policy tip in Office applications",
    },
    {
        "name": "Send email notification",
        "description": "Send email to user explaining the policy violation",
    },
    {
        "name": "Restrict third party app access",
        "description": "Block cloud app access to protected content",
    },
    {
        "name": "Apply encryption",
        "description": "Apply RMS encryption/IRM protection to content",
    },
    {
        "name": "Apply sensitivity label",
        "description": "Auto-apply sensitivity label to matched content",
    },
    {
        "name": "Block activity on endpoint",
        "description": "Block copy, print, USB transfer on endpoints",
    },
    {
        "name": "Audit only",
        "description": "Log the activity without blocking - useful for testing",
    },
    {
        "name": "Allow override with justification",
        "description": "Allow user to override with business justification",
    },
    {
        "name": "Allow override with false positive claim",
        "description": "Allow user to mark as false positive",
    },
    {
        "name": "Quarantine email",
        "description": "Move email to quarantine for review",
    },
    {
        "name": "Add header to email",
        "description": "Add X-header to flagged email messages",
    },
]

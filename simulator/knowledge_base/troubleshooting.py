TROUBLESHOOTING_GUIDE = [
    {
        "issue_id": "ts-001",
        "title": "Policy Not Triggering",
        "description": "DLP policy is configured but not detecting or blocking sensitive content",
        "symptoms": [
            "No incidents in DLP reports",
            "Content is being shared without policy tip",
            "No alerts generated",
        ],
        "common_causes": [
            "Policy is in simulation mode (test mode)",
            "Policy sync delay (can take up to 24 hours)",
            "Incorrect sensitive information type configuration",
            "Content count threshold too high",
            "Exceptions are too broadly configured",
        ],
        "resolution_steps": [
            "1. Check policy mode - ensure it's set to 'Turn on' not 'Test'",
            "2. Wait 24 hours for full policy synchronization",
            "3. Use DLP policy match test in compliance portal",
            "4. Review SIT confidence level and count thresholds",
            "5. Check for conflicting exceptions",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/microsoft-365/compliance/dlp-policy-troubleshooting"
        ],
    },
    {
        "issue_id": "ts-002",
        "title": "High False Positive Rate",
        "description": "Policy is generating too many false positive alerts on legitimate content",
        "symptoms": [
            "Users reporting legitimate work being blocked",
            "High volume of override requests",
            "Business disruption",
        ],
        "common_causes": [
            "Confidence level set too low",
            "Content count threshold too low (e.g., 1 instance)",
            "Overly broad sensitive information types",
            "Missing exception rules for authorized users",
        ],
        "resolution_steps": [
            "1. Increase minimum instance count (e.g., from 1 to 5)",
            "2. Increase confidence level threshold to High",
            "3. Add exceptions for specific user groups (Finance, Legal)",
            "4. Review and narrow sensitive information type definitions",
            "5. Use Activity Explorer to analyze false positive patterns",
            "6. Consider using 'Allow override with justification' instead of hard block",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/microsoft-365/compliance/dlp-configure-view-alerts-policies"
        ],
    },
    {
        "issue_id": "ts-003",
        "title": "Teams DLP Not Working",
        "description": "DLP policy is not applying to Microsoft Teams messages",
        "symptoms": [
            "Sensitive content shared in Teams without policy tip",
            "No Teams-related incidents",
        ],
        "common_causes": [
            "Missing Microsoft 365 E5 Compliance license",
            "Teams not included in policy scope",
            "Policy sync delay for Teams",
            "Teams DLP requires separate configuration",
        ],
        "resolution_steps": [
            "1. Verify Microsoft 365 E5 Compliance or Teams DLP add-on license",
            "2. Edit policy to include Teams as a location",
            "3. Ensure policy includes both channel messages and chats",
            "4. Wait up to 24 hours for Teams policy sync",
            "5. Test with a pilot group first",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/microsoft-365/compliance/dlp-microsoft-teams"
        ],
    },
    {
        "issue_id": "ts-004",
        "title": "Endpoint DLP Not Triggering",
        "description": "Endpoint DLP policy not detecting activities on Windows devices",
        "symptoms": [
            "USB transfers not blocked",
            "No endpoint DLP alerts",
            "Policy tip not shown on endpoint",
        ],
        "common_causes": [
            "Microsoft Defender for Endpoint not deployed",
            "Device not onboarded to MDE",
            "Missing Microsoft 365 E5 license",
            "Windows version too old (requires Windows 10 1809+)",
        ],
        "resolution_steps": [
            "1. Verify MDE deployment and device onboarding status",
            "2. Check Windows version compatibility (10 1809 or later)",
            "3. Verify Microsoft 365 E5 or MDE P2 license assignment",
            "4. Check DLP endpoint settings in Compliance portal",
            "5. Review MDE device health reports",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/microsoft-365/compliance/endpoint-dlp-getting-started"
        ],
    },
    {
        "issue_id": "ts-005",
        "title": "Sensitivity Label Not Auto-Applying",
        "description": "Auto-labeling policy not automatically applying sensitivity labels",
        "symptoms": [
            "Documents not labeled automatically",
            "Auto-labeling simulation shows matches but not applied",
        ],
        "common_causes": [
            "Auto-labeling policy still in simulation mode",
            "License requirement not met (requires AIP P2)",
            "Conflicting manual labels taking precedence",
            "SharePoint timer job delay",
        ],
        "resolution_steps": [
            "1. Switch auto-labeling policy from simulation to enforce mode",
            "2. Verify Azure Information Protection P2 license",
            "3. Check label priority settings",
            "4. Allow 24-48 hours for auto-labeling to process existing content",
            "5. Check SharePoint information management policy settings",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/microsoft-365/compliance/apply-sensitivity-label-automatically"
        ],
    },
    {
        "issue_id": "ts-006",
        "title": "Policy Tip Not Showing in Office Apps",
        "description": "DLP policy tip not appearing in Word, Excel, Outlook, or other Office applications",
        "symptoms": [
            "No policy tip shown when typing sensitive content in Office apps",
            "Policy working on SharePoint but not in desktop Office client",
        ],
        "common_causes": [
            "Office client version too old (requires Office 2016+)",
            "Policy tip configuration missing",
            "User not in policy scope",
            "Sensitivity label overriding DLP tip",
        ],
        "resolution_steps": [
            "1. Verify Office client version is 2016 or later",
            "2. Enable 'Show policy tip as notification' in policy rule",
            "3. Confirm user is within the policy scope",
            "4. Check for sensitivity label policy tip conflicts",
            "5. Clear Office credential cache and retry",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/microsoft-365/compliance/dlp-policy-tips-reference"
        ],
    },
    {
        "issue_id": "ts-007",
        "title": "Incident Reports Not Being Received",
        "description": "DLP incidents are generated but email notifications not received by admins",
        "symptoms": [
            "Incidents visible in Compliance portal but no email",
            "Admins not receiving alert emails",
        ],
        "common_causes": [
            "Notification email address misconfigured",
            "Email blocked by spam filters",
            "Alert policy not configured correctly",
            "Notification throttling",
        ],
        "resolution_steps": [
            "1. Verify notification email addresses in policy rule",
            "2. Check spam/junk folder for compliance@company.com",
            "3. Add compliance notification addresses to safe senders list",
            "4. Configure DLP alert policy in Microsoft Purview alerts",
            "5. Review notification throttling settings",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/microsoft-365/compliance/dlp-alerts-dashboard-get-started"
        ],
    },
    {
        "issue_id": "ts-008",
        "title": "DLP Policy Priority Conflicts",
        "description": "Multiple DLP policies conflicting or unexpected policy applying",
        "symptoms": [
            "Wrong policy applying to content",
            "Policy override not working as expected",
            "Conflicting policy tips shown",
        ],
        "common_causes": [
            "Lower priority policy number (higher priority) conflicting",
            "More specific policy not taking precedence",
            "Policy scope overlap",
        ],
        "resolution_steps": [
            "1. Review policy priority numbers (lower number = higher priority)",
            "2. Reorder policies to put most specific policies at top (lower priority number)",
            "3. Use policy conditions to narrow scope and reduce conflicts",
            "4. Test with Activity Explorer to trace which policy applied",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/microsoft-365/compliance/dlp-policy-reference#policy-priority"
        ],
    },
    {
        "issue_id": "ts-009",
        "title": "On-Premises DLP Scanner Issues",
        "description": "AIP scanner or on-premises DLP not scanning files in file shares",
        "symptoms": [
            "On-premises files not being classified",
            "Scanner job errors in admin portal",
        ],
        "common_causes": [
            "AIP Scanner service account permission issues",
            "Scanner not installed or misconfigured",
            "Network connectivity to Azure AD",
            "Certificate or authentication issues",
        ],
        "resolution_steps": [
            "1. Verify AIP Scanner service account has read access to file shares",
            "2. Check scanner logs in Event Viewer",
            "3. Re-run scanner authentication with Set-AIPAuthentication",
            "4. Verify network connectivity to Azure AD endpoints",
            "5. Update AIP Scanner to latest version",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/azure/information-protection/deploy-aip-scanner"
        ],
    },
    {
        "issue_id": "ts-010",
        "title": "Custom Sensitive Info Type Not Matching",
        "description": "Custom SIT created but not detecting the intended content patterns",
        "symptoms": [
            "Custom SIT shows no matches in Content Explorer",
            "Policy tip not showing for custom SIT",
        ],
        "common_causes": [
            "Regex pattern error or too restrictive",
            "Missing keyword corroboration",
            "Confidence level set too high",
            "Pattern not accounting for variations",
        ],
        "resolution_steps": [
            "1. Test regex pattern using regex tester tools",
            "2. Add keyword validators to improve accuracy",
            "3. Lower confidence level and test",
            "4. Use the 'Test' feature in SIT editor to validate",
            "5. Check for special character escaping in regex",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/microsoft-365/compliance/sit-create-edm-sit-classic-ux-workflow"
        ],
    },
    {
        "issue_id": "ts-011",
        "title": "DLP Override Audit Logs Missing",
        "description": "User overrides of DLP policies not appearing in audit logs",
        "symptoms": [
            "Users claiming they overrode policy but no log entry",
            "Override audit trail incomplete",
        ],
        "common_causes": [
            "Audit logging not enabled",
            "Audit log retention period expired",
            "Override logging not configured in policy",
        ],
        "resolution_steps": [
            "1. Verify audit logging is enabled in Microsoft Purview",
            "2. Check audit log retention policy (default 90 days)",
            "3. Search Audit log for DLPRuleUndo events",
            "4. Enable advanced audit (requires E5 license)",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/microsoft-365/compliance/audit-solutions-overview"
        ],
    },
    {
        "issue_id": "ts-012",
        "title": "Email Encryption Not Applying",
        "description": "DLP policy action to encrypt email not applying encryption to messages",
        "symptoms": [
            "Sensitive emails sent without encryption",
            "Recipients not seeing encrypted email notification",
        ],
        "common_causes": [
            "Azure Information Protection P1/P2 license missing",
            "OME (Office Message Encryption) not configured",
            "Transport rule conflicting",
            "Email client compatibility issue",
        ],
        "resolution_steps": [
            "1. Verify Azure Information Protection or M365 E5 license",
            "2. Configure Office Message Encryption in Admin portal",
            "3. Check for conflicting Exchange transport rules",
            "4. Test with Test-IRMConfiguration PowerShell cmdlet",
            "5. Verify MX records and mail flow configuration",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/microsoft-365/compliance/ome-sensitive-information-types"
        ],
    },
    {
        "issue_id": "ts-013",
        "title": "SharePoint DLP Performance Impact",
        "description": "SharePoint site experiencing slowness after DLP policy deployment",
        "symptoms": [
            "Document uploads slower than usual",
            "Search indexing delays",
            "User complaints about SharePoint performance",
        ],
        "common_causes": [
            "DLP scanning all documents in large libraries",
            "High-traffic site with many simultaneous uploads",
            "Complex SIT patterns with heavy regex",
        ],
        "resolution_steps": [
            "1. Scope DLP policy to specific site collections rather than all SharePoint",
            "2. Simplify complex regex patterns in custom SITs",
            "3. Stagger DLP policy rollout across sites",
            "4. Monitor SharePoint health dashboard for throttling",
            "5. Consider excluding high-volume archive libraries from DLP scope",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/microsoft-365/compliance/dlp-learn-about-dlp#sharepoint-online-and-onedrive-for-business"
        ],
    },
    {
        "issue_id": "ts-014",
        "title": "DLP and External Sharing Settings Conflict",
        "description": "DLP block policy not effective due to SharePoint external sharing settings",
        "symptoms": [
            "External users still accessing files despite DLP block",
            "Sharing links created before DLP policy still working",
        ],
        "common_causes": [
            "Pre-existing sharing links not invalidated",
            "SharePoint admin external sharing settings override DLP",
            "Guest access not restricted at tenant level",
        ],
        "resolution_steps": [
            "1. Review SharePoint tenant external sharing settings in Admin Center",
            "2. Revoke existing sharing links for affected content",
            "3. Configure SharePoint external sharing to 'New and existing guests'",
            "4. Use Conditional Access policies to restrict guest access",
            "5. Enable SharePoint Advanced Management for link expiration",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/sharepoint/external-sharing-overview"
        ],
    },
    {
        "issue_id": "ts-015",
        "title": "Power BI DLP Configuration Issues",
        "description": "DLP policies not applying to Power BI workspace content",
        "symptoms": [
            "Sensitive data in Power BI reports not flagged",
            "No DLP incidents from Power BI",
        ],
        "common_causes": [
            "Microsoft 365 E5 Compliance license not assigned",
            "Power BI DLP not enabled in compliance portal",
            "Power BI workspace not in policy scope",
        ],
        "resolution_steps": [
            "1. Verify Microsoft 365 E5 Compliance license",
            "2. Enable Power BI as a location in DLP policy",
            "3. Ensure Power BI admin settings allow DLP integration",
            "4. Check Power BI workspace classification settings",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/power-bi/enterprise/service-security-dlp-policies-for-power-bi"
        ],
    },
    {
        "issue_id": "ts-016",
        "title": "Compliance Score DLP Recommendations Not Updating",
        "description": "Microsoft Compliance Score not reflecting DLP policy improvements",
        "symptoms": [
            "Compliance score unchanged after implementing DLP policies",
            "DLP improvement actions still showing as incomplete",
        ],
        "common_causes": [
            "Score refresh delay (up to 24 hours)",
            "Policy not meeting minimum score criteria",
            "Assessment template outdated",
        ],
        "resolution_steps": [
            "1. Wait 24 hours for compliance score to refresh",
            "2. Verify DLP policy meets the specific control requirements",
            "3. Manually mark improvement actions as implemented if automated detection fails",
            "4. Review the specific control mapping in Compliance Manager",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/microsoft-365/compliance/compliance-manager-improvement-actions"
        ],
    },
    {
        "issue_id": "ts-017",
        "title": "DLP Simulation vs Enforce Mode Differences",
        "description": "Policy behaves differently between simulation mode and enforce mode",
        "symptoms": [
            "Simulation mode shows different matches than enforce mode",
            "Unexpected blocking after switching to enforce mode",
        ],
        "common_causes": [
            "Simulation mode doesn't block, only logs",
            "Time-based factors affecting content at enforcement time",
            "Policy tips only show in enforce mode for users",
        ],
        "resolution_steps": [
            "1. Review Activity Explorer data from simulation mode to predict impact",
            "2. Communicate to users before switching to enforce mode",
            "3. Start with notify-only in enforce mode before adding block actions",
            "4. Configure appropriate exception groups before enforcing",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/microsoft-365/compliance/dlp-test-dlp-policies"
        ],
    },
    {
        "issue_id": "ts-018",
        "title": "Multi-Geo DLP Policy Deployment",
        "description": "DLP policies not applying correctly in Microsoft 365 Multi-Geo environments",
        "symptoms": [
            "DLP not applying in satellite geo locations",
            "Policy shows only applied to primary geo",
        ],
        "common_causes": [
            "Multi-Geo DLP requires separate policy configuration per geo",
            "Compliance portal geo selection issue",
            "Data residency requirements affecting policy scope",
        ],
        "resolution_steps": [
            "1. Create separate DLP policies for each geo location",
            "2. Use the geo-specific compliance portal URLs",
            "3. Verify data residency requirements for each geo",
            "4. Contact Microsoft Support for Multi-Geo DLP guidance",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/microsoft-365/enterprise/multi-geo-capabilities-in-onedrive-and-sharepoint-online-in-microsoft-365"
        ],
    },
    {
        "issue_id": "ts-019",
        "title": "DLP and Azure AD Conditional Access Interaction",
        "description": "Conditional Access policies interacting unexpectedly with DLP enforcement",
        "symptoms": [
            "Users being double-blocked by CA and DLP",
            "DLP exceptions not working for CA-blocked users",
        ],
        "common_causes": [
            "CA blocking access before DLP can evaluate",
            "Unmanaged device CA policy preventing DLP policy tip display",
            "Session policies in Defender for Cloud Apps conflicting",
        ],
        "resolution_steps": [
            "1. Map the order of CA and DLP policy evaluation",
            "2. Ensure managed device CA policies allow DLP policy tip rendering",
            "3. Configure Defender for Cloud Apps session policies to complement DLP",
            "4. Test scenarios with and without CA policies",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/microsoft-365/compliance/dlp-conditions-and-exceptions"
        ],
    },
    {
        "issue_id": "ts-020",
        "title": "Custom Trainable Classifier Accuracy Issues",
        "description": "Trainable classifier used in DLP policy producing inaccurate results",
        "symptoms": [
            "High false positive rate with trainable classifier",
            "Classifier not detecting intended document types",
        ],
        "common_causes": [
            "Insufficient training samples (need 50+ positive, 50+ negative)",
            "Training data not representative of production data",
            "Classifier needs retraining after content changes",
            "Pre-built classifier not matching custom content",
        ],
        "resolution_steps": [
            "1. Add more diverse training samples (minimum 200 recommended)",
            "2. Review and improve negative sample quality",
            "3. Publish and test classifier before production use",
            "4. Use feedback mechanism to retrain classifier",
            "5. Consider combining classifier with SIT for better precision",
        ],
        "references": [
            "https://learn.microsoft.com/en-us/microsoft-365/compliance/classifier-learn-about"
        ],
    },
]

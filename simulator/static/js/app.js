/* Purview Policy Simulator – app.js */
'use strict';

// ─── State ──────────────────────────────────────────────
let isLoading = false;

// ─── DOM References ──────────────────────────────────────
const queryInput    = document.getElementById('queryInput');
const submitBtn     = document.getElementById('submitBtn');
const btnText       = document.getElementById('btnText');
const btnSpinner    = document.getElementById('btnSpinner');
const contentArea   = document.getElementById('contentArea');
const welcomeScreen = document.getElementById('welcomeScreen');
const resultsContainer = document.getElementById('resultsContainer');
const mcpToggle     = document.getElementById('mcpToggle');
const errorToast    = document.getElementById('errorToast');

// ─── Keyboard handler ────────────────────────────────────
function handleKeydown(event) {
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        event.preventDefault();
        submitQuery();
    }
}

// ─── Set query from sidebar / chip ───────────────────────
function setQuery(text) {
    queryInput.value = text;
    queryInput.focus();
}

// ─── Submit query ─────────────────────────────────────────
async function submitQuery() {
    const query = queryInput.value.trim();
    if (!query) {
        showError('Please enter a query before submitting.');
        return;
    }
    if (isLoading) return;

    setLoadingState(true);
    hideError();

    // Show loading indicator
    welcomeScreen.classList.add('hidden');
    resultsContainer.classList.add('hidden');
    contentArea.innerHTML = buildLoadingHTML(query);

    try {
        const response = await fetch('/simulate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: query,
                mcp_enabled: mcpToggle.checked,
            }),
        });

        if (!response.ok) {
            const err = await response.json().catch(() => ({}));
            throw new Error(err.detail || `Server error: ${response.status}`);
        }

        const data = await response.json();
        renderResults(data);
    } catch (err) {
        showError(`Error: ${err.message}`);
        contentArea.innerHTML = '';
        welcomeScreen.classList.remove('hidden');
    } finally {
        setLoadingState(false);
    }
}

// ─── Build loading HTML ───────────────────────────────────
function buildLoadingHTML(query) {
    return `
        <div class="loading-screen">
            <div class="loading-spinner"></div>
            <p class="loading-text">Analyzing: <strong>${escapeHtml(query)}</strong></p>
        </div>`;
}

// ─── Render results ───────────────────────────────────────
function renderResults(data) {
    contentArea.innerHTML = '';

    const container = document.createElement('div');
    container.className = 'results-container';

    // Summary banner
    const summary = document.createElement('div');
    summary.className = 'summary-banner';
    summary.innerHTML = `
        <h3>Simulation Summary</h3>
        <p>${formatMarkdown(escapeHtml(data.summary))}</p>`;
    container.appendChild(summary);

    // NLP Analysis
    if (data.nlp_analysis) {
        container.appendChild(buildNLPBanner(data.nlp_analysis));
    }

    // Template matches
    if (!data.matches || data.matches.length === 0) {
        const noResults = document.createElement('div');
        noResults.className = 'summary-banner';
        noResults.innerHTML = '<h3>No Matches</h3><p>No matching policy templates found. Try a more specific query.</p>';
        container.appendChild(noResults);
    } else {
        data.matches.forEach((match, index) => {
            container.appendChild(buildMatchCard(match, index, data.mcp_references));
        });
    }

    contentArea.appendChild(container);
}

// ─── NLP Analysis Banner ──────────────────────────────────
function buildNLPBanner(nlp) {
    const div = document.createElement('div');
    div.className = 'nlp-analysis';

    const groups = [
        { label: 'Intent',      items: nlp.intent      || [] },
        { label: 'Data Types',  items: nlp.data_types  || [] },
        { label: 'Locations',   items: nlp.locations   || [] },
        { label: 'Compliance',  items: nlp.compliance  || [] },
    ];

    groups.forEach(({ label, items }) => {
        if (items.length === 0) return;
        const g = document.createElement('div');
        g.className = 'nlp-group';
        g.innerHTML = `<span class="nlp-label">${escapeHtml(label)}:</span>`;
        items.forEach(item => {
            g.innerHTML += `<span class="nlp-tag">${escapeHtml(item.replace(/_/g, ' '))}</span>`;
        });
        div.appendChild(g);
    });

    return div;
}

// ─── Match Card ───────────────────────────────────────────
function buildMatchCard(match, index, mcpRefs) {
    const card = document.createElement('div');
    card.className = 'result-card';

    const tmpl    = match.template || {};
    const effects = match.effects  || {};
    const level   = match.confidence_level || 'LOW';
    const score   = (match.confidence_score * 100).toFixed(0);
    const cardId  = `card-${index}`;

    // Header
    card.innerHTML += `
        <div class="card-header">
            <div class="card-title-group">
                <span class="card-rank">#${index + 1} Match</span>
                <span class="card-name">${escapeHtml(tmpl.name || 'Unknown Policy')}</span>
                <span class="card-category">${escapeHtml(tmpl.category || '')}${tmpl.subcategory ? ' › ' + escapeHtml(tmpl.subcategory) : ''}</span>
            </div>
            <div class="card-badges">
                <span class="confidence-badge ${escapeHtml(level)}">
                    ${confidenceIcon(level)} ${escapeHtml(level)} (${score}%)
                </span>
            </div>
        </div>`;

    // Explanation
    if (match.explanation) {
        card.innerHTML += `
            <div class="card-explanation">${formatMarkdown(escapeHtml(match.explanation))}</div>`;
    }

    // Tabs
    card.innerHTML += `
        <div class="card-tabs" id="${cardId}-tabs">
            <button class="tab-btn active" onclick="switchTab('${cardId}', 'config', this)">📋 Policy Config</button>
            <button class="tab-btn" onclick="switchTab('${cardId}', 'effects', this)">⚡ Effects</button>
            <button class="tab-btn" onclick="switchTab('${cardId}', 'refs', this)">📚 References</button>
        </div>`;

    // Tab: Policy Config
    card.innerHTML += `
        <div class="tab-content active" id="${cardId}-config">
            ${buildConfigTab(tmpl, cardId)}
        </div>`;

    // Tab: Effects
    card.innerHTML += `
        <div class="tab-content" id="${cardId}-effects">
            ${buildEffectsTab(effects, cardId)}
        </div>`;

    // Tab: References
    card.innerHTML += `
        <div class="tab-content" id="${cardId}-refs">
            ${buildRefsTab(tmpl, mcpRefs, cardId)}
        </div>`;

    return card;
}

// ─── Config Tab ───────────────────────────────────────────
function buildConfigTab(tmpl, id) {
    const locations = (tmpl.locations || []).map(l => `<span class="location-badge">${escapeHtml(l)}</span>`).join('');
    const sits = (tmpl.sensitive_info_types || []).map(s => `<span class="tag">${escapeHtml(s)}</span>`).join('');
    const tags = (tmpl.tags || []).map(t => `<span class="tag">#${escapeHtml(t)}</span>`).join('');
    const regs = (tmpl.regulatory_references || []).map(r => `<li>${escapeHtml(r)}</li>`).join('');

    return `
        <div class="${id}-config-section">
            <div class="collapsible" id="${id}-overview">
                <div class="collapsible-header" onclick="toggleCollapsible('${id}-overview')">
                    <span class="collapsible-title">📄 Overview</span>
                    <span class="collapsible-icon open" id="${id}-overview-icon">▼</span>
                </div>
                <div class="collapsible-body open" id="${id}-overview-body">
                    <div class="info-row"><span class="info-key">Description:</span>
                        <span class="info-val">${escapeHtml(tmpl.description || '')}</span></div>
                    <div class="info-row"><span class="info-key">Priority:</span>
                        <span class="info-val">${escapeHtml(String(tmpl.priority || 1))}</span></div>
                    <div class="info-row"><span class="info-key">Locations:</span>
                        <span class="info-val"><div class="locations-row">${locations || 'N/A'}</div></span></div>
                    <div class="info-row"><span class="info-key">Sensitive Info Types:</span>
                        <span class="info-val"><div class="tags-row">${sits || 'N/A'}</div></span></div>
                    ${tags ? `<div class="info-row"><span class="info-key">Tags:</span>
                        <span class="info-val"><div class="tags-row">${tags}</div></span></div>` : ''}
                </div>
            </div>
            ${regs ? `
            <div class="collapsible" id="${id}-regs">
                <div class="collapsible-header" onclick="toggleCollapsible('${id}-regs')">
                    <span class="collapsible-title">⚖️ Regulatory References</span>
                    <span class="collapsible-icon" id="${id}-regs-icon">▼</span>
                </div>
                <div class="collapsible-body" id="${id}-regs-body">
                    <ul class="effect-list">${regs}</ul>
                </div>
            </div>` : ''}
        </div>`;
}

// ─── Effects Tab ─────────────────────────────────────────
function buildEffectsTab(effects, id) {
    const blocked  = (effects.blocked_actions  || []).map(a => `<li>${escapeHtml(a)}</li>`).join('');
    const audited  = (effects.audited_actions  || []).map(a => `<li>${escapeHtml(a)}</li>`).join('');
    const deps     = (effects.dependencies     || []).map(d => `<li>${escapeHtml(d)}</li>`).join('');
    const recs     = (effects.deployment_recommendations || []).map(r => `<li>${escapeHtml(r)}</li>`).join('');
    const fpRisk   = effects.false_positive_risk || 'MEDIUM';
    const coverage = effects.estimated_coverage || '';

    const notif    = effects.notifications || {};
    const userNotif = notif.user || {};
    const adminNotif = notif.admin || {};

    return `
        <div>
            ${blocked ? `
            <div class="collapsible open-by-default" id="${id}-blocked">
                <div class="collapsible-header" onclick="toggleCollapsible('${id}-blocked')">
                    <span class="collapsible-title">🚫 Blocked Actions</span>
                    <span class="collapsible-icon open" id="${id}-blocked-icon">▼</span>
                </div>
                <div class="collapsible-body open" id="${id}-blocked-body">
                    <ul class="effect-list blocked">${blocked}</ul>
                </div>
            </div>` : ''}

            <div class="collapsible" id="${id}-audit">
                <div class="collapsible-header" onclick="toggleCollapsible('${id}-audit')">
                    <span class="collapsible-title">📋 Audited Actions</span>
                    <span class="collapsible-icon open" id="${id}-audit-icon">▼</span>
                </div>
                <div class="collapsible-body open" id="${id}-audit-body">
                    <ul class="effect-list audited">${audited}</ul>
                </div>
            </div>

            <div class="collapsible" id="${id}-notif">
                <div class="collapsible-header" onclick="toggleCollapsible('${id}-notif')">
                    <span class="collapsible-title">🔔 Notifications</span>
                    <span class="collapsible-icon" id="${id}-notif-icon">▼</span>
                </div>
                <div class="collapsible-body" id="${id}-notif-body">
                    <div class="info-row"><span class="info-key">User notification:</span>
                        <span class="info-val">${userNotif.enabled ? '✅ Enabled' : '❌ Disabled'}</span></div>
                    ${userNotif.message ? `<div class="info-row"><span class="info-key">User message:</span>
                        <span class="info-val">${escapeHtml(userNotif.message)}</span></div>` : ''}
                    <div class="info-row"><span class="info-key">Override allowed:</span>
                        <span class="info-val">${userNotif.override_allowed ? '✅ Yes' : '❌ No'}</span></div>
                    <div class="info-row"><span class="info-key">Incident report:</span>
                        <span class="info-val">${adminNotif.incident_report ? '✅ Yes' : '❌ No'}</span></div>
                    <div class="info-row"><span class="info-key">Severity:</span>
                        <span class="info-val">${escapeHtml(adminNotif.severity || 'Medium')}</span></div>
                </div>
            </div>

            <div class="collapsible" id="${id}-deploy">
                <div class="collapsible-header" onclick="toggleCollapsible('${id}-deploy')">
                    <span class="collapsible-title">🚀 Deployment & Risk</span>
                    <span class="collapsible-icon" id="${id}-deploy-icon">▼</span>
                </div>
                <div class="collapsible-body" id="${id}-deploy-body">
                    <div class="info-row">
                        <span class="info-key">False positive risk:</span>
                        <span class="info-val"><span class="risk-badge ${fpRisk}">${fpRiskIcon(fpRisk)} ${escapeHtml(fpRisk)}</span></span>
                    </div>
                    ${coverage ? `<div class="info-row"><span class="info-key">Est. coverage:</span>
                        <span class="info-val">${escapeHtml(coverage)}</span></div>` : ''}
                    ${recs ? `<p class="section-header" style="margin-top:12px;">Recommendations</p>
                        <ul class="effect-list">${recs}</ul>` : ''}
                    ${deps ? `<p class="section-header" style="margin-top:12px;">Dependencies</p>
                        <ul class="dep-list">${deps}</ul>` : ''}
                </div>
            </div>
        </div>`;
}

// ─── References Tab ───────────────────────────────────────
function buildRefsTab(tmpl, mcpRefs, id) {
    const regRefs = (tmpl.regulatory_references || []);
    let html = '';

    if (mcpRefs && mcpRefs.length > 0) {
        html += `<p class="section-header">Microsoft Learn Documentation</p>
            <div class="ref-list">`;
        mcpRefs.forEach(ref => {
            html += `
                <a class="ref-item" href="${escapeHtml(ref.url || '#')}" target="_blank" rel="noopener">
                    <span class="ref-title">${escapeHtml(ref.title || 'Documentation')}</span>
                    <span class="ref-desc">${escapeHtml(ref.description || '')}</span>
                    <span class="ref-source">📖 ${escapeHtml(ref.source || 'Microsoft Learn')}</span>
                </a>`;
        });
        html += `</div>`;
    }

    if (regRefs.length > 0) {
        html += `<p class="section-header" style="margin-top:16px;">Regulatory References</p>
            <ul class="effect-list" style="margin-top:6px;">
                ${regRefs.map(r => `<li>${escapeHtml(r)}</li>`).join('')}
            </ul>`;
    }

    if (!html) {
        html = '<p style="color:var(--color-text-muted);font-size:13px;">No additional references available for this template.</p>';
    }

    return `<div>${html}</div>`;
}

// ─── Tab switching ────────────────────────────────────────
function switchTab(cardId, tabName, btn) {
    // Deactivate all tabs and buttons for this card
    document.querySelectorAll(`[id^="${cardId}-config"], [id^="${cardId}-effects"], [id^="${cardId}-refs"]`)
        .forEach(el => el.classList.remove('active'));

    const tabsEl = document.getElementById(`${cardId}-tabs`);
    if (tabsEl) {
        tabsEl.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    }

    // Activate selected
    const target = document.getElementById(`${cardId}-${tabName}`);
    if (target) target.classList.add('active');
    if (btn) btn.classList.add('active');
}

// ─── Collapsible toggle ───────────────────────────────────
function toggleCollapsible(id) {
    const body = document.getElementById(`${id}-body`);
    const icon = document.getElementById(`${id}-icon`);
    if (!body) return;
    body.classList.toggle('open');
    if (icon) icon.classList.toggle('open');
}

// ─── Loading state ────────────────────────────────────────
function setLoadingState(loading) {
    isLoading = loading;
    submitBtn.disabled = loading;
    if (loading) {
        btnText.classList.add('hidden');
        btnSpinner.classList.remove('hidden');
    } else {
        btnText.classList.remove('hidden');
        btnSpinner.classList.add('hidden');
    }
}

// ─── Error Toast ──────────────────────────────────────────
function showError(msg) {
    errorToast.textContent = msg;
    errorToast.classList.remove('hidden');
    setTimeout(() => errorToast.classList.add('hidden'), 5000);
}

function hideError() {
    errorToast.classList.add('hidden');
}

// ─── Utilities ────────────────────────────────────────────
function escapeHtml(str) {
    if (typeof str !== 'string') str = String(str || '');
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function formatMarkdown(text) {
    // Convert **bold** to <strong>
    return text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
}

function confidenceIcon(level) {
    const icons = { HIGH: '🟢', MEDIUM: '🟡', LOW: '🟠', VERY_LOW: '🔴' };
    return icons[level] || '⚪';
}

function fpRiskIcon(risk) {
    const icons = { LOW: '✅', MEDIUM: '⚠️', HIGH: '🔴' };
    return icons[risk] || '⚠️';
}

// ─── Copy to clipboard ────────────────────────────────────
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showError('Copied to clipboard!');
    }).catch(() => {});
}

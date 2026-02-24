/* global app.js – Purview Policy Simulator */

'use strict';

// ── Config ────────────────────────────────────────────────
const API_BASE = '';

// ── State ─────────────────────────────────────────────────
const state = {
  mcpEnabled:   false,
  mcpAvailable: false,
  loading:      false,
  results:      [],
};

// ── DOM refs ──────────────────────────────────────────────
const $ = id => document.getElementById(id);

// ── Init ──────────────────────────────────────────────────
async function init() {
  setupSidebarToggle();
  setupQueryInput();
  setupSimulateButton();
  setupChips();
  setupSidebarSectionToggles();
  setupMCPToggle();

  await Promise.allSettled([
    loadCategories(),
    checkMCPStatus(),
  ]);
}

// ── Sidebar toggle ────────────────────────────────────────
function setupSidebarToggle() {
  const btn     = $('sidebar-toggle');
  const sidebar = document.querySelector('.sidebar');

  // Overlay for mobile
  const overlay = document.createElement('div');
  overlay.className = 'sidebar-overlay';
  document.body.appendChild(overlay);

  function toggleSidebar() {
    const collapsed = sidebar.classList.toggle('collapsed');
    btn.setAttribute('aria-expanded', String(!collapsed));
    overlay.classList.toggle('visible', !collapsed && window.innerWidth <= 768);
  }

  btn.addEventListener('click', toggleSidebar);
  overlay.addEventListener('click', toggleSidebar);
}

// ── Sidebar section toggles ───────────────────────────────
function setupSidebarSectionToggles() {
  document.querySelectorAll('.sidebar-section-toggle').forEach(btn => {
    btn.addEventListener('click', () => {
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      const contentId = btn.getAttribute('aria-controls');
      const content = document.getElementById(contentId);
      btn.setAttribute('aria-expanded', String(!expanded));
      content.classList.toggle('collapsed', expanded);
    });
  });
}

// ── MCP toggle ────────────────────────────────────────────
function setupMCPToggle() {
  const toggle = $('mcp-toggle');
  toggle.addEventListener('change', () => {
    state.mcpEnabled = toggle.checked;
    if (state.mcpEnabled) checkMCPStatus();
  });
}

// ── Check MCP status ─────────────────────────────────────
async function checkMCPStatus() {
  const dot  = $('mcp-status-dot');
  const text = $('mcp-status-text');
  dot.className  = 'status-dot checking';
  text.textContent = 'Checking MCP…';

  try {
    const res  = await fetch(`${API_BASE}mcp/status`);
    const data = await res.json();
    state.mcpAvailable = data.available === true;

    if (state.mcpAvailable) {
      dot.className    = 'status-dot online';
      text.textContent = 'MCP connected';
    } else {
      dot.className    = 'status-dot offline';
      text.textContent = data.message || 'MCP unavailable';
    }
  } catch {
    state.mcpAvailable = false;
    dot.className    = 'status-dot offline';
    text.textContent = 'MCP unavailable';
  }
}

// ── Load categories ───────────────────────────────────────
async function loadCategories() {
  const list = $('categories-list');
  try {
    const res  = await fetch(`${API_BASE}templates/categories`);
    const data = await res.json();
    const cats = Array.isArray(data) ? data : (data.categories || []);

    list.innerHTML = '';
    if (cats.length === 0) {
      list.innerHTML = '<span class="status-text">No categories found</span>';
      return;
    }
    cats.forEach(cat => {
      const chip = document.createElement('span');
      chip.className   = 'category-chip';
      chip.textContent = cat.name ? `${cat.name} (${cat.count})` : String(cat);
      list.appendChild(chip);
    });
  } catch {
    list.innerHTML = '<span class="status-text" style="color:#a19f9d">Failed to load</span>';
  }
}

// ── Query input: auto-resize + char count ─────────────────
function setupQueryInput() {
  const input     = $('query-input');
  const charCount = $('char-count');

  function update() {
    charCount.textContent = `${input.value.length} / 2000`;
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 140) + 'px';
  }

  input.addEventListener('input', update);

  input.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      e.preventDefault();
      triggerSimulate();
    }
  });
}

// ── Simulate button ───────────────────────────────────────
function setupSimulateButton() {
  $('simulate-btn').addEventListener('click', triggerSimulate);
}

function triggerSimulate() {
  const query = $('query-input').value.trim();
  if (!query || state.loading) return;
  simulate(query);
}

// ── Example prompt chips ──────────────────────────────────
function setupChips() {
  document.querySelectorAll('.chip[data-prompt]').forEach(chip => {
    chip.addEventListener('click', () => {
      const query = chip.dataset.prompt;
      $('query-input').value = query;
      $('query-input').dispatchEvent(new Event('input'));
      simulate(query);
    });
  });
}

// ── Simulate API call ─────────────────────────────────────
async function simulate(query) {
  if (state.loading) return;
  setLoading(true);

  // Hide empty state on first use
  const emptyState = $('empty-state');
  if (emptyState) emptyState.style.display = 'none';

  // Show loading card
  const loadingEl = createLoadingCard(query);
  const resultsArea = $('results-area');
  resultsArea.insertBefore(loadingEl, resultsArea.firstChild);

  try {
    const response = await fetch(`${API_BASE}simulate`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({
        query,
        use_mcp:       state.mcpEnabled,
        max_templates: 3,
      }),
    });

    if (!response.ok) {
      const errData = await response.json().catch(() => ({}));
      throw new Error(errData.detail || errData.message || `HTTP ${response.status}`);
    }

    const data = await response.json();
    state.results.unshift(data);
    loadingEl.replaceWith(renderResults(data, query));
  } catch (err) {
    loadingEl.replaceWith(handleError(err, query));
  } finally {
    setLoading(false);
    $('query-input').value = '';
    $('query-input').style.height = 'auto';
    $('char-count').textContent = '0 / 2000';
  }
}

// ── setLoading ────────────────────────────────────────────
function setLoading(bool) {
  state.loading = bool;
  const btn = $('simulate-btn');
  btn.disabled = bool;
  btn.classList.toggle('loading', bool);
}

// ── Loading card ──────────────────────────────────────────
function createLoadingCard(query) {
  const card = document.createElement('div');
  card.className = 'loading-card';
  card.setAttribute('aria-label', 'Simulating…');
  card.innerHTML = `
    <div class="shimmer-line short"></div>
    <div class="shimmer-line long"></div>
    <div class="shimmer-line medium"></div>
    <div class="shimmer-line full"></div>
    <div class="shimmer-line medium"></div>
  `;
  return card;
}

// ── Render results ────────────────────────────────────────
function renderResults(data, query) {
  const card = document.createElement('article');
  card.className = 'result-card';
  card.setAttribute('aria-label', `Simulation result for: ${query}`);

  const processingTime = data.processing_time_ms != null
    ? `${Math.round(data.processing_time_ms)}ms`
    : null;

  const mcpBadge = data.mcp_enriched
    ? `<span class="badge badge-mcp" title="Enriched with live MS Learn documentation">🔗 MCP Enriched</span>`
    : '';

  const timeBadge = processingTime
    ? `<span class="badge badge-time">⏱ ${processingTime}</span>`
    : '';

  card.innerHTML = `
    <div class="result-card-header">
      <p class="result-query">${escHtml(query || data.query || '')}</p>
      <div class="result-meta">${mcpBadge}${timeBadge}</div>
    </div>
    <div class="result-body" id="result-body-${data.id || Date.now()}"></div>
  `;

  const body = card.querySelector('.result-body');

  // Template matches
  if (data.template_matches && data.template_matches.length > 0) {
    const docLinks = (data.mcp_enriched && data.documentation_links) ? data.documentation_links : [];
    data.template_matches.forEach((match, idx) => {
      // Only attach MCP doc links inline to the first template match card
      const linksForMatch = idx === 0 ? docLinks : [];
      body.appendChild(renderTemplateMatch(match, linksForMatch));
    });
  }

  // Custom config
  if (data.custom_configuration && Object.keys(data.custom_configuration).length > 0) {
    body.appendChild(renderCustomConfig(data.custom_configuration));
  }

  // Expected effects
  if (data.effects) {
    body.appendChild(renderEffects(data.effects));
  }

  // Documentation links
  if (data.documentation_links && data.documentation_links.length > 0) {
    body.appendChild(renderDocLinks(data.documentation_links));
  }

  // Troubleshooting
  if (data.troubleshooting_tips && data.troubleshooting_tips.length > 0) {
    body.appendChild(renderTroubleshooting(data.troubleshooting_tips));
  }

  if (body.children.length === 0) {
    body.innerHTML = `<p style="padding:16px 20px;color:var(--color-text-secondary);font-size:13px;">No structured results returned. Try rephrasing your query.</p>`;
  }

  return card;
}

// ── Render template match ─────────────────────────────────
function renderTemplateMatch(match, docLinks) {
  const conf   = match.confidence || {};
  const tmpl   = match.template   || {};
  const score  = conf.score;
  const level  = conf.level;
  const confidenceBadge = renderConfidenceBadge(score, level);
  const tags = (tmpl.tags || []).map(t => `<span class="tag">${escHtml(t)}</span>`).join('');
  const tagsHtml = tags ? `<div class="tag-list">${tags}</div>` : '';
  const frameworks = (tmpl.compliance_frameworks || []).join(', ');
  const locations  = (tmpl.locations || []).join(', ');

  const section = createCollapsibleSection(
    '📋',
    `Template Match${tmpl.name ? ': ' + tmpl.name : ''}`,
    `
    <div class="template-match-grid">
      ${tmpl.name        ? `<span class="tm-label">Template</span><span class="tm-value">${escHtml(tmpl.name)}</span>` : ''}
      ${tmpl.category    ? `<span class="tm-label">Category</span><span class="tm-value">${escHtml(tmpl.category)}</span>` : ''}
      ${tmpl.description ? `<span class="tm-label">Description</span><span class="tm-value">${escHtml(tmpl.description)}</span>` : ''}
      <span class="tm-label">Confidence</span>
      <span class="tm-value">
        ${confidenceBadge}
        <div class="confidence-bar-wrap">
          <div class="confidence-bar ${confidenceClass(level)}"
               style="width:${Math.round((score || 0) * 100)}%"></div>
        </div>
      </span>
      ${conf.reasoning   ? `<span class="tm-label">Reasoning</span><span class="tm-value">${escHtml(conf.reasoning)}</span>` : ''}
      ${frameworks       ? `<span class="tm-label">Frameworks</span><span class="tm-value">${escHtml(frameworks)}</span>` : ''}
      ${locations        ? `<span class="tm-label">Locations</span><span class="tm-value">${escHtml(locations)}</span>` : ''}
      ${tmpl.source_url  ? `<span class="tm-label">Reference</span><span class="tm-value"><a href="${sanitizeUrl(tmpl.source_url)}" target="_blank" rel="noopener noreferrer">📄 Microsoft Learn Reference</a></span>` : ''}
    </div>
    ${tagsHtml}
    ${renderInlineMCPLinks(docLinks)}
    `,
    true
  );
  return section;
}

// ── Render inline MCP documentation links ────────────────
function renderInlineMCPLinks(links) {
  if (!links || links.length === 0) return '';
  const items = links.map(link => {
    const url   = typeof link === 'string' ? link : (link.url || '#');
    const title = typeof link === 'string' ? url  : (link.title || url);
    const safeUrl = sanitizeUrl(url);
    return `<a class="doc-link-item inline-mcp-link" href="${safeUrl}" target="_blank" rel="noopener noreferrer">
      <span class="doc-link-title">${escHtml(title)}</span>
    </a>`;
  }).join('');
  return `<div class="inline-mcp-docs"><strong>📚 Live MS Learn Docs:</strong><div class="doc-links">${items}</div></div>`;
}


function renderEffects(effects) {
  if (!effects) return document.createDocumentFragment();

  // Collect all effect strings from the SimulationEffects object fields
  const allItems = [];
  const addItems = (label, arr) => {
    if (Array.isArray(arr) && arr.length > 0) {
      arr.forEach(e => allItems.push(`<strong>${escHtml(label)}:</strong> ${escHtml(String(e))}`));
    }
  };
  addItems('Blocked', effects.blocked_actions);
  addItems('Audited', effects.audited_actions);
  addItems('Notification', effects.notifications);
  addItems('Policy tip', effects.policy_tips);
  addItems('Incident report', effects.incident_reports);
  if (effects.user_experience)    allItems.push(`<strong>User experience:</strong> ${escHtml(effects.user_experience)}`);
  if (effects.admin_experience)   allItems.push(`<strong>Admin experience:</strong> ${escHtml(effects.admin_experience)}`);
  if (effects.false_positive_risk) allItems.push(`<strong>False positive risk:</strong> ${escHtml(effects.false_positive_risk)}`);
  addItems('Recommendation', effects.deployment_recommendations);

  const items = allItems.map(e => `<li class="effect-item">${e}</li>`).join('');

  return createCollapsibleSection(
    '⚡',
    'Expected Effects',
    `<ul class="effects-list">${items}</ul>`,
    true
  );
}

// ── Render doc links ──────────────────────────────────────
function renderDocLinks(links) {
  const items = links.map(link => {
    const url   = typeof link === 'string' ? link : (link.url || '#');
    const title = typeof link === 'string' ? url  : (link.title || url);
    const safeUrl = sanitizeUrl(url);
    return `
      <a class="doc-link-item" href="${safeUrl}" target="_blank" rel="noopener noreferrer">
        <span class="doc-link-title">${escHtml(title)}</span>
        <span class="doc-link-url">${escHtml(url)}</span>
      </a>
    `;
  }).join('');

  return createCollapsibleSection(
    '📚',
    'Documentation',
    `<div class="doc-links">${items}</div>`,
    false
  );
}

// ── Render troubleshooting ────────────────────────────────
function renderTroubleshooting(tips) {
  const items = tips.map(tip => `
    <li class="tip-item">
      <span class="tip-icon">⚠️</span>
      <span>${escHtml(typeof tip === 'string' ? tip : tip.tip || JSON.stringify(tip))}</span>
    </li>
  `).join('');

  return createCollapsibleSection(
    '🔍',
    'Troubleshooting',
    `<ul class="tips-list">${items}</ul>`,
    false
  );
}

// ── Render confidence badge ───────────────────────────────
function renderConfidenceBadge(score, level) {
  const pct   = score != null ? `${Math.round(score * 100)}%` : '—';
  const cls   = confidenceClass(level || deriveLevel(score));
  const label = (level || deriveLevel(score) || 'UNKNOWN').replace(/_/g, ' ');
  return `<span class="confidence-badge confidence-${cls}">${pct} ${label}</span>`;
}

// ── Render custom config ──────────────────────────────────
function renderCustomConfig(config) {
  // Build readable sections from CustomConfiguration fields
  let html = '<div class="custom-config-warning">⚠️ <strong>Suggested Starting Point Only.</strong> Verify all settings against official Microsoft documentation before deploying to production.</div>';
  if (config.title)       html += `<div class="config-item"><span class="config-key">Title</span><span class="config-value">${escHtml(config.title)}</span></div>`;
  if (config.locations?.length)    html += `<div class="config-item"><span class="config-key">Locations</span><span class="config-value">${escHtml(config.locations.join(', '))}</span></div>`;
  if (config.sensitive_info_types?.length) html += `<div class="config-item"><span class="config-key">Sensitive Info Types</span><span class="config-value">${escHtml(config.sensitive_info_types.join(', '))}</span></div>`;
  if (config.actions?.length)      html += `<div class="config-item"><span class="config-key">Actions</span><span class="config-value">${escHtml(config.actions.join('; '))}</span></div>`;
  if (config.steps?.length) {
    const stepHtml = config.steps.map((s,i) => `<li>${escHtml(`${i+1}. ${s}`)}</li>`).join('');
    html += `<div class="config-item"><span class="config-key">Steps</span><span class="config-value"><ol style="margin:0;padding-left:18px">${stepHtml}</ol></span></div>`;
  }
  if (config.gap_analysis) {
    const ga = config.gap_analysis;
    if (ga.covered?.length)  html += `<div class="config-item"><span class="config-key">✅ Covered</span><span class="config-value">${escHtml(ga.covered.join(', '))}</span></div>`;
    if (ga.missing?.length)  html += `<div class="config-item"><span class="config-key">⚠️ Missing</span><span class="config-value">${escHtml(ga.missing.join(', '))}</span></div>`;
  }
  if (!html) {
    const rows = Object.entries(config).map(([key, val]) => {
      const display = typeof val === 'object' ? `<code>${escHtml(JSON.stringify(val, null, 2))}</code>` : `<code>${escHtml(String(val))}</code>`;
      return `<div class="config-item"><span class="config-key">${escHtml(key)}</span><span class="config-value">${display}</span></div>`;
    }).join('');
    html = rows;
  }

  return createCollapsibleSection(
    '🔧',
    'Custom Configuration',
    `<div class="config-grid">${html}</div>`,
    false
  );
}

// ── Error display ─────────────────────────────────────────
function handleError(err, query) {
  const card = document.createElement('div');
  card.className = 'error-card';
  card.innerHTML = `
    <span class="error-icon">❌</span>
    <div class="error-content">
      <p class="error-title">Simulation failed${query ? ` for: "${escHtml(query)}"` : ''}</p>
      <p class="error-message">${escHtml(err.message || String(err))}</p>
    </div>
  `;
  return card;
}

// ── Collapsible section factory ───────────────────────────
function createCollapsibleSection(emoji, title, bodyHtml, defaultOpen) {
  const section = document.createElement('div');
  section.className = 'card-section';

  const headerId = `sec-${Math.random().toString(36).slice(2)}`;
  const bodyId   = `body-${Math.random().toString(36).slice(2)}`;

  const chevronSvg = `<svg class="section-chevron" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
    <path d="M4.293 5.293a1 1 0 011.414 0L8 7.586l2.293-2.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z"/>
  </svg>`;

  section.innerHTML = `
    <button class="card-section-header"
            id="${headerId}"
            aria-expanded="${defaultOpen ? 'true' : 'false'}"
            aria-controls="${bodyId}">
      <span class="section-emoji">${emoji}</span>
      <span class="section-title">${escHtml(title)}</span>
      ${chevronSvg}
    </button>
    <div class="card-section-body${defaultOpen ? '' : ' collapsed'}" id="${bodyId}" role="region" aria-labelledby="${headerId}">
      ${bodyHtml}
    </div>
  `;

  section.querySelector('.card-section-header').addEventListener('click', function() {
    toggleSection(this);
  });

  return section;
}

// ── Toggle collapsible section ────────────────────────────
function toggleSection(header) {
  const expanded = header.getAttribute('aria-expanded') === 'true';
  const bodyId   = header.getAttribute('aria-controls');
  const body     = document.getElementById(bodyId);
  header.setAttribute('aria-expanded', String(!expanded));
  body.classList.toggle('collapsed', expanded);
}

// ── Helpers ───────────────────────────────────────────────
function confidenceClass(level) {
  if (!level) return 'medium';
  switch (level.toUpperCase()) {
    case 'HIGH':      return 'high';
    case 'MEDIUM':    return 'medium';
    case 'LOW':       return 'low';
    case 'VERY_LOW':
    case 'VERY LOW':  return 'very-low';
    default:          return 'medium';
  }
}

function deriveLevel(score) {
  if (score == null) return 'UNKNOWN';
  if (score >= 0.85) return 'HIGH';
  if (score >= 0.60) return 'MEDIUM';
  if (score >= 0.30) return 'LOW';
  return 'VERY_LOW';
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// Only allow http/https absolute URLs; block all other schemes including
// javascript:, vbscript:, data:, and any relative-looking scheme tricks.
function sanitizeUrl(url) {
  try {
    const parsed = new URL(url);
    if (parsed.protocol === 'http:' || parsed.protocol === 'https:') {
      return url;
    }
  } catch {
    // URL() threw → not a valid absolute URL. Allow only clearly safe
    // relative paths (start with / or ./) and reject anything that looks
    // like a scheme (contains a colon before any slash).
    const colonIdx = url.indexOf(':');
    const slashIdx = url.search(/[/?#]/);
    const hasScheme = colonIdx !== -1 && (slashIdx === -1 || colonIdx < slashIdx);
    if (!hasScheme) {
      return url;
    }
  }
  return '#';
}

// ── Bootstrap ─────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', init);

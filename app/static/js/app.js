/* =========================================================
   Microsoft Purview Policy Simulator – Frontend Logic
   ========================================================= */

// ---- Example payloads ----
const EXAMPLES = {
  allow: {
    label: "✅ Allow example",
    payload: {
      subject: { id: "alice@contoso.com", subject_type: "User", display_name: "Alice" },
      resource: {
        resource_path:
          "/subscriptions/aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb/resourceGroups/rg-data/providers/Microsoft.Storage/storageAccounts/contosodatalake",
        resource_type: "AzureStorage",
        collection: "Finance"
      },
      action: "Microsoft.Purview/accounts/data/read",
      policies: [
        {
          id: "pol-001",
          name: "Finance Read Access",
          description: "Allow finance team to read storage data",
          enabled: true,
          statements: [
            {
              effect: "Allow",
              actions: ["Microsoft.Purview/accounts/data/read"],
              subjects: [{ id: "alice@contoso.com", subject_type: "User" }],
              resources: [
                {
                  resource_path:
                    "/subscriptions/aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb/resourceGroups/rg-data/providers/Microsoft.Storage/storageAccounts/contosodatalake",
                  resource_type: "AzureStorage"
                }
              ]
            }
          ]
        }
      ]
    }
  },
  deny: {
    label: "🚫 Deny example",
    payload: {
      subject: { id: "bob@contoso.com", subject_type: "User", display_name: "Bob" },
      resource: {
        resource_path:
          "/subscriptions/aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb/resourceGroups/rg-data/providers/Microsoft.Storage/storageAccounts/contosodatalake",
        resource_type: "AzureStorage",
        collection: "Finance"
      },
      action: "Microsoft.Purview/accounts/data/modify",
      policies: [
        {
          id: "pol-001",
          name: "Finance Read Access",
          enabled: true,
          statements: [
            {
              effect: "Allow",
              actions: ["Microsoft.Purview/accounts/data/read"],
              subjects: [{ id: "*", subject_type: "User" }],
              resources: [{ resource_path: "*", resource_type: "AzureStorage" }]
            }
          ]
        },
        {
          id: "pol-002",
          name: "Write Deny Policy",
          enabled: true,
          statements: [
            {
              effect: "Deny",
              actions: [
                "Microsoft.Purview/accounts/data/modify"
              ],
              subjects: [{ id: "bob@contoso.com", subject_type: "User" }],
              resources: [{ resource_path: "*", resource_type: "AzureStorage" }]
            }
          ]
        }
      ]
    }
  },
  noMatch: {
    label: "❓ No match example",
    payload: {
      subject: { id: "carol@contoso.com", subject_type: "User" },
      resource: {
        resource_path:
          "/subscriptions/aaaaaaaa-0000-1111-2222-bbbbbbbbbbbb/resourceGroups/rg-data/providers/Microsoft.Storage/storageAccounts/contosodatalake",
        resource_type: "AzureStorage"
      },
      action: "Microsoft.Purview/accounts/data/read",
      policies: [
        {
          id: "pol-001",
          name: "Alice Only Policy",
          enabled: true,
          statements: [
            {
              effect: "Allow",
              actions: ["Microsoft.Purview/accounts/data/read"],
              subjects: [{ id: "alice@contoso.com", subject_type: "User" }],
              resources: [{ resource_path: "*", resource_type: "AzureStorage" }]
            }
          ]
        }
      ]
    }
  }
};

// ---- DOM helpers ----
const $ = (id) => document.getElementById(id);

function showError(msg) {
  const el = $("error-msg");
  el.textContent = msg;
  el.style.display = "block";
}

function hideError() {
  $("error-msg").style.display = "none";
}

function setLoading(loading) {
  const btn = $("simulate-btn");
  if (loading) {
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Simulating…';
  } else {
    btn.disabled = false;
    btn.textContent = "▶  Run Simulation";
  }
}

// ---- Load example ----
function loadExample(key) {
  const ex = EXAMPLES[key];
  if (!ex) return;
  $("policy-json").value = JSON.stringify(ex.payload, null, 2);
  $("result-panel").classList.add("result-hidden");
  hideError();
}

// ---- Render result ----
function renderResult(result) {
  const panel = $("result-panel");
  panel.classList.remove("result-hidden");

  const banner = $("result-banner");
  const bannerText = $("banner-text");
  banner.className = "result-banner " + (result.access_granted ? "allow" : "deny");
  bannerText.textContent = result.access_granted
    ? "✅  Access Granted"
    : "🚫  Access Denied";

  const effectEl = $("effective-effect");
  effectEl.textContent = result.effective_effect
    ? result.effective_effect
    : "No matching policy (default deny)";

  // Matched policies
  const matchedContainer = $("matched-policies");
  matchedContainer.innerHTML = "";
  if (result.matched_policies.length === 0) {
    matchedContainer.innerHTML =
      '<p style="font-size:13px;color:#605e5c;">No policies matched.</p>';
  } else {
    result.matched_policies.forEach((m) => {
      const div = document.createElement("div");
      div.className = "matched-policy";
      const effectClass = m.effect.toLowerCase();
      div.innerHTML = `
        <span class="policy-name">${escapeHtml(m.policy_name)}</span>
        <span class="effect-badge ${effectClass}">${m.effect}</span>
        <div style="font-size:11px;color:#605e5c;margin-top:4px;">
          Policy ID: ${escapeHtml(m.policy_id)} &nbsp;·&nbsp; Statement index: ${m.statement_index}
        </div>`;
      matchedContainer.appendChild(div);
    });
  }

  // Notes
  const notesList = $("notes-list");
  notesList.innerHTML = "";
  result.evaluation_notes.forEach((note) => {
    const li = document.createElement("li");
    li.textContent = note;
    notesList.appendChild(li);
  });
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

// ---- Run simulation ----
async function runSimulation() {
  hideError();
  const raw = $("policy-json").value.trim();
  if (!raw) {
    showError("Please enter a simulation payload (JSON).");
    return;
  }

  let payload;
  try {
    payload = JSON.parse(raw);
  } catch (e) {
    showError("Invalid JSON: " + e.message);
    return;
  }

  setLoading(true);
  try {
    const resp = await fetch("/api/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!resp.ok) {
      const err = await resp.json().catch(() => ({ detail: resp.statusText }));
      const detail =
        typeof err.detail === "string"
          ? err.detail
          : JSON.stringify(err.detail);
      showError(`API error ${resp.status}: ${detail}`);
      return;
    }

    const result = await resp.json();
    renderResult(result);
  } catch (e) {
    showError("Network error: " + e.message);
  } finally {
    setLoading(false);
  }
}

// ---- Wire up events ----
document.addEventListener("DOMContentLoaded", () => {
  $("simulate-btn").addEventListener("click", runSimulation);

  // Load default example
  loadExample("allow");

  // Ctrl+Enter to run
  $("policy-json").addEventListener("keydown", (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") runSimulation();
  });
});

# Field Enablement & Asset Replication Blueprint
# Google Cloud Financial Research Agent Platform

> **Target Audience:** Google Cloud Customer Engineers (CE), Financial Services Specialists (FSI), Solution Architects, and Partner Technical Leads.  
> **Goal:** Enable technical teams to white-label, deploy, and tailor this Financial Research Agent demonstration for any global or regional financial institution in **under 15 minutes** without reinventing the wheel.

---

## 1. Asset Inventory & Architecture Overview

This repository provides an end-to-end, executive-ready asset package:

| Asset | File Location | Purpose | Reusability |
| :--- | :--- | :--- | :--- |
| **Multi-Bank Canvas** | `index.html` | High-fidelity interactive UI with real-time brand switching across 6 banks. | 100% Config-driven via JS dictionary. |
| **Sequential Pipeline** | `index.html` & `server.py` | Drag-and-drop sequential chaining of 1 to $N$ specialist functions. | Plug-and-play workflow pipeline. |
| **Resilient Backend** | `server.py` | Connects to Vertex AI / Discovery Engine 1P agent with zero-stall offline fallback. | Plug-and-play Python stdlib server. |
| **Agent Definitions** | `agent_registry/` | Declarative JSON cards for Google Cloud Agent Builder registration. | Importable into any GCP project. |
| **Data Room Catalog** | `data/` & `data/README.md` | 8 synthetic institutional financial datasets in JSONL format. | Immediate BigQuery ingestion. |
| **BigQuery Schemas** | `sql/` & `sql/README.md` | DDL schemas, authorized security views, and loading automation. | Ready-to-run GoogleSQL scripts. |
| **Executive Slides** | `docs/assets/slides/` | High-resolution slides from the institutional persona pitch deck. | Ready for customer slide decks. |
| **Diagnostics & Tests** | `tests/` | CLI scripts to test streamAssist latency, discover agents, and verify tokens. | Reusable verification toolkit. |
| **Cloud Run Deployer** | `deploy.sh` & `Dockerfile` | 1-click serverless deployment with pre-warmed instance configuration. | Deploys anywhere in 2 minutes. |

---

## 2. Fast-Track White-Labeling (15-Minute Guide)

To add a new bank (e.g., **UBS**, **Santander**, **BNP Paribas**, or **Sparkasse**), you only need to add a single configuration block to the `BANKS` object in `index.html`.

### Step 1: Define Brand Configuration
Open `index.html` around line 1030 and insert your bank definition into the `BANKS` dictionary:

```javascript
// Example: Adding UBS Group AG
ubs: {
  tag: "UBS",
  name: "UBS Group AG",
  badge: "GLOBAL WEALTH MANAGER",
  title: "UBS Global Wealth Management & Investment Bank",
  desc: "Leading global wealth manager with active presence in all major financial centers. Specialized in ultra-high-net-worth mandates, institutional asset management, and global M&A advisory.",
  license: "FINMA / ECB Systemic SIFI",
  assets: "CHF 5.5T AuM",
  focus: "Global Wealth & IBD",
  emailDomain: "ubs.com",
  localGazette: "Swiss Official Gazette of Commerce (SOGC)",
  browserPreviewUrl: "https://internal.ubs.net/portal/wealth/mandates",
  browserPreviewAction: "Status 200 OK • Extract UBS AG Wealth Allocation & Risk Budget",
  sqlTable: "ubs_internal_core.wealth_portfolios",
  primary: "#E60000",          // UBS Red
  primaryHover: "#B80000",
  primaryText: "#FFFFFF",
  accent: "#111827",           // Charcoal
  bg: "#0B0F17",               // Dark Obsidian Canvas
  surface: "#111827",
  surfaceElevated: "#182234",
  surfaceHigher: "#222F46",
  border: "#2A3B57",
  radius: "12px",
  rainbow: false,
  logoSvg: `
    <svg class="w-7 h-7" viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
    </svg>
  `
}
```

### Step 2: Add the Selector Button
In `index.html` inside the `<header>` bank pills section, add the trigger pill:

```html
<button onclick="changeBank('ubs')" id="bankPill-ubs" class="bank-pill px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center space-x-1.5 transition whitespace-nowrap border border-[var(--bank-border)]">
  <span class="w-2.5 h-2.5 rounded-full bg-[#E60000]"></span>
  <span>UBS</span>
</button>
```

**Done!** When clicked, the application automatically adapts:
* Color variables (`--bank-primary`, `--bank-accent`, `--bank-surface`).
* Institutional regulatory tags (FINMA, BaFin, FCA).
* Email addresses, database table pointers, and SVG emblems.

---

## 3. Adapting Personas and Customer Use Journeys (CUJs)

The platform comes pre-configured with 6 financial personas and 24 CUJs:

1. **Portfolio Manager (Buy Side):** M&A Due Diligence, Target Screening, Valuation Comps, Covenant Stress Test.
2. **Research Analyst (Sell Side):** Earnings Scramble, Consensus Variance, Equity Research Note, Target Price Revisions.
3. **Sales & Quant Trader:** Pre-Market Briefing, Alpha Signal Backtesting, Block Order Flow, Hedging Strategies.
4. **Business Line Manager:** Net Interest Margin (NIM) Sensitivity, Competitor Benchmarking, Deposit Beta, Branch Efficiency.
5. **Investment Banking Analyst:** Data Room Extraction, LBO/DCF Financial Modeling, M&A Pitch Books, Synergy Valuation.
6. **Compliance & KYC Manager:** Alert Fatigue Remediation, PEP & Sanctions Screening, MiCA Crypto Travel Rule, Regulatory Audit Memos.

### How to Modify CUJ Prompts for Specific Customer Engagements
If your customer is focused specifically on **Commercial Real Estate (CRE)** or **SME Credit Underwriting**, edit the `PERSONAS` dictionary in `index.html`:

```javascript
// Example: Modifying CUJ 1 for Commercial Real Estate Focus
{
  id: "cre-cuj-1",
  name: "CRE Debt Service Coverage Ratio (DSCR) & LTV Stress Test",
  desc: "Calculates interest and debt coverage for commercial real estate portfolios under a 150 bps rate shock.",
  prompt: "Perform a sensitivity stress test on the commercial real estate portfolio. Simulate an 8% increase in vacancy rates and a 150 bps rise in debt refinancing costs. Compute resulting impact on DSCR and LTV."
}
```

---

## 4. Replicating the Multi-Stage Sequential Workflow Pipeline

The platform includes a built-in sequential workflow engine that chains 1 to $N$ specialist functions in series.

### How it works:
1. **Mouse Drag & Drop Lane:** Analysts drag any hero CUJ card onto the horizontal sequence shelf, or click `+ In Pipeline`.
2. **Step Reordering & Duplication:** Steps can be shifted left/right, duplicated, or removed.
3. **Step Prompt Inspector:** Custom prompt overrides for individual steps with variable tokens:
   * `{BANK_NAME}`: Resolves to the selected bank.
   * `{VORHERIGES_ERGEBNIS}`: Forwards intermediate findings from Step $i-1$.
   * `+Zins-Stresstest`: Injects ECB +200 bps monetary shock parameters.
   * `+Regulatorik`: Injects BaFin, ECB SSM, and MiCA regulatory criteria.
4. **Context Propagation:** Step $i$ results are automatically forwarded to Step $i+1$ as structured background context.

### Customizing Pipeline Presets
To add or modify preset pipeline chains for a specific client meeting, edit `loadPreset()` in `index.html`:

```javascript
// Example: Adding a Private Equity Buyout Preset
if (presetKey === "pe_buyout") {
  pipelineSteps = [
    {
      id: "step-pe-1",
      persona: "IB_ANALYST",
      cujId: "ib-cuj-1",
      title: "Data Room Extraction",
      prompt: "Extract historical financial statements and EBITDA adjustments for target entity..."
    },
    {
      id: "step-pe-2",
      persona: "IB_ANALYST",
      cujId: "ib-cuj-2",
      title: "LBO Returns Model",
      prompt: "Using figures from Step 1, construct a 5-year LBO model with 4.5x senior leverage..."
    },
    {
      id: "step-pe-3",
      persona: "PORTFOLIO_MANAGER",
      cujId: "pm-cuj-1",
      title: "Investment Committee Memo",
      prompt: "Synthesize findings into an Investment Committee memo with return sensitivities..."
    }
  ];
  renderPipelineLane();
}
```

---

## 5. Connecting Customer Data Stores & Vertex AI Agents

The backend (`server.py`) talks directly to the Google Cloud Discovery Engine / Vertex AI Agent Builder endpoint:

```
POST https://discoveryengine.googleapis.com/v1alpha/projects/{PROJECT_NUM}/locations/global/collections/default_collection/engines/{ENGINE_ID}/servingConfigs/default_search:streamAssist
```

### To point this to a customer's dedicated Vertex AI Agent:
Set environment variables before starting the backend:

```bash
export PROJECT_ID="customer-fsi-prod"
export PROJECT_NUM="123456789012"
export ENGINE_ID="fsi-research-engine"
export AGENT_ID="finance_research"
export PORT="8085"

python3 server.py
```

### Linking Internal Data Rooms (BigQuery & Cloud Storage)
To enable the agent to query real customer balance sheets:
1. **Unstructured Documents (PDFs, Annual Reports, Pitch Books):**
   * Upload documents to `gs://<customer>-data-room/`.
   * Create a Vertex AI Search Data Store pointing to that GCS bucket.
   * Attach the Data Store as a tool to the `finance_research` agent in Agent Builder.
2. **Structured Tables (Balance Sheets, Loan Books, Market Comps):**
   * In BigQuery, create tables using `sql/02_bank_internal_core_ddl.sql` and `sql/03_market_external_enrichment_ddl.sql`.
   * Configure the BigQuery NL2SQL extension in Agent Builder.

---

## 6. Live Executive Demonstration Playbook

### The 60-Second Hook (How to open the meeting)
1. **Start with the Bank Switcher:**  
   *"Notice how the cockpit instantly adopts N26's brand, license, and balance sheet metrics. With one click, we switch to Deutsche Bank or Revolut. This is a single, sovereign agentic architecture that adapts to any institutional mandate."*
2. **Demonstrate the Sequential Pipeline:**  
   *"In institutional workflows, research isn't a single prompt. We drag three specialist functions onto our workflow shelf: M&A Diligence ➔ Valuation Comps ➔ Compliance Screening. We click 'Run Pipeline in Series'."*
3. **Narrate during generation (Latency Masking):**  
   *"While the agent works, look at the step trace. The 1P Financial Research Agent executes a multi-hop reasoning plan: First, querying confidential BigQuery credit records. Second, computing deterministic DSCR math without hallucinations. Third, verifying sanctions registers."*
4. **Show the Deliverables:**  
   * **Consolidated Master Dossier:** Unified multi-stage executive brief.
   * **Interactive Step Navigator:** Discrete drill-downs into each specialist step.
   * **Interactive Financial Models:** Live sensitivity scenario toggles.
   * **Export:** Click **"Download PDF Dossier"** for immediate executive distribution.

---

## 7. Resilience & Offline Fallback Strategy

Executive presentations often suffer from conference Wi-Fi drops or expired Google OAuth tokens.

This asset is engineered with **Automatic Zero-Stall Fallback**:
* When `server.py` detects that `gcloud auth print-access-token` has expired or the Google Cloud API returns an error, it **automatically and silently switches to high-fidelity synthetic generation**.
* The synthetic response matches the exact bank and persona selected, delivering realistic financial models, peer multiples, and citations.
* The presenter is never exposed to raw stack traces, error modals, or loading spinners.

---

## 8. Multi-Tenant Deployment via Cloud Run

To spin up an isolated demo instance for a specific customer:

```bash
# Set customer context
export PROJECT_ID="my-argolis-project"
export REGION="europe-west3"
export SERVICE_NAME="fsi-demo-santander"

# Deploy via Cloud Build and Cloud Run
gcloud config set project "${PROJECT_ID}"
gcloud builds submit --tag "${REGION}-docker.pkg.dev/${PROJECT_ID}/cloud-run-source-deploy/${SERVICE_NAME}:latest" .
gcloud run deploy "${SERVICE_NAME}" \
  --image "${REGION}-docker.pkg.dev/${PROJECT_ID}/cloud-run-source-deploy/${SERVICE_NAME}:latest" \
  --platform managed \
  --region "${REGION}" \
  --allow-unauthenticated \
  --min-instances 1 \
  --memory 1Gi \
  --cpu 1
```

By keeping `--min-instances 1`, the container is kept permanently warm in RAM, ensuring instantaneous initial page loads when meeting with C-level stakeholders.

# REST API Reference
## Google Cloud Financial Research Agent Platform

> **Base URL:** `http://localhost:8085` (or `http://topbulut.c.googlers.com:8085`)  
> **Content-Type:** `application/json`  
> **Authentication:** Google Cloud IAM OAuth2 Bearer Token (handled automatically by backend)

---

## 1. System Health & Configuration

### `GET /api/status`
Returns the operational status of the gateway, active Google Cloud project binding, Discovery Engine engine ID, and current IAM token health.

#### Request
```bash
curl -X GET http://localhost:8085/api/status
```

#### Response (`200 OK`)
```json
{
  "status": "healthy",
  "project_id": "ai-cartridge",
  "engine_id": "finance_research",
  "location": "global",
  "collection": "default_collection",
  "auth_available": true,
  "token_cached": true,
  "server_time": "2026-09-18T12:00:00.000000Z",
  "version": "2.4.0"
}
```

---

## 2. Multi-Bank Simulation Metadata

### `GET /api/banks`
Returns the catalog of simulated banking institutions, including brand tokens, regulatory authorities, deposit balance sheet metrics, and data lake mappings.

#### Request
```bash
curl -X GET http://localhost:8085/api/banks
```

#### Response (`200 OK`)
```json
{
  "banks": {
    "n26": {
      "name": "N26 Bank",
      "tag": "N26",
      "tagline": "The Mobile Bank",
      "license": "BaFin / EZB Vollbank",
      "assets": "€8.2 Mrd.",
      "focus": "Retail & Wealth",
      "primary": "#088177",
      "bg": "#0D1318",
      "sqlTable": "bq_reg_lake.de_n26_prudential"
    },
    "revolut": {
      "name": "Revolut",
      "tag": "REV",
      "tagline": "Change the way you money",
      "license": "UK PRA & Bank of Lithuania",
      "assets": "€21.5 Mrd.",
      "focus": "FX & Global Treasury",
      "primary": "#1326FD",
      "bg": "#080B10",
      "sqlTable": "bq_treasury_lake.uk_revolut_prudential"
    },
    "traderepublic": {
      "name": "Trade Republic",
      "tag": "TR",
      "tagline": "Europe's largest savings platform",
      "license": "BaFin Vollbank",
      "assets": "€35.0 Mrd. AUM",
      "focus": "Wealth & Securities",
      "primary": "#FFFFFF",
      "bg": "#000000",
      "sqlTable": "bq_securities_lake.de_traderepublic_deposits"
    },
    "deutschebank": {
      "name": "Deutsche Bank (CIB)",
      "tag": "DB",
      "tagline": "Leistung aus Leidenschaft",
      "license": "EZB / BaFin Tier-1",
      "assets": "€1.31 Bio.",
      "focus": "Capital Markets & M&A",
      "primary": "#0018A8",
      "bg": "#030712",
      "sqlTable": "bq_cib_lake.global_db_prudential"
    },
    "monzo": {
      "name": "Monzo Bank",
      "tag": "MONZO",
      "tagline": "Banking made easy",
      "license": "UK PRA & FCA",
      "assets": "£11.2 Mrd.",
      "focus": "Digital Retail & Flex",
      "primary": "#FF4F40",
      "bg": "#09121D",
      "sqlTable": "bq_monzo_lake.uk_monzo_credit_risk"
    },
    "bunq": {
      "name": "bunq",
      "tag": "BUNQ",
      "tagline": "Bank of The Free",
      "license": "Dutch DNB Vollbank",
      "assets": "€4.5 Mrd.",
      "focus": "ESG & Multi-IBAN",
      "primary": "#00A86B",
      "bg": "#030D08",
      "sqlTable": "bq_esg_lake.nl_bunq_sustainability"
    }
  }
}
```

---

## 3. Personas & CUJ Catalog

### `GET /api/personas`
Retrieves the list of 6 institutional personas, their hero use journeys, descriptions, and sample prompts.

#### Request
```bash
curl -X GET http://localhost:8085/api/personas
```

#### Response (`200 OK`)
```json
{
  "personas": [
    {
      "code": "PORTFOLIO_MANAGER",
      "title": "Portfolio Manager & Investment Analyst (Buy side)",
      "heroCUJ": "Accelerate due diligence by synthesizing large volumes of research materials and generating first drafts of investment memos.",
      "cuj_count": 4
    },
    {
      "code": "RESEARCH_ANALYST",
      "title": "Research Analyst (Sell side)",
      "heroCUJ": "Address the 'earnings scramble' by summarizing press releases and creating initial drafts of research notes, reducing the time required to publish analysis.",
      "cuj_count": 4
    },
    {
      "code": "QUANT_TRADER",
      "title": "Sales & Quant Trader",
      "heroCUJ": "Prepare morning briefings tailored to specific client lists by synthesizing overnight news and market data; Identify personalized trading ideas.",
      "cuj_count": 4
    },
    {
      "code": "BUSINESS_LINE_MGR",
      "title": "Business Line Manager & Strategy Executive",
      "heroCUJ": "Deliver competitive intelligence on deposit pricing, net interest margin trends, and market share movements.",
      "cuj_count": 4
    },
    {
      "code": "IB_ANALYST",
      "title": "Investment Banking Analyst (M&A / DCM)",
      "heroCUJ": "Synthesize virtual data rooms, extract financial line items, and formulate DCF valuation models and pitchbook comps.",
      "cuj_count": 4
    },
    {
      "code": "COMPLIANCE_MGR",
      "title": "Compliance, KYC & AML Officer",
      "heroCUJ": "Clear alert fatigue by vetting transaction counter-parties against sanctions lists, PEP databases, and regulatory regimes.",
      "cuj_count": 4
    }
  ]
}
```

---

## 4. Single Agent Research Execution

### `POST /api/run_agent`
Dispatches a financial research prompt to the Google Cloud 1P Boq agent (`finance_research`) via Vertex AI Discovery Engine `:streamAssist`. If the Cloud IAM token is expired or offline, it routes transparently to the high-fidelity synthetic fallback engine.

#### Request Headers
| Header | Value | Description |
| :--- | :--- | :--- |
| `Content-Type` | `application/json` | Required |

#### Request Body
```json
{
  "bank": "n26",
  "persona": "PORTFOLIO_MANAGER",
  "query": "Perform a comprehensive credit stress test for Hanseatische Hafenlogistik AG (FKG-9901) assuming a +200 bps ECB rate shock."
}
```

#### Response (`200 OK`)
```json
{
  "status": "success",
  "execution_mode": "LIVE_1P_AGENT",
  "bank": "n26",
  "persona": "PORTFOLIO_MANAGER",
  "thoughts": [
    "Identified target entity: Hanseatische Hafenlogistik AG (Facility ID FKG-9901).",
    "Querying BigQuery internal core dataset `bank_internal_core.firmenkredite` for loan volume and margin.",
    "Joining `bank_internal_core.finanzhistorie` to retrieve LTM EBITDA and debt service obligations.",
    "Applying +200 bps shock to Euribor baseline using deterministic math service.",
    "Evaluating DSCR covenant threshold against `bank_internal_core.kredit_covenants`."
  ],
  "text": "### Executive Investment Committee Memo\n\n**Borrower:** Hanseatische Hafenlogistik AG\n**Facility ID:** FKG-9901 | Senior Secured Fleet Facility (€35.0M)\n\n#### 1. Baseline Financial Position\n* **LTM Revenue:** €104.74M\n* **LTM EBITDA:** €16.76M (16.0% margin)\n* **Baseline DSCR:** 2.47x (Contractual Covenant Minimum: 1.25x)\n\n#### 2. +200 bps Rate Shock Stress Simulation\n* **Post-Shock Interest Expense:** €2.03M (+€700k increase)\n* **Stressed DSCR:** 1.84x (Remains compliant with 59 bps cushion above 1.25x trigger)\n\n#### 3. Committee Recommendation\n**MAINTAIN RATINGS ACCORD:** Recommend approval of facility renewal with periodic quarterly covenant monitoring.",
  "citations": [
    {
      "title": "BigQuery: bank_internal_core.firmenkredite",
      "uri": "bq://ai-cartridge.bank_internal_core.firmenkredite"
    },
    {
      "title": "BigQuery: bank_internal_core.finanzhistorie",
      "uri": "bq://ai-cartridge.bank_internal_core.finanzhistorie"
    }
  ],
  "trace_id": "tr-8f92a10b-4d7e",
  "latency_ms": 1420
}
```

---

## 5. Multi-Stage Sequential Workflow Pipeline

### `POST /api/run_pipeline`
Executes an ordered sequence of specialist functions (1 to $N$ steps). Each step can execute independently or consume the context and findings generated by preceding steps.

#### Request Body
```json
{
  "bank": "n26",
  "pass_context": true,
  "steps": [
    {
      "step_index": 1,
      "persona": "IB_ANALYST",
      "cuj_id": "ib-cuj-1",
      "title": "M&A Virtual Data Room Extraction",
      "prompt": "Extract the EBITDA and free cash flow baseline for Nordic Cold Chain Logistics GmbH (MA-8801)."
    },
    {
      "step_index": 2,
      "persona": "PORTFOLIO_MANAGER",
      "cuj_id": "pm-cuj-1",
      "title": "Buy-Side Valuation & Comps Analysis",
      "prompt": "Using the financial metrics extracted in Step 1, benchmark Nordic Cold Chain Logistics against European logistics peers using EV/EBITDA multiples."
    },
    {
      "step_index": 3,
      "persona": "COMPLIANCE_MGR",
      "cuj_id": "comp-cuj-2",
      "title": "Ultimate Beneficial Owner (UBO) Screening",
      "prompt": "Screen the acquiring consortium and target board against EU Sanctions and PEP watchlists."
    }
  ]
}
```

#### Response (`200 OK`)
```json
{
  "status": "success",
  "execution_mode": "SEQUENTIAL_PIPELINE",
  "total_steps": 3,
  "completed_steps": 3,
  "bank": "n26",
  "consolidated_dossier": "### Consolidated Master Research Dossier\n\n#### Executive Synthesis across 3 Analysis Stages\n...",
  "step_results": [
    {
      "step_index": 1,
      "persona": "IB_ANALYST",
      "title": "M&A Virtual Data Room Extraction",
      "status": "COMPLETED",
      "text": "#### Data Room Diligence Report\nTarget: Nordic Cold Chain Logistics GmbH...",
      "latency_ms": 1100
    },
    {
      "step_index": 2,
      "persona": "PORTFOLIO_MANAGER",
      "title": "Buy-Side Valuation & Comps Analysis",
      "status": "COMPLETED",
      "text": "#### Peer Multiple Valuation Matrix\nPeer Group EV/EBITDA Median: 8.4x...",
      "latency_ms": 1250
    },
    {
      "step_index": 3,
      "persona": "COMPLIANCE_MGR",
      "title": "Ultimate Beneficial Owner (UBO) Screening",
      "status": "COMPLETED",
      "text": "#### Compliance Clearance Certificate\nZero PEP or Sanctions matches found for target entities...",
      "latency_ms": 980
    }
  ],
  "total_latency_ms": 3330
}
```

---

## 6. Error Codes & Diagnostic Responses

| HTTP Status | Error Code | Description | Recommended Action |
| :--- | :--- | :--- | :--- |
| `400 Bad Request` | `INVALID_PAYLOAD` | Request body missing required fields (`query`, `bank`, or `steps`). | Validate JSON syntax against schema. |
| `404 Not Found` | `UNKNOWN_ENDPOINT` | Requested path is not registered on the gateway. | Verify endpoint path and HTTP verb. |
| `500 Internal Error`| `PIPELINE_STEP_FAILED` | An unhandled exception occurred during step execution. | Check server logs (`journalctl` / task log). |
| `504 Gateway Timeout`| `UPSTREAM_TIMEOUT` | Discovery Engine took longer than 30 seconds to stream response. | System automatically falls back to synthetic response. |

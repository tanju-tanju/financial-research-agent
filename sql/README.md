# BigQuery Provisioning, DDL & Authorized Views Guide
## Google Cloud Financial Research Agent Platform

> **Location:** `sql/`  
> **Target Warehouse:** Google Cloud BigQuery (`europe-west3` or `US`)  
> **Architecture:** Dual-Tier Warehouse with Column-Level Security and Authorized Views

---

## 1. Directory Structure & Execution Pipeline

The scripts and DDL files in this directory establish the end-to-end data foundation for the Financial Research Agent:

```
sql/
├── 01_provision_datasets.sh              # Creates BigQuery datasets in target GCP project
├── 02_bank_internal_core_ddl.sql         # DDL schemas for restricted internal banking data
├── 03_market_external_enrichment_ddl.sql # DDL schemas for public capital markets intelligence
├── 04_authorized_views.sql               # Granular security views with row/column masking
├── 05_load_synthetic_data.sh             # Loads data/*.jsonl records using `bq load`
├── generate_personas_jsonl.py            # Generates personas.jsonl catalog
└── personas.jsonl                        # Persona and hero CUJ catalog in JSONL format
```

---

## 2. Step-by-Step Deployment Instructions

Run the scripts in numerical order using the Google Cloud SDK (`gcloud` / `bq`):

### Step 1: Provision BigQuery Datasets
Creates the two foundational datasets with regional location tags (`europe-west3`):
```bash
chmod +x sql/01_provision_datasets.sh
./sql/01_provision_datasets.sh <YOUR_PROJECT_ID> europe-west3
```
*Creates:*
1. `${PROJECT_ID}.bank_internal_core`: Restricted proprietary banking data.
2. `${PROJECT_ID}.market_external_enrichment`: Market benchmarks, watchlists, and multiples.

### Step 2: Create Core Banking Tables
Executes the DDL definitions for commercial loans, covenants, and M&A deals:
```bash
bq query --use_legacy_sql=false \
  --project_id=<YOUR_PROJECT_ID> \
  < sql/02_bank_internal_core_ddl.sql
```

### Step 3: Create Market Intelligence Tables
Executes the DDL definitions for peer multiples and macroeconomic series:
```bash
bq query --use_legacy_sql=false \
  --project_id=<YOUR_PROJECT_ID> \
  < sql/03_market_external_enrichment_ddl.sql
```

### Step 4: Configure Authorized Views & Security Layer
Establishes pre-joined authorized views that allow personas to query synthesized data rooms without granting direct access to raw internal tables:
```bash
bq query --use_legacy_sql=false \
  --project_id=<YOUR_PROJECT_ID> \
  < sql/04_authorized_views.sql
```

### Step 5: Ingest Synthetic Institutional Datasets
Loads all JSONL records from `data/` into BigQuery tables using `bq load`:
```bash
chmod +x sql/05_load_synthetic_data.sh
./sql/05_load_synthetic_data.sh <YOUR_PROJECT_ID>
```

---

## 3. DDL Specifications

### 3.1 `02_bank_internal_core_ddl.sql`
* **`bank_internal_core.firmenkredite`**: Commercial loan facilities, debtor IDs, risk ratings (AAA to C), $PD$, $LGD$, and pledged collateral values.
* **`bank_internal_core.finanzhistorie`**: Multi-year LTM revenues, EBITDA margins, CapEx, debt service, cash tax, and liquid reserves. Partitioned by fiscal year.
* **`bank_internal_core.kredit_covenants`**: Contractual minimum and maximum triggers (DSCR, Debt/EBITDA, Interest Coverage), test frequencies, and cure periods.
* **`bank_internal_core.ma_deal_pipeline`**: Active M&A advisory mandates, target company classifications, and valuation bands.
* **`bank_internal_core.private_wealth_portfolios`**: Client asset holdings, MiFID II risk classes, target vs. actual weights, and ESG compliance flags.

### 3.2 `03_market_external_enrichment_ddl.sql`
* **`market_external_enrichment.capital_markets_multiples`**: Public trading peer multiples ($EV/\text{EBITDA}$, $EV/\text{Sales}$, $P/E$, $Net Debt/\text{EBITDA}$, and Free Cash Flow Yield). Clustered by industrial sector (`wz_code`).
* **`market_external_enrichment.macro_transport_benchmarks`**: Historical time series of ECB policy rates, Euribor 3M/6M fixings, diesel price indices, and sector default rates. Partitioned by `gueltigkeits_datum`.
* **`market_external_enrichment.regulatory_compliance_watchlists`**: Sanctions entities (EU, OFAC), PEP registers, and beneficial ownership records. Clustered by `suchname` for rapid fuzzy text matching.

---

## 4. Authorized Views Architecture (`04_authorized_views.sql`)

To enforce least-privilege access and protect proprietary bank data:
* **`v_commercial_credit_dossier`**: Joins `firmenkredite`, `finanzhistorie`, and `macro_transport_benchmarks`. Calculates Debt Service Coverage Ratio ($\text{DSCR}$) dynamically using GoogleSQL functions.
* **`v_ma_pipeline_overview`**: Joins `ma_deal_pipeline` with `capital_markets_multiples` to compute valuation multiple premiums/discounts on the fly.
* **`v_wealth_rebalancing_alerts`**: Computes portfolio asset allocation drift against MiFID II target bands and flags accounts requiring rebalancing.
* **`v_sanctions_screener`**: Provides fuzzy search capabilities over sanctions databases with normalized Unicode casing.

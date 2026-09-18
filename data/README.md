# Institutional Data Room Catalog & Data Dictionary
## Google Cloud Financial Research Agent Platform

> **Location:** `data/`  
> **Format:** JSON Lines (`.jsonl`)  
> **Data Governance:** 100% Synthetic Datasets. Zero real Personally Identifiable Information (PII) or confidential customer records. Designed for enterprise simulation, stress testing, and executive demonstrations.

---

## 1. Data Architecture & BigQuery Dataset Mapping

The data files in this repository map directly to two BigQuery datasets:

```
data/
├── bank_internal_core/ (Internal Core Banking - Restricted Tier)
│   ├── firmenkredite.jsonl                -> bank_internal_core.firmenkredite
│   ├── finanzhistorie.jsonl               -> bank_internal_core.finanzhistorie
│   ├── kredit_covenants.jsonl             -> bank_internal_core.kredit_covenants
│   ├── ma_deal_pipeline.jsonl             -> bank_internal_core.ma_deal_pipeline
│   └── private_wealth_portfolios.jsonl    -> bank_internal_core.private_wealth_portfolios
│
└── market_external_enrichment/ (Public Market Benchmarks - Accessible Tier)
    ├── capital_markets_multiples.jsonl    -> market_external_enrichment.capital_markets_multiples
    ├── macro_transport_benchmarks.jsonl   -> market_external_enrichment.macro_transport_benchmarks
    ├── regulatory_compliance_watchlists.jsonl -> market_external_enrichment.regulatory_compliance_watchlists
    └── audit_log.jsonl                    -> bank_internal_core.audit_log (WORM Ledger)
```

---

## 2. Comprehensive Data Dictionaries

### 2.1 `firmenkredite.jsonl` (Commercial Loan Facilities)
Contains credit facility records for commercial and corporate borrowers.
* **Target Table:** `bank_internal_core.firmenkredite`
* **Primary Key:** `fazilitaet_id`
* **Foreign Keys:** `kreditnehmer_id`, `wz_code`

| Field Name | Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `fazilitaet_id` | STRING | Unique facility identifier | `"FKG-9901"` |
| `kreditnehmer_id` | STRING | Unique borrower identifier | `"KND-9901"` |
| `kreditnehmer_name` | STRING | Corporate legal name of borrower | `"Hanseatische Hafenlogistik AG"` |
| `rechtsform` | STRING | Corporate legal form (AG, GmbH, etc.) | `"AG"` |
| `wz_code` | STRING | German industrial sector classification code | `"H49.41"` |
| `wz_bezeichnung` | STRING | Sector description | `"Güterkraftverkehr & Hafenlogistik"` |
| `beantragtes_volumen` | FLOAT | Committed facility principal (EUR) | `35000000.0` |
| `fazilitaet_typ` | STRING | Facility loan structure | `"Investitions- & Flottenkredit"` |
| `rangfolge` | STRING | Debt seniority | `"Senior Secured"` |
| `basiszins_indikator` | STRING | Benchmark floating rate index | `"Euribor 3M"` |
| `marge_bps` | INTEGER | Agreed lending spread in basis points | `240` |
| `laufzeit_monate` | INTEGER | Facility tenor in months | `60` |
| `sicherheitenwert_eur` | FLOAT | Appraised value of pledged collateral | `53200000.0` |
| `interne_bonitaetsstufe`| STRING | Internal credit rating master scale | `"AAA"` |
| `ausfallwahrscheinlichkeit_pd`| FLOAT | 1-year Probability of Default ($PD$) in % | `0.12` |
| `verlustquote_lgd` | FLOAT | Loss Given Default ($LGD$) in % | `18.5` |
| `tage_ueberfaellig_dpd` | INTEGER | Days Past Due ($DPD$) | `0` |

---

### 2.2 `finanzhistorie.jsonl` (Historical Financial Statements)
Multi-year P&L, balance sheet, and cash flow records for corporate credit borrowers.
* **Target Table:** `bank_internal_core.finanzhistorie`
* **Primary Key:** Composite (`fazilitaet_id`, `geschaeftsjahr`)

| Field Name | Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `fazilitaet_id` | STRING | Linked credit facility ID | `"FKG-9901"` |
| `geschaeftsjahr` | STRING | Fiscal reporting period | `"GJ 2024 (LTM)"` |
| `umsatzerloese_eur` | FLOAT | Total revenue (EUR) | `104737500.0` |
| `ebitda_eur` | FLOAT | Operating profit before D&A (EUR) | `16758000.0` |
| `capex_eur` | FLOAT | Capital expenditures (EUR) | `5760562.5` |
| `zinsaufwand_eur` | FLOAT | Annual interest expenses (EUR) | `1330000.0` |
| `tilgungsdienst_eur` | FLOAT | Contractual principal amortization | `2275000.0` |
| `steueraufwand_cash_eur`| FLOAT | Cash income taxes paid (EUR) | `2094750.0` |
| `freier_cashflow_eur` | FLOAT | Free cash flow before debt service | `10892700.0` |
| `gesamtverbindlichkeiten_eur`| FLOAT | Total balance sheet liabilities | `73500000.0` |
| `fluessige_mittel_eur` | FLOAT | Cash and cash equivalents | `8750000.0` |

---

### 2.3 `kredit_covenants.jsonl` (Loan Covenants & Triggers)
Contractual covenants governing commercial credit facilities.
* **Target Table:** `bank_internal_core.kredit_covenants`
* **Primary Key:** `covenant_id`

| Field Name | Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `covenant_id` | STRING | Unique covenant clause identifier | `"COV-FKG-9901-01"` |
| `fazilitaet_id` | STRING | Associated facility ID | `"FKG-9901"` |
| `covenant_typ` | STRING | Covenant type (`MIN_DSCR`, `MAX_LEVERAGE`) | `"MIN_DSCR"` |
| `schwellenwert_mindest`| FLOAT | Minimum required covenant ratio | `1.25` |
| `schwellenwert_maximal`| FLOAT | Maximum allowed covenant ratio | `null` |
| `prueffrequenz` | STRING | Compliance test frequency | `"QUARTERLY"` |
| `letzter_pruefwert` | FLOAT | Most recent tested ratio value | `2.47` |
| `covenant_status` | STRING | Covenant status (`OK`, `WATCH`, `BREACH`) | `"OK"` |
| `heilungsfrist_tage` | INTEGER | Grace period to cure breach (days) | `30` |

---

### 2.4 `ma_deal_pipeline.jsonl` (M&A Advisory Mandates)
Confidential deal room tracking for Investment Banking M&A mandates.
* **Target Table:** `bank_internal_core.ma_deal_pipeline`
* **Primary Key:** `deal_id`

| Field Name | Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `deal_id` | STRING | Unique transaction identifier | `"MA-8801"` |
| `zielgesellschaft_name` | STRING | Legal name of target company | `"Nordic Cold Chain Logistics GmbH"` |
| `branche_wz` | STRING | Industrial classification | `"H52.10"` |
| `mandant_name` | STRING | Retaining client / private equity sponsor | `"Hanseatic Private Equity Fonds"` |
| `transaktions_typ` | STRING | Mandate direction (`BUY_SIDE`, `SELL_SIDE`)| `"BUY_SIDE"` |
| `ziel_ev_spanne_min` | FLOAT | Low end of target EV range (EUR) | `45000000.0` |
| `ziel_ev_spanne_max` | FLOAT | High end of target EV range (EUR) | `55000000.0` |
| `umsatz_akt_eur` | FLOAT | LTM Revenue of target (EUR) | `65000000.0` |
| `ebitda_akt_eur` | FLOAT | LTM EBITDA of target (EUR) | `8200000.0` |
| `status` | STRING | Deal stage (`SCREENING`, `DD`, `SIGNING`) | `"SCREENING"` |

---

### 2.5 `capital_markets_multiples.jsonl` (Listed Peer Multiples)
Real-time valuation multiples for public market trading comparables.
* **Target Table:** `market_external_enrichment.capital_markets_multiples`
* **Primary Key:** `ticker`

| Field Name | Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `ticker` | STRING | Stock ticker symbol | `"KUEHNE"` |
| `unternehmensname` | STRING | Corporate name | `"Kühne + Nagel International AG"`|
| `sektor` | STRING | Market sector | `"Logistik & Spedition"` |
| `wz_code` | STRING | Sector code | `"H49.41"` |
| `marktkapitalisierung_eur`| FLOAT | Market capitalization (EUR) | `28500000000.0` |
| `enterprise_value_eur` | FLOAT | Enterprise Value ($EV$) (EUR) | `31200000000.0` |
| `ev_ebitda_multiple` | FLOAT | $EV / \text{EBITDA}$ Multiple | `8.4` |
| `ev_sales_multiple` | FLOAT | $EV / \text{Sales}$ Multiple | `1.1` |
| `pe_multiple` | FLOAT | Price-to-Earnings ($P/E$) Multiple | `16.2` |
| `net_debt_ebitda` | FLOAT | Net Debt / EBITDA ratio | `1.2` |
| `free_cashflow_yield_pct`| FLOAT | Free Cash Flow Yield in % | `6.8` |

---

### 2.6 `private_wealth_portfolios.jsonl` (Client Wealth Depots)
High-Net-Worth Individual (HNWI) wealth allocations and MiFID II mandates.
* **Target Table:** `bank_internal_core.private_wealth_portfolios`
* **Primary Key:** `depot_id`

| Field Name | Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `depot_id` | STRING | Portfolio depot identifier | `"DEP-7701"` |
| `kunde_id` | STRING | Customer identifier | `"KND-1001"` |
| `kunden_segment` | STRING | Customer tier (`HNWI`, `UHNWI`, `RETAIL`)| `"HNWI"` |
| `mifid_risikoklasse` | INTEGER | MiFID II risk profile (1 to 5) | `3` |
| `depotwert_gesamt_eur` | FLOAT | Total portfolio value (EUR) | `4500000.0` |
| `ziel_aktien_quote` | FLOAT | Target equity weight (0.0 – 1.0) | `0.40` |
| `ist_aktien_quote` | FLOAT | Current equity weight (0.0 – 1.0) | `0.41` |
| `sperrliste_esg_konform` | BOOLEAN | ESG exclusion list compliance | `true` |

---

### 2.7 `regulatory_compliance_watchlists.jsonl` (Sanctions & PEP)
Regulatory watchlists for counterparty screening.
* **Target Table:** `market_external_enrichment.regulatory_compliance_watchlists`
* **Primary Key:** `eintrag_id`

| Field Name | Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `eintrag_id` | STRING | Unique entry identifier | `"SANCT-EU-2024-001"` |
| `suchname` | STRING | Legal entity or individual name | `"Volkov Shipping Ltd"` |
| `entitaets_typ` | STRING | Entity classification (`ENTERPRISE`, `INDIVIDUAL`)| `"ENTERPRISE"` |
| `sanktionsliste` | STRING | Watchlist source (`EU_SANCTIONS`, `OFAC`)| `"EU_SANCTIONS"` |
| `wirtschaftlich_berechtigter`| STRING | Ultimate Beneficial Owner (UBO) | `"Dmitri Volkov"` |
| `transparenzregister_status` | STRING | Registry status (`SANCTIONED`, `CLEAR`) | `"SANCTIONED"` |

---

### 2.8 `macro_transport_benchmarks.jsonl` (Macroeconomic Indicators)
Central bank rates, money market fixings, and inflation benchmarks.
* **Target Table:** `market_external_enrichment.macro_transport_benchmarks`
* **Primary Key:** Composite (`gueltigkeits_datum`, `wz_code`)

| Field Name | Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `gueltigkeits_datum` | DATE | Benchmark effective date | `"2025-05-01"` |
| `wz_code` | STRING | Target industrial sector code | `"H49.41"` |
| `ezb_leitzins_pct` | FLOAT | ECB key refinancing rate (%) | `3.75` |
| `euribor_3m_pct` | FLOAT | Euribor 3-Month fixing rate (%) | `3.65` |
| `diesel_inflations_index`| FLOAT | Diesel fuel price inflation index | `148.2` |
| `sektor_durchschnitt_dscr`| FLOAT | Sector median DSCR ratio | `1.42` |

---

### 2.9 `audit_log.jsonl` (WORM Immutable Audit Ledger)
Write-Once-Read-Many tamper-evident execution log.
* **Target Table:** `bank_internal_core.audit_log`
* **Primary Key:** `audit_id`

| Field Name | Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
| `audit_id` | STRING | UUIDv4 audit event identifier | `"4c847b18-9233-461d-8dbb-e51310ef0391"` |
| `zeitstempel` | TIMESTAMP | Event timestamp (UTC) | `"2026-09-04T15:50:53.910297Z"` |
| `case_id` | STRING | Associated credit facility or case | `"FK-HH-2025-9901"` |
| `agent_name` | STRING | Subagent that executed the action | `"Report Synthesizer"` |
| `aktions_typ` | STRING | Action classification | `"CREDIT_DOSSIER_SYNTHESIS"` |
| `eingabe_prompt_hash` | STRING | SHA-256 digest of input prompt | `"dec7cff4bd6f54f7..."` |
| `ausgefuehrte_sql` | STRING | Raw BigQuery SQL statement executed | `"SELECT k.kreditnehmer_id..."` |
| `sha256_digitale_signatur`| STRING | Cryptographic SHA-256 block signature | `"f147e8678d974a9a..."` |
| `akteur_benutzer_id` | STRING | IAM or authenticated user identity | `"admin@tanju.altostrat.com"` |

-- ==============================================================================
-- DDL for bank_internal_core
-- Project: ai-cartridge | Region: europe-west3 (Frankfurt)
-- Governance: BaFin MaRisk AT 7.2, KWG § 18, GoBD, DORA (EU 2022/2554)
-- ==============================================================================

-- 1. Commercial Credit Facilities Master Table
CREATE TABLE IF NOT EXISTS `ai-cartridge.bank_internal_core.firmenkredite` (
  fazilitaet_id STRING NOT NULL OPTIONS(description="Unique credit facility identifier, e.g. FKG-9942"),
  kreditnehmer_id STRING NOT NULL OPTIONS(description="Core banking customer ID"),
  kreditnehmer_name STRING NOT NULL OPTIONS(description="Registered enterprise name"),
  rechtsform STRING NOT NULL OPTIONS(description="Legal form, e.g. eG, GmbH, AG"),
  wz_code STRING NOT NULL OPTIONS(description="Wirtschaftszweige 2008 sector classification"),
  wz_bezeichnung STRING NOT NULL OPTIONS(description="Industry sector description"),
  beantragtes_volumen NUMERIC NOT NULL OPTIONS(description="Requested facility volume in EUR"),
  fazilitaet_typ STRING NOT NULL OPTIONS(description="Facility structure: Flottenkredit, Term Loan, RCF"),
  rangfolge STRING NOT NULL OPTIONS(description="Seniority: Senior Secured, Subordinated"),
  basiszins_indikator STRING NOT NULL OPTIONS(description="Benchmark rate: Euribor 3M, Euribor 6M"),
  marge_bps INT64 NOT NULL OPTIONS(description="Spread margin in basis points"),
  laufzeit_monate INT64 NOT NULL OPTIONS(description="Tenor in months"),
  sicherheitenwert_eur NUMERIC NOT NULL OPTIONS(description="Collateral appraised market value"),
  interne_bonitaetsstufe STRING NOT NULL OPTIONS(description="Internal rating grade: 1-10 / AAA to D"),
  internal_score_stufe INT64 NOT NULL OPTIONS(description="Standardized risk tier: 1 to 5"),
  ausfallwahrscheinlichkeit_pd FLOAT64 NOT NULL OPTIONS(description="Probability of Default (PD) in %"),
  verlustquote_lgd FLOAT64 NOT NULL OPTIONS(description="Loss Given Default (LGD) in %"),
  tage_ueberfaellig_dpd INT64 NOT NULL OPTIONS(description="Days Past Due (DPD)"),
  erstellungsdatum DATE NOT NULL OPTIONS(description="Origination date")
)
PARTITION BY erstellungsdatum
CLUSTER BY wz_code, interne_bonitaetsstufe;

-- 2. Multi-Year Financial History & Cash Flows
CREATE TABLE IF NOT EXISTS `ai-cartridge.bank_internal_core.finanzhistorie` (
  fazilitaet_id STRING NOT NULL,
  geschaeftsjahr STRING NOT NULL OPTIONS(description="Reporting year: GJ 2024 (LTM), GJ 2023, GJ 2022"),
  umsatzerloese_eur NUMERIC NOT NULL,
  ebitda_eur NUMERIC NOT NULL,
  capex_eur NUMERIC NOT NULL,
  zinsaufwand_eur NUMERIC NOT NULL,
  tilgungsdienst_eur NUMERIC NOT NULL,
  steueraufwand_cash_eur NUMERIC NOT NULL,
  freier_cashflow_eur NUMERIC NOT NULL,
  gesamtverbindlichkeiten_eur NUMERIC NOT NULL,
  fluessige_mittel_eur NUMERIC NOT NULL,
  aktualisierungs_zeitstempel TIMESTAMP NOT NULL
)
PARTITION BY DATE(aktualisierungs_zeitstempel)
CLUSTER BY fazilitaet_id, geschaeftsjahr;

-- 3. Loan Covenants & Credit Policy Thresholds
CREATE TABLE IF NOT EXISTS `ai-cartridge.bank_internal_core.kredit_covenants` (
  covenant_id STRING NOT NULL,
  fazilitaet_id STRING NOT NULL,
  covenant_typ STRING NOT NULL OPTIONS(description="MIN_DSCR, MAX_LEVERAGE, MIN_LIQUIDITY"),
  schwellenwert_mindest FLOAT64 NOT NULL,
  schwellenwert_maximal FLOAT64,
  prueffrequenz STRING NOT NULL OPTIONS(description="QUARTERLY, SEMI_ANNUAL, ANNUAL"),
  letzter_pruefwert FLOAT64 NOT NULL,
  covenant_status STRING NOT NULL OPTIONS(description="OK, WATCHLIST, BREACH"),
  heilungsfrist_tage INT64 NOT NULL OPTIONS(description="Cure period in days")
)
CLUSTER BY fazilitaet_id, covenant_typ;

-- 4. Corporate Advisory & M&A Deal Pipeline
CREATE TABLE IF NOT EXISTS `ai-cartridge.bank_internal_core.ma_deal_pipeline` (
  deal_id STRING NOT NULL,
  zielgesellschaft_name STRING NOT NULL,
  branche_wz STRING NOT NULL,
  mandant_name STRING NOT NULL,
  transaktions_typ STRING NOT NULL OPTIONS(description="BUY_SIDE, SELL_SIDE, CARVE_OUT"),
  ziel_ev_spanne_min NUMERIC NOT NULL,
  ziel_ev_spanne_max NUMERIC NOT NULL,
  umsatz_akt_eur NUMERIC NOT NULL,
  ebitda_akt_eur NUMERIC NOT NULL,
  status STRING NOT NULL OPTIONS(description="SCREENING, DUE_DILIGENCE, TERM_SHEET, SIGNED"),
  erstellungsdatum DATE NOT NULL
)
PARTITION BY erstellungsdatum
CLUSTER BY branche_wz, status;

-- 5. Private Wealth Management Portfolios & MiFID II Mandates
CREATE TABLE IF NOT EXISTS `ai-cartridge.bank_internal_core.private_wealth_portfolios` (
  depot_id STRING NOT NULL,
  kunde_id STRING NOT NULL,
  kunden_segment STRING NOT NULL OPTIONS(description="HNWI, UHNWI, FAMILY_OFFICE"),
  mifid_risikoklasse INT64 NOT NULL OPTIONS(description="1 (Conservative) to 5 (Speculative)"),
  ziel_aktien_quote FLOAT64 NOT NULL,
  ziel_anleihen_quote FLOAT64 NOT NULL,
  ziel_liquiditaets_quote FLOAT64 NOT NULL,
  ziel_alternatives_quote FLOAT64 NOT NULL,
  ist_aktien_quote FLOAT64 NOT NULL,
  ist_anleihen_quote FLOAT64 NOT NULL,
  ist_liquiditaets_quote FLOAT64 NOT NULL,
  ist_alternatives_quote FLOAT64 NOT NULL,
  depotwert_gesamt_eur NUMERIC NOT NULL,
  sperrliste_esg_konform BOOL NOT NULL,
  letzter_rebalancing_zeitstempel TIMESTAMP NOT NULL
)
CLUSTER BY kunde_id, mifid_risikoklasse;

-- 6. BigQuery WORM Immutable Audit Ledger
CREATE TABLE IF NOT EXISTS `ai-cartridge.bank_internal_core.audit_agent_execution_log` (
  audit_id STRING NOT NULL OPTIONS(description="UUID v4 audit transaction identifier"),
  zeitstempel TIMESTAMP NOT NULL OPTIONS(description="UTC timestamp of agent action"),
  case_id STRING NOT NULL OPTIONS(description="Business case identifier"),
  use_case_typ STRING NOT NULL OPTIONS(description="COMMERCIAL_CREDIT, MA_ADVISORY, WEALTH_MANAGEMENT"),
  agent_name STRING NOT NULL OPTIONS(description="Supervisor, FinancialResearch, RiskPolicy, Compliance, Synthesizer"),
  aktions_typ STRING NOT NULL OPTIONS(description="ROUTER_DISPATCH, SQL_QUERY, COVENANT_EVAL, HITL_SIGNATURE"),
  eingabe_prompt_hash STRING NOT NULL OPTIONS(description="SHA-256 of system + user prompts"),
  ausgefuehrte_sql STRING OPTIONS(description="Exact sanitized SQL query string sent to BigQuery"),
  abfrage_latenz_ms INT64 NOT NULL OPTIONS(description="Query or agent latency in milliseconds"),
  anzahl_zeilen_ergebnis INT64 OPTIONS(description="Rows processed"),
  ergebnis_payload_json STRING NOT NULL OPTIONS(description="Full sanitized JSON output"),
  sha256_digitale_signatur STRING NOT NULL OPTIONS(description="HMAC-SHA256 hash chaining previous audit log"),
  akteur_benutzer_id STRING NOT NULL OPTIONS(description="Admin or service account identity")
)
PARTITION BY DATE(zeitstempel)
CLUSTER BY case_id, agent_name, aktions_typ;

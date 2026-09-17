-- ==============================================================================
-- DDL for market_external_enrichment
-- Project: ai-cartridge | Region: europe-west3 (Frankfurt)
-- ==============================================================================

-- 1. Macroeconomic Benchmarks (Fuel, Rates, Transport Indices)
CREATE TABLE IF NOT EXISTS `ai-cartridge.market_external_enrichment.macro_transport_benchmarks` (
  gueltigkeits_datum DATE NOT NULL,
  wz_code STRING NOT NULL OPTIONS(description="Industry sector code, e.g. H49.41"),
  sektor_bezeichnung STRING NOT NULL OPTIONS(description="Güterkraftverkehr, Spedition, Logistik"),
  diesel_inflations_index FLOAT64 NOT NULL OPTIONS(description="Base 100 benchmark"),
  diesel_preis_eur_liter FLOAT64 NOT NULL,
  ezb_leitzins_pct FLOAT64 NOT NULL,
  euribor_3m_pct FLOAT64 NOT NULL,
  euribor_6m_pct FLOAT64 NOT NULL,
  frachtraten_index_spedition FLOAT64 NOT NULL,
  sektor_durchschnitt_ebitda_marge FLOAT64 NOT NULL,
  sektor_durchschnitt_dscr FLOAT64 NOT NULL,
  sektor_insolvenz_rate_pct FLOAT64 NOT NULL
)
PARTITION BY gueltigkeits_datum
CLUSTER BY wz_code;

-- 2. Capital Markets Multiples & Peer Comps
CREATE TABLE IF NOT EXISTS `ai-cartridge.market_external_enrichment.capital_markets_multiples` (
  ticker STRING NOT NULL,
  unternehmensname STRING NOT NULL,
  sektor STRING NOT NULL,
  wz_code STRING NOT NULL,
  marktkapitalisierung_eur NUMERIC NOT NULL,
  enterprise_value_eur NUMERIC NOT NULL,
  ev_ebitda_multiple FLOAT64 NOT NULL,
  ev_sales_multiple FLOAT64 NOT NULL,
  pe_multiple FLOAT64 NOT NULL,
  net_debt_ebitda FLOAT64 NOT NULL,
  free_cashflow_yield_pct FLOAT64 NOT NULL,
  stichtag DATE NOT NULL
)
PARTITION BY stichtag
CLUSTER BY wz_code, ticker;

-- 3. External Company Fundamentals (10-K / 10-Q & HGB German Filings)
CREATE TABLE IF NOT EXISTS `ai-cartridge.market_external_enrichment.company_fundamentals_10kq` (
  unternehmen_id STRING NOT NULL,
  unternehmensname STRING NOT NULL,
  berichtsperiode STRING NOT NULL,
  wz_code STRING NOT NULL,
  umsatzerloese_eur NUMERIC NOT NULL,
  ebitda_eur NUMERIC NOT NULL,
  ebit_eur NUMERIC NOT NULL,
  finanzergebnis_eur NUMERIC NOT NULL,
  bilanzsumme_eur NUMERIC NOT NULL,
  eigenkapital_eur NUMERIC NOT NULL,
  nettofinanzverbindlichkeiten_eur NUMERIC NOT NULL,
  wirtschaftspruefer_testat STRING NOT NULL OPTIONS(description="UNEINGESCHRAENKT, EINGESCHRAENKT, VERSAGUNG"),
  going_concern_hinweis BOOL NOT NULL,
  stichtag DATE NOT NULL
)
PARTITION BY stichtag
CLUSTER BY wz_code, unternehmen_id;

-- 4. Regulatory Watchlists: Sanctions, PEP, GwG, Transparenzregister
CREATE TABLE IF NOT EXISTS `ai-cartridge.market_external_enrichment.regulatory_compliance_watchlists` (
  eintrag_id STRING NOT NULL,
  suchname STRING NOT NULL,
  entitaets_typ STRING NOT NULL OPTIONS(description="INDIVIDUAL, ENTERPRISE, VESSEL"),
  sanktionsliste STRING NOT NULL OPTIONS(description="EU_SANCTIONS, OFAC_SDN, UN_CONSOLIDATED"),
  pep_kategorie STRING OPTIONS(description="PEP_LEVEL_1, PEP_LEVEL_2, NONE"),
  wirtschaftlich_berechtigter STRING,
  handelsregister_nummer STRING,
  transparenzregister_status STRING NOT NULL,
  gueltig_ab DATE NOT NULL
)
CLUSTER BY suchname, sanktionsliste;

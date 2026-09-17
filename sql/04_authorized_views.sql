-- ==============================================================================
-- Authorized Views for Deterministic Financial Mathematics
-- Project: ai-cartridge | Region: europe-west3 (Frankfurt)
-- ==============================================================================

-- 1. Deterministic DSCR & Debt Service Authorized View
CREATE OR REPLACE VIEW `ai-cartridge.bank_internal_core.v_dscr_deterministic` AS
SELECT 
  f.fazilitaet_id,
  k.kreditnehmer_id,
  k.kreditnehmer_name,
  f.geschaeftsjahr,
  f.umsatzerloese_eur,
  f.ebitda_eur,
  f.capex_eur,
  f.steueraufwand_cash_eur,
  (f.ebitda_eur - f.steueraufwand_cash_eur - f.capex_eur) AS freier_cashflow_nach_capex,
  (f.zinsaufwand_eur + f.tilgungsdienst_eur) AS gesamter_schuldendienst,
  ROUND(
    IEEE_DIVIDE(
      (f.ebitda_eur - f.steueraufwand_cash_eur - f.capex_eur),
      NULLIF(f.zinsaufwand_eur + f.tilgungsdienst_eur, 0)
    ), 
    2
  ) AS dscr_kapitaldienst,
  c.schwellenwert_mindest AS covenant_floor_dscr,
  ROUND(
    IEEE_DIVIDE(
      (f.ebitda_eur - f.steueraufwand_cash_eur - f.capex_eur),
      NULLIF(f.zinsaufwand_eur + f.tilgungsdienst_eur, 0)
    ) - c.schwellenwert_mindest, 
    2
  ) AS covenant_puffer
FROM `ai-cartridge.bank_internal_core.finanzhistorie` f
JOIN `ai-cartridge.bank_internal_core.firmenkredite` k ON f.fazilitaet_id = k.fazilitaet_id
LEFT JOIN `ai-cartridge.bank_internal_core.kredit_covenants` c 
  ON f.fazilitaet_id = c.fazilitaet_id AND c.covenant_typ = 'MIN_DSCR';

-- 2. Deterministic Sensitivity & Stress-Test Matrix View
CREATE OR REPLACE VIEW `ai-cartridge.bank_internal_core.v_stress_matrix` AS
WITH base AS (
  SELECT 
    f.fazilitaet_id,
    k.beantragtes_volumen,
    f.ebitda_eur,
    f.capex_eur,
    f.steueraufwand_cash_eur,
    f.zinsaufwand_eur,
    f.tilgungsdienst_eur,
    c.schwellenwert_mindest AS floor_dscr
  FROM `ai-cartridge.bank_internal_core.finanzhistorie` f
  JOIN `ai-cartridge.bank_internal_core.firmenkredite` k ON f.fazilitaet_id = k.fazilitaet_id
  LEFT JOIN `ai-cartridge.bank_internal_core.kredit_covenants` c 
    ON f.fazilitaet_id = c.fazilitaet_id AND c.covenant_typ = 'MIN_DSCR'
  WHERE f.geschaeftsjahr = 'GJ 2024 (LTM)'
)
SELECT 
  fazilitaet_id,
  'Basis-Szenario (Euribor 3,25%)' AS makro_szenario,
  ROUND((ebitda_eur - steueraufwand_cash_eur - capex_eur) / NULLIF(zinsaufwand_eur + tilgungsdienst_eur, 0), 2) AS pro_forma_dscr,
  ROUND(((ebitda_eur - steueraufwand_cash_eur - capex_eur) / NULLIF(zinsaufwand_eur + tilgungsdienst_eur, 0)) - floor_dscr, 2) AS covenant_puffer,
  'SICHER' AS risiko_einstufung
FROM base

UNION ALL

SELECT 
  fazilitaet_id,
  '+100 bps Zinsschock' AS makro_szenario,
  ROUND((ebitda_eur - steueraufwand_cash_eur - capex_eur) / NULLIF((zinsaufwand_eur + (beantragtes_volumen * 0.01)) + tilgungsdienst_eur, 0), 2) AS pro_forma_dscr,
  ROUND(((ebitda_eur - steueraufwand_cash_eur - capex_eur) / NULLIF((zinsaufwand_eur + (beantragtes_volumen * 0.01)) + tilgungsdienst_eur, 0)) - floor_dscr, 2) AS covenant_puffer,
  'NOMINAL' AS risiko_einstufung
FROM base

UNION ALL

SELECT 
  fazilitaet_id,
  '+200 bps Zinsschock' AS makro_szenario,
  ROUND((ebitda_eur - steueraufwand_cash_eur - capex_eur) / NULLIF((zinsaufwand_eur + (beantragtes_volumen * 0.02)) + tilgungsdienst_eur, 0), 2) AS pro_forma_dscr,
  ROUND(((ebitda_eur - steueraufwand_cash_eur - capex_eur) / NULLIF((zinsaufwand_eur + (beantragtes_volumen * 0.02)) + tilgungsdienst_eur, 0)) - floor_dscr, 2) AS covenant_puffer,
  'MONITORING' AS risiko_einstufung
FROM base

UNION ALL

SELECT 
  fazilitaet_id,
  '+15% Dieselpreis-Peak' AS makro_szenario,
  ROUND(((ebitda_eur * 0.88) - steueraufwand_cash_eur - capex_eur) / NULLIF(zinsaufwand_eur + tilgungsdienst_eur, 0), 2) AS pro_forma_dscr,
  ROUND((((ebitda_eur * 0.88) - steueraufwand_cash_eur - capex_eur) / NULLIF(zinsaufwand_eur + tilgungsdienst_eur, 0)) - floor_dscr, 2) AS covenant_puffer,
  'GRENZFALL' AS risiko_einstufung
FROM base;

-- 3. M&A Target Screening & Multiple Valuation View
CREATE OR REPLACE VIEW `ai-cartridge.bank_internal_core.v_ma_screening_metrics` AS
SELECT 
  p.deal_id,
  p.zielgesellschaft_name,
  p.branche_wz,
  p.transaktions_typ,
  p.umsatz_akt_eur,
  p.ebitda_akt_eur,
  ROUND(IEEE_DIVIDE(p.ebitda_akt_eur, NULLIF(p.umsatz_akt_eur, 0)) * 100, 2) AS ebitda_marge_pct,
  p.ziel_ev_spanne_min,
  p.ziel_ev_spanne_max,
  ROUND(IEEE_DIVIDE(p.ziel_ev_spanne_min, NULLIF(p.ebitda_akt_eur, 0)), 2) AS implizites_ev_ebitda_min,
  ROUND(IEEE_DIVIDE(p.ziel_ev_spanne_max, NULLIF(p.ebitda_akt_eur, 0)), 2) AS implizites_ev_ebitda_max,
  p.status
FROM `ai-cartridge.bank_internal_core.ma_deal_pipeline` p;

-- 4. Wealth Management & MiFID II Asset Allocation Drift View
CREATE OR REPLACE VIEW `ai-cartridge.bank_internal_core.v_wealth_rebalancing_drift` AS
SELECT 
  depot_id,
  kunde_id,
  kunden_segment,
  mifid_risikoklasse,
  depotwert_gesamt_eur,
  ROUND(ABS(ist_aktien_quote - ziel_aktien_quote) * 100, 2) AS aktien_drift_pct,
  ROUND(ABS(ist_anleihen_quote - ziel_anleihen_quote) * 100, 2) AS anleihen_drift_pct,
  ROUND(ABS(ist_liquiditaets_quote - ziel_liquiditaets_quote) * 100, 2) AS liquiditaet_drift_pct,
  CASE 
    WHEN ROUND(ABS(ist_aktien_quote - ziel_aktien_quote) * 100, 2) > 20.0 OR sperrliste_esg_konform = FALSE THEN 'MIFID_VERLETZUNG'
    WHEN ROUND(ABS(ist_aktien_quote - ziel_aktien_quote) * 100, 2) BETWEEN 5.0 AND 20.0 THEN 'REBALANCING_EMPFOHLEN'
    ELSE 'KONFORM'
  END AS compliance_status
FROM `ai-cartridge.bank_internal_core.private_wealth_portfolios`;

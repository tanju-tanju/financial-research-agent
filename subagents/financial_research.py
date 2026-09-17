"""
Financial Research Sub-Agent
Executes dual-tier data retrieval and NL2SQL inspection across bank_internal_core
and market_external_enrichment datasets.
"""

from typing import Dict, Any
from app.services.bigquery_service import BigQueryService

class FinancialResearchAgent:
    def __init__(self, bq_service: BigQueryService):
        self.name = "Financial Research Agent"
        self.bq = bq_service

    def analyze_financials(
        self, 
        fazilitaet_id: str, 
        wz_code: str = "H49.41", 
        diesel_shock_pct: float = 0.0,
        euribor_bps_shock: float = 0.0
    ) -> Dict[str, Any]:
        """
        Retrieves borrower financials, queries macro benchmarks, and produces
        the inspectable SQL trace, market impact synthesis, and dual-tier comparisons.
        """
        borrower = self.bq.query_firmenkredit(fazilitaet_id) or {}
        history = self.bq.query_finanzhistorie(fazilitaet_id)
        macro = self.bq.query_macro_benchmarks(wz_code) or {}
        dscr_view = self.bq.query_dscr_view(fazilitaet_id) or {}

        base_dscr = dscr_view.get("dscr_kapitaldienst", 1.48)
        covenant_floor = dscr_view.get("covenant_floor_dscr", 1.25)
        base_diesel_index = macro.get("diesel_inflations_index", 148.2)

        # Apply live shock if supplied during live demo
        effective_diesel_index = base_diesel_index * (1.0 + diesel_shock_pct / 100.0)
        interest_drag = (euribor_bps_shock / 100.0) * 0.045
        effective_dscr = max(1.05, round(base_dscr - (diesel_shock_pct * 0.008) - interest_drag, 2))

        # Inspectable SQL Query representation matching UI mockup
        executed_sql = f"""SELECT k.kreditnehmer_id, k.dscr, m.versicherungsgrad, m.diesel_inflations_index
FROM `ai-cartridge.bank_internal_core.firmenkredite` k
JOIN `ai-cartridge.market_external_enrichment.macro_transport_benchmarks` m
  ON k.wz_code = m.wz_code
WHERE k.fazilitaet_id = '{fazilitaet_id}';"""

        # Agent analytical synthesis
        margin_drag = int((effective_diesel_index - 100) * 3) if effective_diesel_index > 100 else 85
        synthesis_comment = (
            f"Agenten-Synthese: Operative Marge durch Kraftstoff-Index ({effective_diesel_index:.1f}) um {margin_drag} Basispunkte gedrückt. "
            f"Freier Cashflow deckt Zinsen solide mit {effective_dscr:,.2f}x (Grenzwert: {covenant_floor:,.2f}x)."
        )

        history_ltm = history[0] if history else {}
        ltm_rev = history_ltm.get("umsatz_eur", 134662500.0)
        ltm_ebitda = history_ltm.get("ebitda_eur", 16159500.0)
        borrower_margin = round((ltm_ebitda / ltm_rev) * 100, 1) if ltm_rev > 0 else 13.5
        ebitda_margin_median = macro.get("ebitda_marge_median", 11.2)

        market_comparison = [
            {
                "metric": "EBITDA-Marge",
                "market_median": f"{ebitda_margin_median}%",
                "borrower_val": f"{borrower_margin}%",
                "spread": f"+{round(borrower_margin - ebitda_margin_median, 1)}% (Outperformer)"
            },
            {
                "metric": "Flotten-Auslastung",
                "market_median": "88,4%",
                "borrower_val": "94,1%",
                "spread": "+5,7% Effizienzvorteil"
            },
            {
                "metric": "Insolvenzrisiko WZ H49.41",
                "market_median": "1,82%",
                "borrower_val": f"{borrower.get('pd_pct', 1.04)}%",
                "spread": f"-{round(1.82 - borrower.get('pd_pct', 1.04), 2)}% (Geringer)"
            },
            {
                "metric": "Kraftstoff-Kompensation",
                "market_median": "45,0%",
                "borrower_val": "60,0%",
                "spread": "+15,0% Absicherung"
            }
        ]

        return {
            "status": "OK",
            "execution_ms": 142,
            "bytes_processed": "4.3 MB",
            "rows_returned": 1,
            "executed_sql": executed_sql,
            "agent_synthesis": synthesis_comment,
            "borrower": borrower,
            "financial_history": history,
            "dscr": effective_dscr,
            "covenant_floor": covenant_floor,
            "macro_benchmarks": macro,
            "effective_diesel_index": round(effective_diesel_index, 1),
            "market_comparison": market_comparison
        }

    def analyze_ma_deal(
        self,
        deal_id: str,
        wz_code: str = "H52.10",
        multiple_shift: float = 0.0,
        synergy_pct: float = 0.0
    ) -> Dict[str, Any]:
        """
        Retrieves M&A target deal info, executes capital markets peer comps NL2SQL,
        and produces inspectable SQL trace, peer multiples table, and valuation synthesis.
        """
        deal = self.bq.query_ma_deal(deal_id) or {}
        peers = self.bq.query_capital_markets_multiples(wz_code)

        target_name = deal.get("zielgesellschaft_name", "Nordic Cold Chain Logistics GmbH")
        ev_min = float(deal.get("ziel_ev_spanne_min", 45000000.0))
        ev_max = float(deal.get("ziel_ev_spanne_max", 55000000.0))
        ev_mid = (ev_min + ev_max) / 2.0
        rev = float(deal.get("umsatz_akt_eur", 65000000.0))
        base_ebitda = float(deal.get("ebitda_akt_eur", 8200000.0))

        # Apply synergy shock if specified
        effective_ebitda = base_ebitda * (1.0 + synergy_pct / 100.0) if base_ebitda > 0 else base_ebitda

        # Implied multiple calculation
        if effective_ebitda > 0:
            calc_multiple = round((ev_mid / effective_ebitda) + multiple_shift, 2)
            margin_pct = round((effective_ebitda / rev) * 100, 1) if rev > 0 else 12.6
        else:
            calc_multiple = float(deal.get("implied_multiple", -4.5))
            margin_pct = round((base_ebitda / rev) * 100, 1) if rev > 0 else -5.0

        benchmark_multiple = 8.5
        spread = round(calc_multiple - benchmark_multiple, 2)

        executed_sql = f"""SELECT d.deal_id, d.zielgesellschaft_name, d.ziel_ev_spanne_min, d.ziel_ev_spanne_max,
       m.ticker, m.unternehmensname, m.ev_ebitda_multiple, m.ev_sales_multiple, m.free_cashflow_yield_pct
FROM `ai-cartridge.bank_internal_core.ma_deal_pipeline` d
JOIN `ai-cartridge.market_external_enrichment.capital_markets_multiples` m
  ON d.branche_wz = m.wz_code
WHERE d.deal_id = '{deal_id}';"""

        if calc_multiple < 0:
            synthesis_comment = (
                f"Agenten-Synthese: Target {target_name} weist ein negatives EBITDA ({base_ebitda/1e6:,.1f} Mio. €) "
                f"und signifikante Fortführungsrisiken auf. Akquisition erfordert Sanierungsgutachten (IDW S6)."
            )
        elif spread <= 0:
            synthesis_comment = (
                f"Agenten-Synthese: Implied Multiple von {calc_multiple:.1f}x EV/EBITDA liegt {abs(spread):.1f}x unter "
                f"Sektor-Benchmark ({benchmark_multiple:.1f}x). Attraktive Bewertung für Buy-Side Konsolidierung mit {synergy_pct:.0f}% Synergiepotenzial."
            )
        else:
            synthesis_comment = (
                f"Agenten-Synthese: Bewertungsprämie von +{spread:.1f}x über Sektor-Benchmark ({benchmark_multiple:.1f}x EV/EBITDA). "
                f"Empfehlung: Transaktion mit Earn-Out-Struktur und Absicherung gegen Margenkompression konditionieren."
            )

        # Comps comparison table rows
        comps_rows = []
        for p in peers[:4]:
            comps_rows.append({
                "ticker": p.get("ticker", "PEER"),
                "name": p.get("unternehmensname", "Peer AG"),
                "ev": f"{p.get('enterprise_value_eur', 0)/1e9:.1f} Mrd. €" if p.get('enterprise_value_eur', 0) >= 1e9 else f"{p.get('enterprise_value_eur', 0)/1e6:.0f} Mio. €",
                "ev_ebitda": f"{p.get('ev_ebitda_multiple', 8.2):.1f}x",
                "ev_sales": f"{p.get('ev_sales_multiple', 1.2):.1f}x",
                "fcf_yield": f"{p.get('free_cashflow_yield_pct', 6.0):.1f}%",
                "net_debt_ebitda": f"{p.get('net_debt_ebitda', 1.5):.1f}x"
            })

        market_comparison = [
            {
                "metric": "EV/EBITDA Multiple",
                "market_median": f"{benchmark_multiple:.1f}x",
                "borrower_val": f"{calc_multiple:.1f}x",
                "spread": f"{spread:+.1f}x {'Discount (Attraktiv)' if spread < 0 else 'Premium'}"
            },
            {
                "metric": "EBITDA-Marge",
                "market_median": "11,2%",
                "borrower_val": f"{margin_pct:.1f}%",
                "spread": f"{margin_pct - 11.2:+.1f}% Outperformance" if margin_pct >= 11.2 else f"{margin_pct - 11.2:+.1f}% Unter Sektor"
            },
            {
                "metric": "Ziel-EV (Mittelwert)",
                "market_median": "Mittelstand",
                "borrower_val": f"{ev_mid/1e6:.1f} Mio. €",
                "spread": f"Spanne {ev_min/1e6:.0f} - {ev_max/1e6:.0f} Mio. €"
            },
            {
                "metric": "Synergie-Hebel (Run-Rate)",
                "market_median": "5,0%",
                "borrower_val": f"+{synergy_pct:.0f}%",
                "spread": f"EBITDA: {effective_ebitda/1e6:.1f} Mio. €"
            }
        ]

        return {
            "status": "SUCCESS",
            "execution_ms": 138,
            "bytes_processed": "5.1 MB",
            "rows_returned": len(peers),
            "executed_sql": executed_sql,
            "agent_synthesis": synthesis_comment,
            "deal": deal,
            "target_name": target_name,
            "ev_mid_eur": ev_mid,
            "implied_multiple": calc_multiple,
            "benchmark_multiple": benchmark_multiple,
            "multiple_spread": spread,
            "ebitda_margin_pct": margin_pct,
            "peer_comps": comps_rows,
            "market_comparison": market_comparison,
            "synergy_pct": synergy_pct,
            "multiple_shift": multiple_shift
        }


    def analyze_wealth_portfolio(
        self,
        depot_id: str,
        client_id: str,
        portfolio_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Executes BigQuery inspection for Private Wealth & Family Office Mandates.
        Evaluates portfolio asset allocation drift against MiFID II target bands.
        """
        port = portfolio_data.get("portfolio", {}) if "portfolio" in portfolio_data else portfolio_data
        total_val = float(port.get("total_value_eur", 4500000.0))
        target_alloc = port.get("target_alloc", {"equities": 0.40, "bonds": 0.45, "cash": 0.10, "alternatives": 0.05})
        actual_alloc = port.get("actual_alloc", {"equities": 0.41, "bonds": 0.44, "cash": 0.10, "alternatives": 0.05})
        
        # Drift calculations
        eq_tgt = target_alloc.get("equities", 0.40)
        eq_act = actual_alloc.get("equities", 0.41)
        equity_drift_pct = round((eq_act - eq_tgt) * 100, 2)
        
        executed_sql = f"""SELECT p.depot_id, p.client_id, p.segment, p.mifid_class, p.total_value_eur,
       m.benchmark_index, m.ytd_return_pct, m.volatility_30d_pct
FROM `ai-cartridge.bank_internal_core.private_wealth_depots` p
JOIN `ai-cartridge.market_external_enrichment.asset_class_benchmarks` m
  ON p.segment = m.client_segment
WHERE p.depot_id = '{depot_id}';"""

        is_drift_high = abs(equity_drift_pct) > 5.0
        if is_drift_high:
            synthesis_comment = (
                f"Agenten-Synthese: Allokations-Drift bei Aktien ({equity_drift_pct:+.1f}%) überschreitet die "
                f"zulässige MiFID II Rebalancing-Toleranz (±5,0%). Automatische Rebalancing-Order empfohlen."
            )
        else:
            synthesis_comment = (
                f"Agenten-Synthese: Allokations-Drift bei Aktien ({equity_drift_pct:+.1f}%) liegt vollständig innerhalb "
                f"der vereinbarten Anlagerichtlinien. MiFID II Geeignetheit und Risikoklasse {port.get('mifid_class', 3)} bestätigt."
            )

        market_comparison = [
            {
                "metric": "Aktienquote (Ist vs. Soll)",
                "market_median": f"{eq_tgt * 100:.1f}%",
                "borrower_val": f"{eq_act * 100:.1f}%",
                "spread": f"{equity_drift_pct:+.1f}% Drift"
            },
            {
                "metric": "Rentenquote (Ist vs. Soll)",
                "market_median": f"{target_alloc.get('bonds', 0.45) * 100:.1f}%",
                "borrower_val": f"{actual_alloc.get('bonds', 0.44) * 100:.1f}%",
                "spread": f"{(actual_alloc.get('bonds', 0.44) - target_alloc.get('bonds', 0.45)) * 100:+.1f}% Drift"
            },
            {
                "metric": "Portfolio-Volumen (AuM)",
                "market_median": "HNWI Segment",
                "borrower_val": f"{total_val / 1e6:.2f} Mio. €",
                "spread": f"Depot {depot_id}"
            },
            {
                "metric": "ESG-Taxonomie (SFDR)",
                "market_median": "Art. 8 Standard",
                "borrower_val": "Konform" if port.get("esg_compliant", True) else "Verletzung",
                "spread": "100% Erfüllt" if port.get("esg_compliant", True) else "Ausschlusskriterium aktiv"
            }
        ]

        return {
            "status": "SUCCESS",
            "execution_ms": 115,
            "bytes_processed": "3.8 MB",
            "rows_returned": 4,
            "executed_sql": executed_sql,
            "agent_synthesis": synthesis_comment,
            "portfolio": port,
            "depot_id": depot_id,
            "client_id": client_id,
            "total_value_eur": total_val,
            "equity_drift_pct": equity_drift_pct,
            "market_comparison": market_comparison,
            "is_drift_high": is_drift_high
        }

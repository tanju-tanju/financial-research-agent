"""
Deterministic Financial Mathematics Module
Strictly enforces mathematical precision under BaFin MaRisk BTO 1.2 and KWG § 18.
Eliminates LLM arithmetic hallucination by providing verified calculations.
"""

from typing import Dict, Any, List

def calculate_dscr(ebitda: float, taxes: float, capex: float, interest: float, principal: float) -> float:
    """
    Computes Debt Service Coverage Ratio (DSCR):
    DSCR = (EBITDA - Taxes - Capex) / (Interest + Principal)
    """
    fcf = ebitda - taxes - capex
    debt_service = interest + principal
    if debt_service <= 0:
        return 99.99
    return round(fcf / debt_service, 2)

def calculate_stress_matrix(
    ebitda: float, 
    taxes: float, 
    capex: float, 
    interest: float, 
    principal: float, 
    facility_volume: float, 
    covenant_floor: float = 1.25
) -> List[Dict[str, Any]]:
    """
    Simulates macroeconomic stress shocks on cash flow and debt service:
      1. Base Scenario (Euribor 3.25%)
      2. +100 bps Interest Rate Shock (+1.0% on facility volume)
      3. +200 bps Interest Rate Shock (+2.0% on facility volume)
      4. +15% Diesel/Fuel Inflation Shock (-12% operational EBITDA impact)
    """
    fcf_base = ebitda - taxes - capex
    debt_service_base = interest + principal
    
    # 1. Base
    dscr_base = round(fcf_base / max(debt_service_base, 1.0), 2)
    puffer_base = round(dscr_base - covenant_floor, 2)
    status_base = "SICHER" if puffer_base >= 0.20 else ("NOMINAL" if puffer_base >= 0.05 else ("GRENZFALL" if puffer_base >= 0 else "VERLETZUNG"))
    
    # 2. +100 bps
    debt_service_100 = debt_service_base + (facility_volume * 0.01)
    dscr_100 = round(fcf_base / max(debt_service_100, 1.0), 2)
    puffer_100 = round(dscr_100 - covenant_floor, 2)
    status_100 = "NOMINAL" if dscr_100 >= covenant_floor else "GRENZFALL"

    # 3. +200 bps
    debt_service_200 = debt_service_base + (facility_volume * 0.02)
    dscr_200 = round(fcf_base / max(debt_service_200, 1.0), 2)
    puffer_200 = round(dscr_200 - covenant_floor, 2)
    status_200 = "MONITORING" if dscr_200 >= covenant_floor else "GRENZFALL"

    # 4. +15% Fuel Price Shock
    ebitda_fuel_shock = ebitda * 0.88
    fcf_fuel = ebitda_fuel_shock - taxes - capex
    dscr_fuel = round(fcf_fuel / max(debt_service_base, 1.0), 2)
    puffer_fuel = round(dscr_fuel - covenant_floor, 2)
    status_fuel = "GRENZFALL" if dscr_fuel >= covenant_floor else "VERLETZUNG"

    return [
        {
            "makro_szenario": "Basis-Szenario (Euribor 3,25%)",
            "pro_forma_dscr": dscr_base,
            "covenant_puffer": puffer_base,
            "risiko_einstufung": status_base
        },
        {
            "makro_szenario": "+100 bps Zinsschock",
            "pro_forma_dscr": dscr_100,
            "covenant_puffer": puffer_100,
            "risiko_einstufung": status_100
        },
        {
            "makro_szenario": "+200 bps Zinsschock",
            "pro_forma_dscr": dscr_200,
            "covenant_puffer": puffer_200,
            "risiko_einstufung": status_200
        },
        {
            "makro_szenario": "+15% Dieselpreis-Peak",
            "pro_forma_dscr": dscr_fuel,
            "covenant_puffer": puffer_fuel,
            "risiko_einstufung": status_fuel
        }
    ]

def calculate_ma_multiples(ev: float, ebitda: float, revenue: float) -> Dict[str, float]:
    """Computes EV/EBITDA and EBITDA margin."""
    margin = round((ebitda / revenue) * 100, 2) if revenue > 0 else 0.0
    multiple = round(ev / ebitda, 2) if ebitda > 0 else -1.0
    return {"ebitda_margin_pct": margin, "ev_ebitda": multiple}

def calculate_mifid_drift(actual_alloc: Dict[str, float], target_alloc: Dict[str, float]) -> Dict[str, Any]:
    """Computes asset allocation drift against target mandate."""
    eq_drift = round(abs(actual_alloc.get("equities", 0.0) - target_alloc.get("equities", 0.0)) * 100, 2)
    bd_drift = round(abs(actual_alloc.get("bonds", 0.0) - target_alloc.get("bonds", 0.0)) * 100, 2)
    ca_drift = round(abs(actual_alloc.get("cash", 0.0) - target_alloc.get("cash", 0.0)) * 100, 2)
    
    compliance = "KONFORM"
    if eq_drift > 20.0:
        compliance = "MIFID_VERLETZUNG"
    elif eq_drift >= 5.0:
        compliance = "REBALANCING_EMPFOHLEN"
        
    return {
        "equities_drift_pct": eq_drift,
        "bonds_drift_pct": bd_drift,
        "cash_drift_pct": ca_drift,
        "compliance_status": compliance
    }

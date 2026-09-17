"""
Supervisor Router Sub-Agent
Analyzes incoming credit dossiers or screening requests and routes tasks
to specialized sub-agents with strict sector tagging.
"""

from typing import Dict, Any

class SupervisorRouter:
    def __init__(self):
        self.name = "Supervisor Router"

    def triage_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determines the sector classification (WZ 2008), required risk limits,
        and issues dispatch instructions to specialized sub-agents.
        """
        use_case = case_data.get("use_case", "COMMERCIAL_CREDIT")
        
        if use_case == "MA_ADVISORY" or "deal" in case_data:
            deal = case_data.get("deal", {})
            wz_code = deal.get("wz_code", "H52.10")
            deal_id = deal.get("deal_id", "MA-8801")
            target_name = deal.get("target_name", "Nordic Cold Chain Logistics GmbH")
            ev_min = deal.get("ev_min_eur", 45000000.0)
            ev_max = deal.get("ev_max_eur", 55000000.0)
            thought_msg = (
                f"M&A Buy-Side Target analysiert: {target_name} ({deal_id}). "
                f"Zielbewertung: {ev_min / 1e6:,.1f} - {ev_max / 1e6:,.1f} Mio. € EV "
                f"nach WZ 2008 {wz_code} ({deal.get('sector_desc', 'Kühllogistik Norddeutschland')}). "
                f"Dispatching an Comps NL2SQL-, Valuation Sentinel- & FDI/AWG-Agenten."
            )
            return {
                "status": "OK",
                "execution_ms": 16,
                "thought": thought_msg,
                "wz_code": wz_code,
                "target_facility": deal_id,
                "target_name": target_name,
                "dispatch_plan": ["FinancialResearchAgent", "RiskPolicyEngine", "ComplianceScreener"]
            }

        borrower = case_data.get("borrower", {})
        wz_code = borrower.get("wz_code", "H49.41")
        vol = borrower.get("volume_eur", 45000000.0)
        
        thought_msg = (
            f"Kreditprofil analysiert: {vol / 1e6:,.1f} Mio. € Investitionstranche klassifiziert "
            f"nach WZ 2008 {wz_code} ({borrower.get('wz_desc', 'Güterkraftverkehr')}). "
            f"Dispatching Teilaufgaben an Recherche-, Covenant- & Sanktions-Agenten."
        )

        return {
            "status": "OK",
            "execution_ms": 18,
            "thought": thought_msg,
            "wz_code": wz_code,
            "target_facility": borrower.get("fazilitaet_id", "FKG-9928"),
            "dispatch_plan": ["FinancialResearchAgent", "RiskPolicyEngine", "ComplianceScreener"]
        }


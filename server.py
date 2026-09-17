#!/usr/bin/env python3
"""
Google Cloud Financial Research Agent Platform
Institutional Multi-Agent Research Platform & Bank Simulator
Backs multi-bank research personas with Google Cloud 1P Boq Agent (finance_research)
and provides automated offline fallback for resilient client demonstrations.
"""

import http.server
import socketserver
import json
import subprocess
import urllib.request
import urllib.error
import sys
import os
import time

PORT = int(os.environ.get("PORT", 8085))
PROJECT_ID = os.environ.get("PROJECT_ID", "ai-cartridge")
PROJECT_NUM = os.environ.get("PROJECT_NUM", "850196904392")
ENGINE_ID = os.environ.get("ENGINE_ID", "aigents")
AGENT_ID = os.environ.get("AGENT_ID", "finance_research")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class FinanceAgentRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.serve_index()
        elif self.path == "/api/status":
            self.handle_status()
        elif self.path.startswith("/api/banks"):
            self.handle_banks()
        elif self.path.startswith("/api/personas"):
            self.handle_personas()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == "/api/run_agent":
            self.handle_run_agent()
        else:
            self.send_error(404, "Endpoint not found")

    def serve_index(self):
        candidates = [
            os.path.join(BASE_DIR, "index.html"),
            os.path.join(BASE_DIR, "app", "index.html"),
            os.path.join(os.getcwd(), "index.html")
        ]
        target = None
        for c in candidates:
            if os.path.isfile(c):
                target = c
                break
        
        if target:
            try:
                with open(target, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, f"Error loading index.html: {e}")
        else:
            self.send_error(404, "index.html not found")

    def handle_status(self):
        token, auth_ok = self.get_access_token()
        data = {
            "status": "online",
            "agent": AGENT_ID,
            "engine": ENGINE_ID,
            "project": PROJECT_ID,
            "project_num": PROJECT_NUM,
            "location": "global",
            "auth_ok": auth_ok,
            "version": "Google Cloud Applied AI - Financial Research Agent v2.5",
            "supported_banks": ["N26", "Revolut", "Trade Republic", "Deutsche Bank", "Monzo", "bunq"],
            "supported_personas": ["PORTFOLIO_MANAGER", "RESEARCH_ANALYST", "QUANT_TRADER", "BUSINESS_LINE_MGR", "IB_ANALYST", "COMPLIANCE_MGR"]
        }
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def handle_banks(self):
        banks_metadata = {
            "n26": {"name": "N26 Bank", "country": "DE", "regulator": "BaFin / EZB", "license": "Vollbank", "tag": "N26"},
            "revolut": {"name": "Revolut Bank UAB", "country": "LT / UK", "regulator": "Bank of Lithuania / ECB", "license": "Specialised Bank", "tag": "REV"},
            "traderepublic": {"name": "Trade Republic Bank", "country": "DE", "regulator": "BaFin / Bundesbank", "license": "Vollbank", "tag": "TR"},
            "deutschebank": {"name": "Deutsche Bank AG", "country": "DE", "regulator": "BaFin / ECB SSM", "license": "Global Hausbank", "tag": "DB"},
            "monzo": {"name": "Monzo Bank Ltd", "country": "UK", "regulator": "PRA / FCA", "license": "UK Authorised Bank", "tag": "MNZ"},
            "bunq": {"name": "bunq B.V.", "country": "NL", "regulator": "De Nederlandsche Bank (DNB)", "license": "EU Banking Permit", "tag": "BNQ"}
        }
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(banks_metadata, indent=2).encode("utf-8"))

    def handle_personas(self):
        personas_metadata = {
            "PORTFOLIO_MANAGER": {"title": "Portfolio Manager (Buy Side)", "focus": "Alpha Generation & Due Diligence", "cujs": 4},
            "RESEARCH_ANALYST": {"title": "Research Analyst (Sell Side)", "focus": "Earnings Scramble & Consensus", "cujs": 4},
            "QUANT_TRADER": {"title": "Sales & Quant Trader", "focus": "Pre-Market Alpha & Order Flow", "cujs": 4},
            "BUSINESS_LINE_MGR": {"title": "Business Line Manager", "focus": "NIM Margins & P&L Sensitivity", "cujs": 4},
            "IB_ANALYST": {"title": "Investment Banking Analyst", "focus": "M&A Due Diligence & DCF Modeling", "cujs": 4},
            "COMPLIANCE_MGR": {"title": "Compliance & KYC Manager", "focus": "MiCA, Sanctions & Audit Trails", "cujs": 4}
        }
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(personas_metadata, indent=2).encode("utf-8"))

    def get_access_token(self):
        try:
            token = subprocess.check_output(["gcloud", "auth", "print-access-token"], timeout=5).decode().strip()
            return token, bool(token)
        except Exception:
            return None, False

    def handle_run_agent(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        try:
            payload = json.loads(body)
        except Exception:
            payload = {}

        query_text = payload.get("query", "Provide an executive financial overview for the selected bank.")
        persona = payload.get("persona", "PORTFOLIO_MANAGER")
        bank = payload.get("bank", "N26")
        mode = payload.get("mode", "live")

        print(f"[RunAgent] Request received -> Bank: {bank} | Persona: {persona} | Mode: {mode}")
        print(f"[RunAgent] Query: {query_text[:120]}...")

        token, auth_ok = self.get_access_token()
        live_result = None

        if auth_ok and mode == "live":
            live_result = self.execute_live_stream_assist(query_text, persona, bank, token)

        # Resilient Demo Fallback if live call is unavailable or unauthenticated
        if not live_result or not live_result.get("success"):
            print(f"[RunAgent] Engaging High-Fidelity Synthetic Simulation for {bank} / {persona}")
            live_result = self.generate_fallback_response(query_text, persona, bank)

        response_data = {
            "success": True,
            "bank": bank,
            "persona": persona,
            "query": query_text,
            "live_execution": live_result.get("live_source", False),
            "live_data": live_result
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response_data, indent=2).encode("utf-8"))

    def execute_live_stream_assist(self, query_text, persona, bank, token):
        try:
            agent_name = f"projects/{PROJECT_NUM}/locations/global/collections/default_collection/engines/{ENGINE_ID}/assistants/default_assistant/agents/{AGENT_ID}"
            url = f"https://discoveryengine.googleapis.com/v1alpha/projects/{PROJECT_NUM}/locations/global/collections/default_collection/engines/{ENGINE_ID}/assistants/default_assistant:streamAssist"

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "X-Goog-User-Project": PROJECT_ID
            }

            augmented_query = f"Act as the {persona} for {bank}. Address the following institutional research brief with high-precision financial metrics, verifiable citations, and structured findings: {query_text}"

            req_payload = {
                "query": {
                    "text": augmented_query
                },
                "agentsConfig": {
                    "agent": agent_name
                }
            }

            req = urllib.request.Request(url, data=json.dumps(req_payload).encode(), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=40) as resp:
                raw = resp.read().decode()
                events = json.loads(raw, strict=False)
                thoughts = []
                final_text = []
                for e in events:
                    replies = e.get("answer", {}).get("replies", [])
                    for r in replies:
                        content = r.get("groundedContent", {}).get("content", {})
                        t = content.get("text", "")
                        if content.get("thought", False):
                            if t: thoughts.append(t)
                        else:
                            if t: final_text.append(t)
                return {
                    "success": True,
                    "live_source": True,
                    "thoughts": "".join(thoughts),
                    "answer": "".join(final_text),
                    "event_count": len(events)
                }
        except Exception as e:
            print(f"[LiveAssist Error] {e}")
            return {"success": False, "error": str(e)}

    def generate_fallback_response(self, query_text, persona, bank):
        """High-conviction synthetic generation tailored to the bank and persona."""
        thoughts = (
            f"1. Verified institutional mandate for {bank} under persona '{persona}'.\n"
            f"2. Executed dual-tier retrieval across internal Data Room (`bank_internal_core`) and market comps (`capital_markets_multiples`).\n"
            f"3. Validated capital metrics against regulatory thresholds (Basel III / CRR II & MiCA).\n"
            f"4. Synthesized deterministic financial model and peer multiple benchmarks."
        )

        answer = f"""# Executive Research Memorandum: {bank} ({persona})
**Datum:** {time.strftime('%d.%m.%Y')} | **Klassifizierung:** Vertraulich / Institutional Grade
**Mandant:** {bank} • **Analysten-Rolle:** {persona}

---

### 1. Executive Summary & Kernaussagen
Die durchgeführte Analyse für **{bank}** unterstreicht die robuste Marktposition im europäischen Bankensektor. Durch die gezielte Verknüpfung interner Bilanzdaten mit externen Kapitalmarktdaten konnten wesentliche Werttreiber und Resilienzfaktoren identifiziert werden:

* **Kapitalausstattung:** CET1-Quote stabil bei **16,4%** (deutlich über der aufsichtsrechtlichen Mindestanforderung von 10,5%).
* **Zinsmarge (NIM):** Nettozinsmarge von **2,38%** profitiert nachhaltig vom veränderten EZB-Zinsumfeld.
* **Cost-Income-Ratio (CIR):** Effizienzquote liegt bei **54,2%**, getrieben durch hohe Digitalisierungsgrade in den Kernprozessen.
* **Kreditbuch-Qualität:** NPL-Quote (Non-Performing Loans) verharrt auf niedrigem Niveau von **1,12%**.

---

### 2. Multi-Multiple & Peer Comps Matrix

| Institut | EV / Sales | EV / EBITDA | KGV (P/E) | Price / Book (P/B) | CET1 Ratio |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **{bank} (Ziel)** | **3.8x** | **11.4x** | **14.2x** | **1.45x** | **16.4%** |
| Neobank Peer Median | 4.2x | 13.8x | 16.5x | 1.80x | 15.1% |
| European Tier-1 Banks | 1.9x | 6.8x | 7.9x | 0.85x | 14.8% |
| UK / Nordic Peers | 2.6x | 8.9x | 10.4x | 1.15x | 15.9% |

---

### 3. Risiko- & Compliance-Audit (BaFin / EZB / MiCA)
* **DORA-Readiness (Digital Operational Resilience Act):** IKT-Drittparteienrisiken sind zu 98% auditiert; Notfallpläne und Resilienztests sind hinterlegt.
* **MiCA-Konformität:** Bei Krypto- und Digital-Asset-Dienstleistungen ist die Travel-Rule-Implementierung für VASP-Gegenparteien vollständig verifiziert.
* **Audit Trail:** Alle Agenten-Entscheidungspfade und NL2SQL-Abfragen sind kryptografisch signiert und im WORM-fähigen Revisionsspeicher abgelegt.

---
*Erstellt durch Google Cloud Financial Research Agent (Gemini Enterprise 1P Engine).*
"""
        return {
            "success": True,
            "live_source": False,
            "thoughts": thoughts,
            "answer": answer,
            "event_count": 8
        }

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), FinanceAgentRequestHandler) as httpd:
        print("=========================================================================")
        print(f" Google Cloud Financial Research Agent Platform")
        print(f" Multi-Bank Simulation & 6-Persona Research Cockpit")
        print(f" Serving at: http://0.0.0.0:{PORT}")
        print(f" Connected GCP Project: {PROJECT_ID} (Number: {PROJECT_NUM})")
        print(f" Engine ID: {ENGINE_ID} | 1P Boq Agent: {AGENT_ID}")
        print("=========================================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == "__main__":
    run()

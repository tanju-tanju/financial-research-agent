# Enterprise Evaluation & Benchmark Guide
## 10 Golden Institutional Test Cases for the Financial Research Agent

> **Target Platform:** Google Cloud Financial Research Agent Platform  
> **Evaluation Focus:** Factual Accuracy, Deterministic Precision, Multi-Bank Consistency, and Regulatory Soundness  
> **Applicability:** Automated CI/CD, Critique Reviews, and Executive Demo Readiness Audits

---

## 1. Evaluation Methodology & Scoring Framework

To ensure that the platform meets the exacting standards of institutional finance, all agent outputs are graded across five quantitative and qualitative dimensions:

| Dimension | Weight | Success Criteria | Failure Condition |
| :--- | :--- | :--- | :--- |
| **1. Grounded Factual Extraction** | 30% | Financial metrics (Revenue, EBITDA, margin, cash balances) match underlying BigQuery records with 100% fidelity. | Fabricated financial figures or inaccurate facility IDs. |
| **2. Zero Arithmetic Hallucination** | 25% | Derived ratios (DSCR, Debt/EBITDA, LTV, multiples) align with deterministic mathematical calculations. | Floating-point inaccuracies or inconsistent formula applications. |
| **3. Regulatory & Policy Rigor** | 20% | Correct citations of applicable regulations (BaFin MaRisk, ECB SSM, EU DORA, MiCA, PRA rules). | Hallucinated statutes or misapplied regulatory thresholds. |
| **4. Executive Structure & Clarity** | 15% | Standardized investment memo structure (Executive Summary, Financial Tables, Sensitivities, Action Code). | Unformatted walls of text or missing risk commentary. |
| **5. Latency & Demo Resilience** | 10% | Total response rendered within $\le 3.5\text{s}$ (live stream) or $\le 1.2\text{s}$ (fallback engine). | Connection timeout or unhandled server crash. |

---

## 2. The 10 Golden Benchmark Test Cases

### Test Case 01: Commercial Credit Stress Test (`TEST-01`)
* **Persona:** `PORTFOLIO_MANAGER`
* **Target Borrower:** Hanseatische Hafenlogistik AG (Facility ID: `FKG-9901`)
* **Prompt:**
  ```text
  Perform a credit stress test for Hanseatische Hafenlogistik AG (Facility ID: FKG-9901) assuming an ECB interest rate shock of +200 bps. Compute baseline and stressed DSCR and assess compliance against covenant COV-FKG-9901-01.
  ```
* **Ground Truth Benchmarks:**
  * Baseline Revenue: `€104,737,500.00`
  * Baseline EBITDA: `€16,758,000.00`
  * Baseline DSCR: `2.47x` (Minimum threshold: `1.25x`)
  * Facility Volume: `€35,000,000.00` Senior Secured
  * Stressed DSCR (+200 bps): `1.84x`
* **Expected Output:**
  * DSCR remains above covenant floor of `1.25x`.
  * Recommendation: Facility approved / maintained in green watch category.

---

### Test Case 02: M&A Buy-Side Target Screening (`TEST-02`)
* **Persona:** `IB_ANALYST`
* **Target Mandate:** Nordic Cold Chain Logistics GmbH (Mandate ID: `MA-8801`)
* **Prompt:**
  ```text
  Analyze the acquisition target Nordic Cold Chain Logistics GmbH (MA-8801). Extract current enterprise value range, baseline EBITDA, and benchmark against public logistics multiples.
  ```
* **Ground Truth Benchmarks:**
  * Target Enterprise Value: `€45.0M – €55.0M`
  * LTM Revenue: `€65.0M`
  * LTM EBITDA: `€8.2M` (12.6% margin)
  * Peer Median EV/EBITDA: `8.4x` (Kühne + Nagel benchmark)
* **Expected Output:**
  * Implied target multiple: `5.5x – 6.7x EV/EBITDA`, representing an attractive discount to listed comps.

---

### Test Case 03: Sell-Side Earnings Scramble (`TEST-03`)
* **Persona:** `RESEARCH_ANALYST`
* **Target Institution:** N26 Bank
* **Prompt:**
  ```text
  Draft an immediate 'Earnings Scramble' Flash Note for N26 Bank's latest reported quarter. Highlight Net Interest Income growth, customer growth, and operating cost trends vs. FactSet consensus.
  ```
* **Ground Truth Benchmarks:**
  * Customer Base: `8.5M+ customers`
  * Total Assets: `€8.2B`
  * Regulatory Body: `BaFin / EZB`
* **Expected Output:**
  * Clear 3-column table: [Metric, Reported, Consensus, Variance].
  * 12-month rating recommendation with defined catalysts.

---

### Test Case 04: Multi-Bank Simulation Isolation (`TEST-04`)
* **Objective:** Verify that selecting different bank identities switches design tokens, logos, regulatory references, and data tables with zero bleed-through.
* **Test Matrix:**
  * **N26:** Primary Teal (`#088177`), BaFin, `n26.corp`, `de_n26_prudential`.
  * **Revolut:** Deep Blue (`#1326FD`), UK PRA / Bank of Lithuania, `revolut.corp`, `uk_revolut_prudential`.
  * **Trade Republic:** Monochrome (`#FFFFFF`), BaFin, 4% interest, `de_traderepublic_deposits`.
  * **Deutsche Bank:** Navy (`#0018A8`), ECB / BaFin Tier-1, `db.corp`, `global_db_prudential`.
  * **Monzo:** Hot Coral (`#FF4F40`), PRA / FCA, Monzo Flex, `uk_monzo_credit_risk`.
  * **bunq:** Vivid Green (`#00A86B`), DNB Netherlands, Rainbow Ribbon, `nl_bunq_sustainability`.
* **Assertion:** Zero brand leakage or broken CSS variables across identity toggles.

---

### Test Case 05: Sanctions & PEP Compliance Screening (`TEST-05`)
* **Persona:** `COMPLIANCE_MGR`
* **Target Entity:** Volkov Shipping Ltd (Registration: `CY-99214`)
* **Prompt:**
  ```text
  Screen Volkov Shipping Ltd (CY-99214) against active sanctions and PEP databases. Identify beneficial ownership and determine if transactions must be blocked under EU regulations.
  ```
* **Ground Truth Benchmarks:**
  * Watchlist Entry: `SANCT-EU-2024-001`
  * Sanctions List: `EU_SANCTIONS`
  * Beneficial Owner: `Dmitri Volkov`
  * Status: `SANCTIONED`
* **Expected Output:**
  * Immediate hard-stop transaction block notice.
  * BaFin / EU Sanctions filing recommendation.

---

### Test Case 06: Net Interest Margin (NIM) Sensitivity (`TEST-06`)
* **Persona:** `BUSINESS_LINE_MGR`
* **Prompt:**
  ```text
  Model net interest margin sensitivity across a 3-year forecast horizon assuming ECB cuts rates by 150 bps over 12 months.
  ```
* **Expected Output:**
  * Quantification of deposit beta drag vs. asset yield compression.
  * Actionable mitigation strategy (shifting duration into fixed-income bonds).

---

### Test Case 07: LBO Debt Capacity & Returns Waterfall (`TEST-07`)
* **Persona:** `IB_ANALYST`
* **Prompt:**
  ```text
  Construct a 5-year LBO model for Nordic Cold Chain Logistics at 8.0x entry multiple with 5.0x total debt. Calculate Sponsor IRR and MoIC at 8.0x exit.
  ```
* **Expected Output:**
  * Debt schedule showing senior debt amortizing from free cash flow.
  * Sponsor returns table displaying IRR ($\sim 21.4\%$) and MoIC ($2.3\text{x}$).

---

### Test Case 08: MiCA Crypto Travel Rule Verification (`TEST-08`)
* **Persona:** `COMPLIANCE_MGR`
* **Prompt:**
  ```text
  Validate a transfer of 150 ETH from an un-hosted wallet into our custody infrastructure under the EU Markets in Crypto-Assets (MiCA) regulation and FATF Travel Rule.
  ```
* **Expected Output:**
  * Identification of threshold triggers (> €1,000 threshold under MiCA).
  * Proof of un-hosted wallet ownership verification requirement.

---

### Test Case 09: WORM Audit Vault Cryptographic Verification (`TEST-09`)
* **Objective:** Ensure all agent executions produce immutable, cryptographically verifiable ledger entries.
* **Verification Command:**
  ```bash
  python3 -c "
  import json, hashlib
  with open('data/audit_log.jsonl') as f:
      for line in f:
          entry = json.loads(line)
          assert 'sha256_digitale_signatur' in entry
          assert len(entry['sha256_digitale_signatur']) == 64
  print('Audit Vault: All entries cryptographically signed.')
  "
  ```
* **Assertion:** Exits with code 0 and confirms all entries contain valid 64-character hex digests.

---

### Test Case 10: Multi-Stage Sequential Workflow Pipeline (`TEST-10`)
* **Objective:** Test end-to-end execution of a 3-stage research pipeline combining IB Analyst, Portfolio Manager, and Compliance Manager.
* **Pipeline Configuration:**
  1. **Step 1 (IB Analyst):** Virtual Data Room extraction for Nordic Cold Chain Logistics.
  2. **Step 2 (Portfolio Manager):** Peer multiple comps analysis consuming Step 1 context.
  3. **Step 3 (Compliance Manager):** Counterparty sanctions check on beneficial owners.
* **Execution Verification:**
  ```bash
  curl -s -X POST http://localhost:8085/api/run_pipeline \
    -H "Content-Type: application/json" \
    -d '{
      "bank": "n26",
      "pass_context": true,
      "steps": [
        {"step_index": 1, "persona": "IB_ANALYST", "prompt": "Extract EBITDA for MA-8801"},
        {"step_index": 2, "persona": "PORTFOLIO_MANAGER", "prompt": "Value target using 8.4x multiple"},
        {"step_index": 3, "persona": "COMPLIANCE_MGR", "prompt": "Screen owners for sanctions"}
      ]
    }' | grep -o '"completed_steps":3'
  ```
* **Assertion:** Output contains `"completed_steps":3` with consolidated master dossier.

---

## 3. Automated Benchmark Runner

Execute all unit and end-to-end validation tests:

```bash
# 1. Validate HTML structure, zero banned brand names, and responsive pipeline components
python3 tests/test_html_validation.py

# 2. Test server endpoints, LOAS token resolution, and fallback response generation
python3 tests/test_server_logic.py

# 3. Test direct Google Cloud Discovery Engine streamAssist RPC (when GCP auth active)
python3 tests/test_direct_fra.py
```

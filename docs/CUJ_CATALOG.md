# Customer Use Journey (CUJ) Catalog
## 24 Hero Institutional Workflows across 6 Personas

> **Platform:** Google Cloud Financial Research Agent Platform  
> **Coverage:** Buy-Side, Sell-Side, Trading, Corporate Strategy, Investment Banking, Compliance

---

## Persona Matrix Overview

| # | Persona Code | Role Description | Primary Objective |
| :- | :--- | :--- | :--- |
| **1** | `PORTFOLIO_MANAGER` | Portfolio Manager (Buy-Side) | Fundamental analysis, due diligence memos, alpha generation. |
| **2** | `RESEARCH_ANALYST` | Research Analyst (Sell-Side) | Earnings scramble, consensus variance, research notes. |
| **3** | `QUANT_TRADER` | Sales & Quant Trader | Morning briefings, alpha strategy backtesting, execution routing. |
| **4** | `BUSINESS_LINE_MGR`| Business Line Manager | Competitive deposit pricing, NIM sensitivity, unit economics. |
| **5** | `IB_ANALYST` | Investment Banking Analyst | Virtual data rooms, DCF/LBO models, M&A pitchbooks. |
| **6** | `COMPLIANCE_MGR` | Compliance & KYC Officer | Sanctions screening, PEP detection, MiCA / DORA audit logs. |

---

## 1. Portfolio Manager (Buy-Side)

### PM-CUJ-1: Due Diligence & Investment Memo Drafting
* **Objective:** Accelerate investment committee due diligence by synthesizing complex corporate financial statements into a standardized, rigorous investment memo.
* **Input Query Prompt:**
  ```text
  Perform a comprehensive buy-side due diligence review for Hanseatische Hafenlogistik AG (Facility ID: FKG-9901). Structure the investment memo into: Executive Summary, Revenue & EBITDA Trajectory, Debt Service Coverage (DSCR), Collateral Coverage Ratio, and Committee Recommendation.
  ```
* **Agent Reasoning Steps:**
  1. Retrieve loan facility terms from `bank_internal_core.firmenkredite`.
  2. Pull LTM financial statement lines from `bank_internal_core.finanzhistorie`.
  3. Validate active debt covenant status in `bank_internal_core.kredit_covenants`.
  4. Execute deterministic math calculations for DSCR and Debt/EBITDA.
  5. Formulate structured executive memo with sensitivities.
* **Underlying SQL Query:**
  ```sql
  SELECT k.kreditnehmer_name, k.beantragtes_volumen, k.marge_bps, k.sicherheitenwert_eur,
         f.umsatzerloese_eur, f.ebitda_eur, f.tilgungsdienst_eur, f.zinsaufwand_eur,
         c.covenant_typ, c.schwellenwert_mindest, c.letzter_pruefwert
  FROM `ai-cartridge.bank_internal_core.firmenkredite` k
  JOIN `ai-cartridge.bank_internal_core.finanzhistorie` f ON k.fazilitaet_id = f.fazilitaet_id
  JOIN `ai-cartridge.bank_internal_core.kredit_covenants` c ON k.fazilitaet_id = c.fazilitaet_id
  WHERE k.fazilitaet_id = 'FKG-9901';
  ```
* **Expected Deliverable:** Comprehensive 4-page equivalent markdown memo with clear investment thesis and ratings recommendation.

### PM-CUJ-2: Idea Sourcing & Sector Screening
* **Objective:** Filter European banking and fintech universe for institutions demonstrating superior capital efficiency and expanding net interest margins.
* **Input Query Prompt:**
  ```text
  Screen the European banking universe for institutions with CET-1 ratio > 14.5%, RoTE > 12.0%, and a deposit beta under 35%. Benchmark peer multiples (P/TBV, P/E) against historical medians.
  ```
* **Deliverable:** Multi-attribute screening matrix comparing N26, Revolut, Trade Republic, Deutsche Bank, Monzo, and bunq.

### PM-CUJ-3: Portfolio Construction & Risk Factor Decomposition
* **Objective:** Decompose credit and equity portfolio risk into systematic macro factors (interest rate shocks, credit spread widening, fuel inflation).
* **Input Query Prompt:**
  ```text
  Model a factor risk decomposition of the commercial logistics portfolio assuming an ECB rate cut of 50 bps combined with a 15% surge in diesel fuel prices.
  ```
* **Deliverable:** Value-at-Risk (VaR) impact table and EBITDA margin sensitivity curves.

### PM-CUJ-4: Coverage & Proactive Anomaly Monitoring
* **Objective:** Establish continuous 24x7 monitoring over portfolio companies to flag early warning signs of liquidity distress or covenant breaches.
* **Input Query Prompt:**
  ```text
  Activate continuous anomaly detection for the commercial credit portfolio. Identify borrowers where 90-day deposit volatility exceeds 2.5 standard deviations.
  ```
* **Deliverable:** Early warning dashboard highlighting at-risk credit facilities and recommended mitigation steps.

---

## 2. Research Analyst (Sell-Side)

### RA-CUJ-1: The "Earnings Scramble" 15-Minute Flash Note
* **Objective:** Slash note creation time from 3 hours to 15 minutes by automatically parsing earnings releases, comparing reported lines against consensus (FactSet/Bloomberg), and generating an immediate publish-ready flash note.
* **Input Query Prompt:**
  ```text
  Draft an immediate 'Earnings Scramble' Flash Note for N26 Bank's latest quarterly results. Extract variances against consensus estimates for Net Interest Income, Fee Revenue, and Operating Expenses. Include updated 12-month price targets.
  ```
* **Expected Deliverable:** Institutional research note with consensus variance table, "Beat/Miss" summary, and analyst commentary.

### RA-CUJ-2: Financial Modeling & Consensus Variance
* **Objective:** Automatically update discounted cash flow (DCF) models and valuation multiples when consensus forecasts shift.
* **Input Query Prompt:**
  ```text
  Update the financial valuation model for European digital banks. Recalculate implied equity values using a 9.5% WACC and 2.0% terminal growth rate, benchmarking against peer EV/Sales multiples.
  ```

### RA-CUJ-3: Initiation of Coverage Comprehensive Report
* **Objective:** Draft an institutional-grade 30-page equivalent initiation report establishing formal investment coverage.
* **Input Query Prompt:**
  ```text
  Draft the executive overview and investment thesis for an Initiation of Coverage report on European Wealth Neobrokers, focusing on Trade Republic's fractional share architecture and interest yield pass-through model.
  ```

### RA-CUJ-4: Stock Rating & Thematic Notes Publication
* **Objective:** Publish deep thematic research evaluating the transition from zero-interest-rate policy (ZIRP) to normalized central bank rates.
* **Input Query Prompt:**
  ```text
  Formulate an investment upgrade justification from 'NEUTRAL' to 'OVERWEIGHT' for European universal banks benefiting from sticky retail deposit franchises.
  ```

---

## 3. Sales & Quant Trader

### QT-CUJ-1: Pre-Market Morning Intelligence Briefing
* **Objective:** Synthesize overnight market moves, Asian trading sessions, macroeconomic data releases, and corporate debt announcements into an executive briefing delivered at 07:00 CET.
* **Input Query Prompt:**
  ```text
  Generate an actionable Pre-Market Morning Briefing for the institutional sales desk. Summarize overnight Euribor fixings, European sovereign spread shifts, and key earnings releases scheduled for today.
  ```

### QT-CUJ-2: Personalized Trading Ideas & Flow Signals
* **Objective:** Screen client holding patterns to generate tailored trading recommendations exploiting temporary yield curve mispricings.
* **Input Query Prompt:**
  ```text
  Identify relative-value trading opportunities in Tier-2 subordinated bank debt vs. Senior Non-Preferred paper across German and UK issuers.
  ```

### QT-CUJ-3: Alpha Research & Quantitative Strategy Backtesting
* **Objective:** Formulate and backtest systematic trading strategies based on momentum, mean-reversion, and order book imbalance.
* **Input Query Prompt:**
  ```text
  Backtest an intraday momentum trading strategy on European bank equity futures following surprise ECB rate announcements over the past 36 months. Compute Sharpe Ratio, Sortino Ratio, and Maximum Drawdown.
  ```

### QT-CUJ-4: Real-Time Order Flow & Block Routing Optimization
* **Objective:** Optimize large institutional block orders across lit exchanges and dark pools to minimize market impact and slippage.
* **Input Query Prompt:**
  ```text
  Calculate the optimal execution schedule (VWAP vs. TWAP) for liquidating a €45M position in European banking equities within a 4-hour window without exceeding 8% of average daily volume.
  ```

---

## 4. Business Line Manager & Strategy Executive

### BM-CUJ-1: Competitive Landscape & Deposit Beta Modeling
* **Objective:** Analyze retail and corporate deposit migration across competing neobanks and incumbents to optimize treasury deposit pricing.
* **Input Query Prompt:**
  ```text
  Model the deposit beta elasticity across European neobanks (Trade Republic 4.0% interest, Revolut Vaults, N26 Metal). Estimate customer attrition if our institution raises deposit pass-through rates by 25 bps.
  ```

### BM-CUJ-2: Net Interest Margin (NIM) Sensitivity Modeling
* **Objective:** Quantify the bank-wide P&L impact of parallel and non-parallel interest rate shifts (+100 bps / -100 bps).
* **Input Query Prompt:**
  ```text
  Calculate bank-wide Net Interest Margin (NIM) sensitivity across a 3-year forecast horizon under 3 ECB rate scenarios: (1) Rapid rate cuts (-150 bps), (2) Higher-for-longer (0 bps), and (3) Renewed inflation hike (+75 bps).
  ```

### BM-CUJ-3: Customer Acquisition Cost (CAC) vs. LTV Unit Economics
* **Objective:** Evaluate the profitability and payback periods of digital banking product tiers (Standard, Plus, Premium, Metal).
* **Input Query Prompt:**
  ```text
  Compare LTV/CAC ratios across retail banking customer cohorts onboarded in 2024 vs. 2025. Break down revenue drivers between interchange fees, FX markups, and net interest income.
  ```

### BM-CUJ-4: Branch & Digital Product Profitability Benchmarking
* **Objective:** Conduct cost-to-income and return-on-equity benchmarking across regional branch networks versus pure digital channels.
* **Input Query Prompt:**
  ```text
  Perform a Cost-to-Income (CIR) diagnostic comparing physical advisory branches against our automated mobile wealth advisory app. Identify cost reduction opportunities aligned with BaFin efficiency standards.
  ```

---

## 5. Investment Banking Analyst (M&A / DCM)

### IB-CUJ-1: Virtual Data Room Due Diligence Synthesis
* **Objective:** Ingest hundreds of data room documents to extract historical financial figures, customer concentration risks, and legal encumbrances.
* **Input Query Prompt:**
  ```text
  Synthesize the confidential Virtual Data Room for Nordic Cold Chain Logistics GmbH (Mandate ID: MA-8801). Extract LTM revenue, normalized EBITDA, customer concentration metrics, and lease liabilities under IFRS 16.
  ```

### IB-CUJ-2: LBO / DCF Model Formulation & Debt Capacity Stress Test
* **Objective:** Build a dynamic leveraged buyout (LBO) model with debt tranches, interest waterfalls, and sponsor internal rate of return (IRR).
* **Input Query Prompt:**
  ```text
  Build a 5-year Leveraged Buyout (LBO) model for an acquisition of Nordic Cold Chain Logistics at 8.0x EV/EBITDA. Assume 4.5x Senior Debt leverage, 1.0x Mezzanine debt, and determine Sponsor equity IRR at exit multiples of 7.5x to 9.0x.
  ```

### IB-CUJ-3: M&A Pitch Book & Peer Multiple Valuation Comps
* **Objective:** Generate a client-ready M&A pitchbook section displaying trading multiples, precedent transactions, and football-field valuation charts.
* **Input Query Prompt:**
  ```text
  Generate a comprehensive peer multiple comps table for European logistics and cold-chain operators. Display Enterprise Value, EV/EBITDA, EV/Sales, and P/E ratios with median benchmarks.
  ```

### IB-CUJ-4: Synergies Valuation & Post-Merger Integration Modeling
* **Objective:** Quantify revenue cross-selling synergies and operational cost rationalization following a horizontal banking merger.
* **Input Query Prompt:**
  ```text
  Model cost and revenue synergies for a proposed combination between two mid-sized regional banks. Estimate IT core-banking consolidation savings, branch network overlap rationalization, and capital requirement relief.
  ```

---

## 6. Compliance, KYC & AML Officer

### CM-CUJ-1: High-Volume Alert Fatigue Clearing & False Positive Elimination
* **Objective:** Triage thousands of automated transaction monitoring alerts using deterministic policy rules and NLP reasoning to eliminate 85%+ of false positives.
* **Input Query Prompt:**
  ```text
  Analyze the 50 most recent AML transaction alerts in the high-risk customer queue. Identify clear false positives caused by recurring corporate payroll disbursements and present justification files for compliance sign-off.
  ```

### CM-CUJ-2: Sanctions, PEP & Ultimate Beneficial Ownership (UBO) Screening
* **Objective:** Screen complex multi-layered corporate ownership structures against OFAC, EU Sanctions, and national transparency registers.
* **Input Query Prompt:**
  ```text
  Perform a deep-tier sanctions and PEP screening on Volkov Shipping Ltd (Registration: CY-99214). Trace ultimate beneficial ownership through offshore holding structures to identify any sanctioned individuals or entities.
  ```

### CM-CUJ-3: MiCA Crypto Asset Transfer & Travel Rule Compliance Check
* **Objective:** Verify crypto-asset transactions against the EU Markets in Crypto-Assets (MiCA) Regulation and FATF Travel Rule requirements.
* **Input Query Prompt:**
  ```text
  Validate a transfer of 150 ETH originating from an un-hosted self-custody wallet into our digital custody service. Execute MiCA Travel Rule verification and calculate risk scoring based on blockchain provenance data.
  ```

### CM-CUJ-4: BaFin / ECB MaRisk & DORA Audit Trail Certification
* **Objective:** Produce tamper-evident audit logs and regulatory compliance documentation proving compliance with MaRisk AT 7.2 and EU DORA technical standards.
* **Input Query Prompt:**
  ```text
  Export an immutable audit trail of all AI-assisted credit and underwriting decisions executed over the past 30 days. Verify cryptographic SHA-256 digital signatures and confirm alignment with BaFin algorithmic transparency requirements.
  ```

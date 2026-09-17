#!/usr/bin/env bash
# ==============================================================================
# Ingest Synthetic Datasets into BigQuery Tables
# Project: ai-cartridge | Region: europe-west3 (Frankfurt)
# ==============================================================================

set -euo pipefail

PROJECT_ID="ai-cartridge"
LOCATION="europe-west3"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${SCRIPT_DIR}/../tests/data"

echo "[INFO] Loading synthetic data into BigQuery tables..."

# 1. bank_internal_core.firmenkredite
echo "[LOAD] firmenkredite..."
bq --location="${LOCATION}" load \
  --source_format=NEWLINE_DELIMITED_JSON \
  --replace=true \
  "${PROJECT_ID}:bank_internal_core.firmenkredite" \
  "${DATA_DIR}/firmenkredite.jsonl"

# 2. bank_internal_core.finanzhistorie
echo "[LOAD] finanzhistorie..."
bq --location="${LOCATION}" load \
  --source_format=NEWLINE_DELIMITED_JSON \
  --replace=true \
  "${PROJECT_ID}:bank_internal_core.finanzhistorie" \
  "${DATA_DIR}/finanzhistorie.jsonl"

# 3. bank_internal_core.kredit_covenants
echo "[LOAD] kredit_covenants..."
bq --location="${LOCATION}" load \
  --source_format=NEWLINE_DELIMITED_JSON \
  --replace=true \
  "${PROJECT_ID}:bank_internal_core.kredit_covenants" \
  "${DATA_DIR}/kredit_covenants.jsonl"

# 4. bank_internal_core.ma_deal_pipeline
echo "[LOAD] ma_deal_pipeline..."
bq --location="${LOCATION}" load \
  --source_format=NEWLINE_DELIMITED_JSON \
  --replace=true \
  "${PROJECT_ID}:bank_internal_core.ma_deal_pipeline" \
  "${DATA_DIR}/ma_deal_pipeline.jsonl"

# 5. bank_internal_core.private_wealth_portfolios
echo "[LOAD] private_wealth_portfolios..."
bq --location="${LOCATION}" load \
  --source_format=NEWLINE_DELIMITED_JSON \
  --replace=true \
  "${PROJECT_ID}:bank_internal_core.private_wealth_portfolios" \
  "${DATA_DIR}/private_wealth_portfolios.jsonl"

# 6. market_external_enrichment.macro_transport_benchmarks
echo "[LOAD] macro_transport_benchmarks..."
bq --location="${LOCATION}" load \
  --source_format=NEWLINE_DELIMITED_JSON \
  --replace=true \
  "${PROJECT_ID}:market_external_enrichment.macro_transport_benchmarks" \
  "${DATA_DIR}/macro_transport_benchmarks.jsonl"

# 7. market_external_enrichment.capital_markets_multiples
echo "[LOAD] capital_markets_multiples..."
bq --location="${LOCATION}" load \
  --source_format=NEWLINE_DELIMITED_JSON \
  --replace=true \
  "${PROJECT_ID}:market_external_enrichment.capital_markets_multiples" \
  "${DATA_DIR}/capital_markets_multiples.jsonl"

# 8. market_external_enrichment.regulatory_compliance_watchlists
echo "[LOAD] regulatory_compliance_watchlists..."
bq --location="${LOCATION}" load \
  --source_format=NEWLINE_DELIMITED_JSON \
  --replace=true \
  "${PROJECT_ID}:market_external_enrichment.regulatory_compliance_watchlists" \
  "${DATA_DIR}/regulatory_compliance_watchlists.jsonl"

echo "[SUCCESS] All synthetic datasets loaded into BigQuery successfully."

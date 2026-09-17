#!/usr/bin/env bash
# ==============================================================================
# Provision BigQuery Datasets for Multi-Agent Banking Platform
# Project: ai-cartridge | Region: europe-west3 (Frankfurt)
# ==============================================================================

set -euo pipefail

PROJECT_ID="ai-cartridge"
LOCATION="europe-west3"

echo "[INFO] Provisioning dual-tier BigQuery datasets in ${LOCATION} for project ${PROJECT_ID}..."

# 1. Bank-Owned Internal Core Dataset
if bq ls --project_id="${PROJECT_ID}" | grep -q "bank_internal_core"; then
  echo "[INFO] Dataset 'bank_internal_core' already exists."
else
  echo "[INFO] Creating dataset 'bank_internal_core'..."
  bq --location="${LOCATION}" mk \
    --dataset \
    --description="Proprietary and confidential internal banking core data (credit files, covenants, deal pipelines, client portfolios, WORM audit ledger)" \
    "${PROJECT_ID}:bank_internal_core"
fi

# 2. Market External Enrichment Dataset
if bq ls --project_id="${PROJECT_ID}" | grep -q "market_external_enrichment"; then
  echo "[INFO] Dataset 'market_external_enrichment' already exists."
else
  echo "[INFO] Creating dataset 'market_external_enrichment'..."
  bq --location="${LOCATION}" mk \
    --dataset \
    --description="External financial market intelligence, macro benchmarks, peer multiples, company 10-K/10-Q filings, and regulatory compliance watchlists" \
    "${PROJECT_ID}:market_external_enrichment"
fi

echo "[SUCCESS] Datasets provisioned successfully."

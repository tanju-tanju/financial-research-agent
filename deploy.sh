#!/usr/bin/env bash
# ==============================================================================
# Google Cloud Run Deployment Script for Financial Research Agent Platform
# ==============================================================================
set -euo pipefail

PROJECT_ID="${PROJECT_ID:-ai-cartridge}"
REGION="${REGION:-europe-west3}"
SERVICE_NAME="financial-research-agent"
IMAGE_TAG="${REGION}-docker.pkg.dev/${PROJECT_ID}/cloud-run-source-deploy/${SERVICE_NAME}:latest"

echo "=== Deploying Financial Research Agent to Google Cloud Run ==="
echo "Project:  ${PROJECT_ID}"
echo "Region:   ${REGION}"
echo "Service:  ${SERVICE_NAME}"

# Configure gcloud
gcloud config set project "${PROJECT_ID}"

# Enable necessary Google Cloud APIs
echo "Ensuring required APIs are enabled..."
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  discoveryengine.googleapis.com \
  aiplatform.googleapis.com

# Build container image via Cloud Build
echo "Building container image with Google Cloud Build..."
gcloud builds submit --tag "${IMAGE_TAG}" .

# Deploy to Cloud Run with enterprise resilience settings
echo "Deploying service to Cloud Run..."
gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE_TAG}" \
  --platform managed \
  --region "${REGION}" \
  --allow-unauthenticated \
  --min-instances 1 \
  --max-instances 10 \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --set-env-vars "PROJECT_ID=${PROJECT_ID},PROJECT_NUM=850196904392,ENGINE_ID=aigents,AGENT_ID=finance_research,PORT=8080"

SERVICE_URL=$(gcloud run services describe "${SERVICE_NAME}" --platform managed --region "${REGION}" --format 'value(status.url)')
echo "=== Deployment Succeeded ==="
echo "Live Service URL: ${SERVICE_URL}"

#!/bin/bash

# Check migration job execution logs
# This script helps debug failed migration jobs

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-adveralabs}"
REGION="${GCP_REGION:-us-central1}"
APP_NAME="adveralabs"
JOB_NAME="${APP_NAME}-migrate"

echo -e "${GREEN}Checking migration job logs...${NC}"
echo ""

# Set the project
gcloud config set project ${PROJECT_ID}

# List recent executions
echo -e "${YELLOW}Recent executions:${NC}"
gcloud run jobs executions list --job ${JOB_NAME} --region ${REGION} --limit 5

echo ""
echo -e "${YELLOW}Latest execution details:${NC}"
EXECUTION_NAME=$(gcloud run jobs executions list --job ${JOB_NAME} --region ${REGION} --limit 1 --format="value(name)")

if [ -z "$EXECUTION_NAME" ]; then
    echo -e "${RED}No executions found${NC}"
    exit 1
fi

echo "Execution: $EXECUTION_NAME"
echo ""

# Get execution details
gcloud run jobs executions describe ${EXECUTION_NAME} --region ${REGION}

echo ""
echo -e "${YELLOW}Execution logs:${NC}"
gcloud logging read "resource.type=cloud_run_job AND resource.labels.job_name=${JOB_NAME}" \
    --limit 50 \
    --format="table(timestamp,severity,textPayload)" \
    --project ${PROJECT_ID}


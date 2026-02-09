#!/bin/bash

# Setup script for GitHub Actions CI/CD
# This script creates the service account and key needed for GitHub Actions

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-adveralabs-prod}"
SERVICE_ACCOUNT_NAME="github-actions-sa"
KEY_FILE="github-actions-key.json"

echo -e "${GREEN}Setting up GitHub Actions for Google Cloud deployment...${NC}"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed.${NC}"
    exit 1
fi

# Set the project
gcloud config set project ${PROJECT_ID}

# Create service account
echo -e "${YELLOW}Creating service account...${NC}"
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} \
    --display-name="GitHub Actions Service Account" \
    --description="Service account for GitHub Actions CI/CD" \
    --project=${PROJECT_ID} 2>/dev/null || \
    echo -e "${YELLOW}Service account may already exist${NC}"

# Grant necessary permissions
echo -e "${YELLOW}Granting permissions...${NC}"

echo "  - Cloud Run Admin"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/run.admin" \
    --condition=None 2>/dev/null || true

echo "  - Artifact Registry Writer"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.writer" \
    --condition=None 2>/dev/null || true

echo "  - Cloud SQL Client"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/cloudsql.client" \
    --condition=None 2>/dev/null || true

echo "  - Service Account User"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser" \
    --condition=None 2>/dev/null || true

echo "  - Secret Manager Secret Accessor"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor" \
    --condition=None 2>/dev/null || true

# Create and download key
echo -e "${YELLOW}Creating service account key...${NC}"
gcloud iam service-accounts keys create ${KEY_FILE} \
    --iam-account=${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
    --project=${PROJECT_ID}

echo ""
echo -e "${GREEN}✓ Setup complete!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo ""
echo "1. Add the following secrets to your GitHub repository:"
echo "   - Go to: https://github.com/pmaxit/adveralabs/settings/secrets/actions"
echo ""
echo "2. Add secret: GCP_PROJECT_ID"
echo "   Value: ${PROJECT_ID}"
echo ""
echo "3. Add secret: GCP_SA_KEY"
echo "   Value: (Copy the entire contents of ${KEY_FILE})"
echo ""
echo "   To view the key:"
echo "   cat ${KEY_FILE}"
echo ""
echo -e "${RED}⚠️  IMPORTANT: Keep ${KEY_FILE} secure and never commit it to git!${NC}"
echo ""
echo "4. After adding secrets, push to main branch to trigger deployment:"
echo "   git push origin main"
echo ""
echo -e "${GREEN}The workflow will automatically deploy on every push to main!${NC}"


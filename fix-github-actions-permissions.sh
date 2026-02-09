#!/bin/bash

# Fix GitHub Actions Service Account Permissions
# This script adds the missing Cloud SQL Viewer permission

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-adveralabs-prod}"
SERVICE_ACCOUNT_NAME="github-actions-sa"

echo -e "${GREEN}Fixing GitHub Actions service account permissions...${NC}"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed.${NC}"
    exit 1
fi

# Set the project
gcloud config set project ${PROJECT_ID}

# Grant Cloud SQL Viewer permission
echo -e "${YELLOW}Granting Cloud SQL Viewer permission...${NC}"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/cloudsql.viewer" \
    --condition=None

# Grant Artifact Registry permissions
echo -e "${YELLOW}Granting Artifact Registry permissions...${NC}"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.writer" \
    --condition=None

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.reader" \
    --condition=None

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/storage.admin" \
    --condition=None

# Grant Cloud Run permissions
echo -e "${YELLOW}Granting Cloud Run permissions...${NC}"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/run.admin" \
    --condition=None

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/run.developer" \
    --condition=None

# Grant Cloud SQL Client permission (for connecting to database)
echo -e "${YELLOW}Granting Cloud SQL Client permission...${NC}"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/cloudsql.client" \
    --condition=None

# Grant Service Account User permission (for using service accounts)
echo -e "${YELLOW}Granting Service Account User permission...${NC}"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser" \
    --condition=None

echo ""
echo -e "${GREEN}✓ All permissions granted!${NC}"
echo ""
echo "The GitHub Actions service account can now:"
echo "  - View Cloud SQL instances"
echo "  - Get connection names"
echo "  - Push/pull Docker images to Artifact Registry"
echo "  - Deploy to Cloud Run services"
echo "  - Create and execute Cloud Run Jobs (for migrations)"
echo ""
echo "You can now retry the GitHub Actions workflow."


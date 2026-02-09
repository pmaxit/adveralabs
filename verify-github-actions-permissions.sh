#!/bin/bash

# Verify GitHub Actions Service Account Permissions
# This script checks if all required permissions are granted

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-adveralabs-prod}"
SERVICE_ACCOUNT_NAME="github-actions-sa"
SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo -e "${GREEN}Verifying GitHub Actions service account permissions...${NC}"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed.${NC}"
    exit 1
fi

# Set the project
gcloud config set project ${PROJECT_ID}

# Required roles
REQUIRED_ROLES=(
    "roles/run.admin"
    "roles/run.developer"
    "roles/artifactregistry.writer"
    "roles/artifactregistry.reader"
    "roles/cloudsql.client"
    "roles/cloudsql.viewer"
    "roles/iam.serviceAccountUser"
    "roles/secretmanager.secretAccessor"
    "roles/storage.admin"
)

echo -e "${YELLOW}Checking permissions for: ${SERVICE_ACCOUNT_EMAIL}${NC}"
echo ""

# Get current IAM policy
CURRENT_ROLES=$(gcloud projects get-iam-policy ${PROJECT_ID} \
    --flatten="bindings[].members" \
    --filter="bindings.members:serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --format="value(bindings.role)" 2>/dev/null || echo "")

# Check each required role
MISSING_ROLES=()
for ROLE in "${REQUIRED_ROLES[@]}"; do
    if echo "$CURRENT_ROLES" | grep -q "^${ROLE}$"; then
        echo -e "${GREEN}✓${NC} ${ROLE}"
    else
        echo -e "${RED}✗${NC} ${ROLE} (MISSING)"
        MISSING_ROLES+=("${ROLE}")
    fi
done

echo ""

if [ ${#MISSING_ROLES[@]} -eq 0 ]; then
    echo -e "${GREEN}✓ All required permissions are granted!${NC}"
    exit 0
else
    echo -e "${RED}✗ Missing ${#MISSING_ROLES[@]} permission(s)${NC}"
    echo ""
    echo -e "${YELLOW}To fix, run:${NC}"
    echo "./fix-github-actions-permissions.sh"
    echo ""
    echo "Or manually grant each missing role:"
    for ROLE in "${MISSING_ROLES[@]}"; do
        echo "  gcloud projects add-iam-policy-binding ${PROJECT_ID} \\"
        echo "    --member=\"serviceAccount:${SERVICE_ACCOUNT_EMAIL}\" \\"
        echo "    --role=\"${ROLE}\""
    done
    exit 1
fi


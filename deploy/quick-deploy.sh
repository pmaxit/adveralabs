#!/bin/bash

# Quick Deploy Script - Runs all deployment steps in sequence
# Usage: ./deploy/quick-deploy.sh

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Advera Labs Quick Deploy ===${NC}"
echo ""

# Check if project ID is set
if [ -z "$GCP_PROJECT_ID" ]; then
    echo -e "${YELLOW}GCP_PROJECT_ID not set. Please set it:${NC}"
    echo "export GCP_PROJECT_ID='your-project-id'"
    exit 1
fi

# Step 1: Initial Setup
echo -e "${GREEN}Step 1: Running initial GCP setup...${NC}"
./deploy/gcp-setup.sh

echo ""
echo -e "${GREEN}Step 2: Building and deploying to Cloud Run...${NC}"
./deploy/build-and-deploy.sh

echo ""
echo -e "${GREEN}Step 3: Running database migrations...${NC}"
./deploy/run-migrations.sh

echo ""
echo -e "${GREEN}Step 4: Creating superuser...${NC}"
./deploy/create-superuser.sh

echo ""
echo -e "${GREEN}=== Deployment Complete! ===${NC}"
echo ""
echo "Your website is now live on Google Cloud Run!"
echo "Get the URL with:"
echo "gcloud run services describe adveralabs-web --region us-central1 --format='value(status.url)'"


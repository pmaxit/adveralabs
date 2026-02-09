#!/bin/bash

# Verification Script - Checks if deployment is successful
# Usage: ./deploy/verify-deployment.sh

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-adveralabs-prod}"
REGION="${GCP_REGION:-us-central1}"
SERVICE_NAME="adveralabs-web"
DB_INSTANCE_NAME="adveralabs-mysql"
APP_NAME="adveralabs"

echo -e "${GREEN}=== Verifying Advera Labs Deployment ===${NC}"
echo ""

# Set project
gcloud config set project ${PROJECT_ID} > /dev/null 2>&1

# Check Cloud Run service
echo -e "${YELLOW}Checking Cloud Run service...${NC}"
if gcloud run services describe ${SERVICE_NAME} --region ${REGION} > /dev/null 2>&1; then
    SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format="value(status.url)")
    echo -e "${GREEN}✓ Cloud Run service is running${NC}"
    echo "  URL: ${SERVICE_URL}"
    
    # Check if service is accessible
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" ${SERVICE_URL} || echo "000")
    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "301" ] || [ "$HTTP_CODE" = "302" ]; then
        echo -e "${GREEN}✓ Service is accessible (HTTP ${HTTP_CODE})${NC}"
    else
        echo -e "${RED}✗ Service returned HTTP ${HTTP_CODE}${NC}"
    fi
else
    echo -e "${RED}✗ Cloud Run service not found${NC}"
fi

echo ""

# Check Cloud SQL instance
echo -e "${YELLOW}Checking Cloud SQL instance...${NC}"
if gcloud sql instances describe ${DB_INSTANCE_NAME} > /dev/null 2>&1; then
    DB_STATUS=$(gcloud sql instances describe ${DB_INSTANCE_NAME} --format="value(state)")
    echo -e "${GREEN}✓ Cloud SQL instance exists (Status: ${DB_STATUS})${NC}"
    
    if [ "$DB_STATUS" = "RUNNABLE" ]; then
        echo -e "${GREEN}✓ Database is running${NC}"
    else
        echo -e "${YELLOW}⚠ Database status: ${DB_STATUS}${NC}"
    fi
else
    echo -e "${RED}✗ Cloud SQL instance not found${NC}"
fi

echo ""

# Check Artifact Registry
echo -e "${YELLOW}Checking Artifact Registry...${NC}"
if gcloud artifacts repositories describe ${APP_NAME}-repo --location=${REGION} > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Artifact Registry repository exists${NC}"
else
    echo -e "${RED}✗ Artifact Registry repository not found${NC}"
fi

echo ""

# Check service account
echo -e "${YELLOW}Checking service account...${NC}"
SERVICE_ACCOUNT="${APP_NAME}-sa@${PROJECT_ID}.iam.gserviceaccount.com"
if gcloud iam service-accounts describe ${SERVICE_ACCOUNT} > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Service account exists${NC}"
else
    echo -e "${RED}✗ Service account not found${NC}"
fi

echo ""

# Check secrets
echo -e "${YELLOW}Checking secrets...${NC}"
if gcloud secrets describe db-password > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Database password secret exists${NC}"
else
    echo -e "${RED}✗ Database password secret not found${NC}"
fi

echo ""
echo -e "${GREEN}=== Verification Complete ===${NC}"
echo ""
echo "To view logs:"
echo "  gcloud run services logs read ${SERVICE_NAME} --region ${REGION} --limit 50"


#!/bin/bash

# Build and Deploy Script for Advera Labs
# This script builds the Docker image and deploys it to Cloud Run

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration variables
PROJECT_ID="${GCP_PROJECT_ID:-adveralabs-prod}"
REGION="${GCP_REGION:-us-central1}"
APP_NAME="adveralabs"
REPOSITORY="${APP_NAME}-repo"
IMAGE_NAME="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${APP_NAME}"
SERVICE_NAME="${APP_NAME}-web"
SERVICE_ACCOUNT_NAME="${APP_NAME}-sa"
DB_INSTANCE_NAME="${APP_NAME}-mysql"

echo -e "${GREEN}Building and deploying Advera Labs to Cloud Run...${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed.${NC}"
    exit 1
fi

# Set the project
gcloud config set project ${PROJECT_ID}

# Get Cloud SQL connection name
CONNECTION_NAME=$(gcloud sql instances describe ${DB_INSTANCE_NAME} --format="value(connectionName)")

# Build Docker image
echo -e "${YELLOW}Building Docker image...${NC}"
docker build -t ${IMAGE_NAME}:latest .

# Push image to Artifact Registry
echo -e "${YELLOW}Pushing image to Artifact Registry...${NC}"
docker push ${IMAGE_NAME}:latest

# Deploy to Cloud Run
echo -e "${YELLOW}Deploying to Cloud Run...${NC}"
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME}:latest \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --service-account ${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
    --add-cloudsql-instances ${CONNECTION_NAME} \
    --set-env-vars="DJANGO_SETTINGS_MODULE=adveralabs.settings,USE_CLOUD_SQL=True" \
    --set-secrets="DB_PASSWORD=db-password:latest" \
    --memory 512Mi \
    --cpu 1 \
    --timeout 300 \
    --max-instances 10 \
    --min-instances 0 \
    --port 8080

# Get service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format="value(status.url)")

echo -e "${GREEN}Deployment completed!${NC}"
echo -e "${GREEN}Service URL: ${SERVICE_URL}${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Run database migrations: ./deploy/run-migrations.sh"
echo "2. Create superuser: ./deploy/create-superuser.sh"
echo "3. Visit your site at: ${SERVICE_URL}"


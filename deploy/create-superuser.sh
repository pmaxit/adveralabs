#!/bin/bash

# Create Django Superuser
# This script creates a superuser using Cloud Run Jobs

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-adveralabs-prod}"
REGION="${GCP_REGION:-us-central1}"
APP_NAME="adveralabs"
REPOSITORY="${APP_NAME}-repo"
IMAGE_NAME="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${APP_NAME}"
JOB_NAME="${APP_NAME}-createsuperuser"
SERVICE_ACCOUNT_NAME="${APP_NAME}-sa"
DB_INSTANCE_NAME="${APP_NAME}-mysql"

echo -e "${GREEN}Creating Django superuser...${NC}"

# Set the project
gcloud config set project ${PROJECT_ID}

# Get Cloud SQL connection name
CONNECTION_NAME=$(gcloud sql instances describe ${DB_INSTANCE_NAME} --format="value(connectionName)")

# Prompt for superuser details
read -p "Enter superuser email: " SUPERUSER_EMAIL
read -sp "Enter superuser password: " SUPERUSER_PASSWORD
echo ""

# Create Cloud Run Job for creating superuser
echo -e "${YELLOW}Creating Cloud Run Job...${NC}"
gcloud run jobs create ${JOB_NAME} \
    --image ${IMAGE_NAME}:latest \
    --region ${REGION} \
    --service-account ${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
    --set-cloudsql-instances ${CONNECTION_NAME} \
    --set-env-vars="DJANGO_SETTINGS_MODULE=adveralabs.settings,USE_CLOUD_SQL=True,DJANGO_SUPERUSER_EMAIL=${SUPERUSER_EMAIL},DJANGO_SUPERUSER_PASSWORD=${SUPERUSER_PASSWORD}" \
    --set-secrets="DB_PASSWORD=db-password:latest" \
    --memory 512Mi \
    --cpu 1 \
    --task-timeout 300 \
    --command python \
    --args manage.py,createsuperuser,--noinput,--email,${SUPERUSER_EMAIL} \
    --max-retries 1 || \
    (echo -e "${YELLOW}Job may already exist, updating...${NC}" && \
    gcloud run jobs update ${JOB_NAME} \
        --image ${IMAGE_NAME}:latest \
        --region ${REGION} \
        --set-cloudsql-instances ${CONNECTION_NAME} \
        --update-env-vars="DJANGO_SETTINGS_MODULE=adveralabs.settings,USE_CLOUD_SQL=True,DJANGO_SUPERUSER_EMAIL=${SUPERUSER_EMAIL},DJANGO_SUPERUSER_PASSWORD=${SUPERUSER_PASSWORD}" \
        --update-secrets="DB_PASSWORD=db-password:latest" \
        --task-timeout 300)

# Execute the job
echo -e "${YELLOW}Executing job...${NC}"
gcloud run jobs execute ${JOB_NAME} --region ${REGION} --wait

echo -e "${GREEN}Superuser created!${NC}"
echo -e "${GREEN}Email: ${SUPERUSER_EMAIL}${NC}"


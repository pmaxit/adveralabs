#!/bin/bash

# Fix Existing Cloud Run Jobs
# This script updates existing Cloud Run Jobs with correct syntax

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
PROJECT_ID="${GCP_PROJECT_ID:-adveralabs-prod}"
REGION="${GCP_REGION:-us-central1}"
APP_NAME="adveralabs"
REPOSITORY="${APP_NAME}-repo"
IMAGE_NAME="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${APP_NAME}"
SERVICE_ACCOUNT_NAME="${APP_NAME}-sa"
DB_INSTANCE_NAME="${APP_NAME}-mysql"

echo -e "${GREEN}Fixing existing Cloud Run Jobs...${NC}"

# Set the project
gcloud config set project ${PROJECT_ID}

# Get Cloud SQL connection name
CONNECTION_NAME=$(gcloud sql instances describe ${DB_INSTANCE_NAME} --format="value(connectionName)")

# Fix migrations job
MIGRATE_JOB="${APP_NAME}-migrate"
if gcloud run jobs describe ${MIGRATE_JOB} --region ${REGION} > /dev/null 2>&1; then
    echo -e "${YELLOW}Updating migrations job...${NC}"
    gcloud run jobs update ${MIGRATE_JOB} \
        --image ${IMAGE_NAME}:latest \
        --region ${REGION} \
        --set-cloudsql-instances ${CONNECTION_NAME} \
        --update-env-vars="DJANGO_SETTINGS_MODULE=adveralabs.settings,USE_CLOUD_SQL=True" \
        --update-secrets="DB_PASSWORD=db-password:latest" \
        --task-timeout 600 \
        --memory 512Mi \
        --cpu 1
    echo -e "${GREEN}✓ Migrations job updated${NC}"
else
    echo -e "${YELLOW}Migrations job not found, creating...${NC}"
    gcloud run jobs create ${MIGRATE_JOB} \
        --image ${IMAGE_NAME}:latest \
        --region ${REGION} \
        --service-account ${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com \
        --set-cloudsql-instances ${CONNECTION_NAME} \
        --set-env-vars="DJANGO_SETTINGS_MODULE=adveralabs.settings,USE_CLOUD_SQL=True" \
        --set-secrets="DB_PASSWORD=db-password:latest" \
        --memory 512Mi \
        --cpu 1 \
        --task-timeout 600 \
        --command python \
        --args manage.py,migrate \
        --max-retries 1
    echo -e "${GREEN}✓ Migrations job created${NC}"
fi

# Fix superuser job
SUPERUSER_JOB="${APP_NAME}-createsuperuser"
if gcloud run jobs describe ${SUPERUSER_JOB} --region ${REGION} > /dev/null 2>&1; then
    echo -e "${YELLOW}Updating superuser job...${NC}"
    gcloud run jobs update ${SUPERUSER_JOB} \
        --image ${IMAGE_NAME}:latest \
        --region ${REGION} \
        --set-cloudsql-instances ${CONNECTION_NAME} \
        --update-env-vars="DJANGO_SETTINGS_MODULE=adveralabs.settings,USE_CLOUD_SQL=True" \
        --update-secrets="DB_PASSWORD=db-password:latest" \
        --task-timeout 300 \
        --memory 512Mi \
        --cpu 1
    echo -e "${GREEN}✓ Superuser job updated${NC}"
else
    echo -e "${YELLOW}Superuser job not found${NC}"
fi

echo -e "${GREEN}All jobs fixed!${NC}"


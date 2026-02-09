#!/bin/bash

# GCP Deployment Setup Script for Advera Labs
# This script sets up all necessary GCP resources for deploying the Django website

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration variables (modify these)
PROJECT_ID="${GCP_PROJECT_ID:-adveralabs-prod}"
REGION="${GCP_REGION:-us-central1}"
ZONE="${GCP_ZONE:-us-central1-a}"
APP_NAME="adveralabs"
DB_INSTANCE_NAME="${APP_NAME}-mysql"
DB_NAME="adveralabs_db"
DB_USER="adveralabs_user"
DB_PASSWORD="${DB_PASSWORD:-$(openssl rand -base64 32)}"
SERVICE_ACCOUNT_NAME="${APP_NAME}-sa"
CLOUD_RUN_SERVICE="${APP_NAME}-web"

echo -e "${GREEN}Starting GCP setup for Advera Labs...${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed. Please install it from https://cloud.google.com/sdk/docs/install${NC}"
    exit 1
fi

# Set the project
echo -e "${YELLOW}Setting GCP project to ${PROJECT_ID}...${NC}"
gcloud config set project ${PROJECT_ID}

# Enable required APIs
echo -e "${YELLOW}Enabling required GCP APIs...${NC}"
gcloud services enable \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    sqladmin.googleapis.com \
    servicenetworking.googleapis.com \
    vpcaccess.googleapis.com \
    secretmanager.googleapis.com \
    artifactregistry.googleapis.com

# Create Cloud SQL MySQL instance
echo -e "${YELLOW}Creating Cloud SQL MySQL instance...${NC}"
gcloud sql instances create ${DB_INSTANCE_NAME} \
    --database-version=MYSQL_8_0 \
    --tier=db-f1-micro \
    --region=${REGION} \
    --root-password=${DB_PASSWORD} \
    --storage-type=SSD \
    --storage-size=20GB \
    --storage-auto-increase \
    --backup-start-time=03:00 \
    --enable-bin-log \
    --maintenance-window-day=SUN \
    --maintenance-window-hour=4 \
    --deletion-protection || echo -e "${YELLOW}Instance may already exist${NC}"

# Create database
echo -e "${YELLOW}Creating database ${DB_NAME}...${NC}"
gcloud sql databases create ${DB_NAME} \
    --instance=${DB_INSTANCE_NAME} || echo -e "${YELLOW}Database may already exist${NC}"

# Create database user
echo -e "${YELLOW}Creating database user...${NC}"
gcloud sql users create ${DB_USER} \
    --instance=${DB_INSTANCE_NAME} \
    --password=${DB_PASSWORD} || echo -e "${YELLOW}User may already exist${NC}"

# Get Cloud SQL connection name
CONNECTION_NAME=$(gcloud sql instances describe ${DB_INSTANCE_NAME} --format="value(connectionName)")

# Store secrets in Secret Manager
echo -e "${YELLOW}Storing secrets in Secret Manager...${NC}"
echo -n ${DB_PASSWORD} | gcloud secrets create db-password --data-file=- --replication-policy="automatic" 2>/dev/null || \
    echo -n ${DB_PASSWORD} | gcloud secrets versions add db-password --data-file=-

# Create service account for Cloud Run
echo -e "${YELLOW}Creating service account...${NC}"
gcloud iam service-accounts create ${SERVICE_ACCOUNT_NAME} \
    --display-name="Advera Labs Service Account" \
    --description="Service account for Advera Labs Cloud Run service" || \
    echo -e "${YELLOW}Service account may already exist${NC}"

# Grant necessary permissions
echo -e "${YELLOW}Granting permissions to service account...${NC}"
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT_NAME}@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/cloudsql.client"

# Create Artifact Registry repository
echo -e "${YELLOW}Creating Artifact Registry repository...${NC}"
gcloud artifacts repositories create ${APP_NAME}-repo \
    --repository-format=docker \
    --location=${REGION} \
    --description="Docker repository for Advera Labs" || \
    echo -e "${YELLOW}Repository may already exist${NC}"

# Configure Docker to use gcloud as credential helper
echo -e "${YELLOW}Configuring Docker authentication...${NC}"
gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet

# Create VPC connector for Cloud SQL access (if needed)
echo -e "${YELLOW}Creating VPC connector...${NC}"
gcloud compute networks vpc-access connectors create ${APP_NAME}-connector \
    --region=${REGION} \
    --subnet-project=${PROJECT_ID} \
    --subnet=default \
    --min-instances=2 \
    --max-instances=3 \
    --machine-type=e2-micro || \
    echo -e "${YELLOW}VPC connector may already exist${NC}"

echo -e "${GREEN}GCP setup completed!${NC}"
echo -e "${GREEN}Database connection name: ${CONNECTION_NAME}${NC}"
echo -e "${GREEN}Database password saved to Secret Manager${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Update your Django settings with the database connection details"
echo "2. Run: ./deploy/build-and-deploy.sh"
echo ""
echo -e "${YELLOW}Connection details:${NC}"
echo "DB_HOST: /cloudsql/${CONNECTION_NAME}"
echo "DB_NAME: ${DB_NAME}"
echo "DB_USER: ${DB_USER}"
echo "DB_PASSWORD: Check Secret Manager (secret: db-password)"


# Google Cloud Platform Deployment Guide

This directory contains scripts and configuration files for deploying the Advera Labs Django website to Google Cloud Platform.

## Prerequisites

1. **Google Cloud SDK (gcloud CLI)**
   ```bash
   # Install gcloud CLI
   # https://cloud.google.com/sdk/docs/install
   ```

2. **Docker**
   ```bash
   # Install Docker
   # https://docs.docker.com/get-docker/
   ```

3. **Google Cloud Project**
   - Create a new GCP project or use an existing one
   - Enable billing (required for Cloud SQL and Cloud Run)

4. **Authentication**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

## Quick Start

### 1. Set Environment Variables

```bash
export GCP_PROJECT_ID="your-project-id"
export GCP_REGION="us-central1"
export GCP_ZONE="us-central1-a"
export DB_PASSWORD="your-secure-password"  # Optional, will be auto-generated if not set
```

### 2. Run Initial Setup

This script creates all necessary GCP resources:
- Cloud SQL MySQL instance
- Database and user
- Service account
- Artifact Registry repository
- VPC connector
- Secret Manager secrets

```bash
chmod +x deploy/gcp-setup.sh
./deploy/gcp-setup.sh
```

### 3. Build and Deploy

This script builds the Docker image and deploys it to Cloud Run:

```bash
chmod +x deploy/build-and-deploy.sh
./deploy/build-and-deploy.sh
```

### 4. Run Database Migrations

```bash
chmod +x deploy/run-migrations.sh
./deploy/run-migrations.sh
```

### 5. Create Superuser

```bash
chmod +x deploy/create-superuser.sh
./deploy/create-superuser.sh
```

## Manual Steps

### Update Django Settings

The Django settings are already configured to use Cloud SQL when `USE_CLOUD_SQL=True` is set. The deployment scripts handle this automatically.

### Get Service URL

After deployment, get your service URL:

```bash
gcloud run services describe adveralabs-web \
    --region us-central1 \
    --format="value(status.url)"
```

## Scripts Overview

### `gcp-setup.sh`
Initial setup script that creates all GCP resources:
- Enables required APIs
- Creates Cloud SQL MySQL instance
- Creates database and user
- Sets up service account with permissions
- Creates Artifact Registry repository
- Stores secrets in Secret Manager

### `build-and-deploy.sh`
Builds Docker image and deploys to Cloud Run:
- Builds Docker image
- Pushes to Artifact Registry
- Deploys to Cloud Run with proper configuration

### `run-migrations.sh`
Runs Django migrations using Cloud Run Jobs:
- Creates a Cloud Run Job
- Executes `python manage.py migrate`

### `create-superuser.sh`
Creates Django superuser using Cloud Run Jobs:
- Prompts for email and password
- Creates superuser via Cloud Run Job

## Configuration

### Environment Variables

You can customize the deployment by setting these environment variables:

- `GCP_PROJECT_ID`: Your GCP project ID (default: `adveralabs-prod`)
- `GCP_REGION`: GCP region (default: `us-central1`)
- `GCP_ZONE`: GCP zone (default: `us-central1-a`)
- `DB_PASSWORD`: Database password (auto-generated if not set)

### Cloud SQL Configuration

The setup script creates:
- **Instance**: `adveralabs-mysql`
- **Database**: `adveralabs_db`
- **User**: `adveralabs_user`
- **Tier**: `db-f1-micro` (can be upgraded)
- **Storage**: 20GB SSD with auto-increase

### Cloud Run Configuration

- **Memory**: 512Mi
- **CPU**: 1
- **Timeout**: 300 seconds
- **Max Instances**: 10
- **Min Instances**: 0 (scales to zero)

## CI/CD with Cloud Build

You can set up automated deployments using Cloud Build:

```bash
# Create a trigger
gcloud builds triggers create github \
    --name="adveralabs-deploy" \
    --repo-name="your-repo" \
    --repo-owner="your-username" \
    --branch-pattern="^main$" \
    --build-config="deploy/cloudbuild.yaml"
```

## Troubleshooting

### Database Connection Issues

If you encounter database connection errors:

1. Check Cloud SQL instance is running:
   ```bash
   gcloud sql instances describe adveralabs-mysql
   ```

2. Verify connection name:
   ```bash
   gcloud sql instances describe adveralabs-mysql --format="value(connectionName)"
   ```

3. Check service account permissions:
   ```bash
   gcloud projects get-iam-policy your-project-id \
       --flatten="bindings[].members" \
       --filter="bindings.members:serviceAccount:adveralabs-sa@*"
   ```

### Build Failures

1. Check Docker is running:
   ```bash
   docker ps
   ```

2. Verify Artifact Registry access:
   ```bash
   gcloud auth configure-docker us-central1-docker.pkg.dev
   ```

3. Check build logs:
   ```bash
   gcloud builds list --limit=5
   ```

### Deployment Issues

1. Check Cloud Run service logs:
   ```bash
   gcloud run services logs read adveralabs-web --region us-central1
   ```

2. Verify environment variables:
   ```bash
   gcloud run services describe adveralabs-web --region us-central1
   ```

## Cost Estimation

Approximate monthly costs (varies by usage):

- **Cloud SQL (db-f1-micro)**: ~$7-10/month
- **Cloud Run**: Pay per request (~$0.40 per million requests)
- **Artifact Registry**: ~$0.10 per GB stored
- **VPC Connector**: ~$10/month

Total: ~$20-30/month for low traffic

## Security Best Practices

1. **Secrets Management**: Database passwords are stored in Secret Manager
2. **Service Account**: Uses least-privilege IAM roles
3. **HTTPS**: Cloud Run automatically provides HTTPS
4. **Database**: Cloud SQL uses encrypted connections
5. **Environment Variables**: Sensitive data in Secret Manager, not env vars

## Scaling

To scale up:

1. **Cloud SQL**: Upgrade instance tier
   ```bash
   gcloud sql instances patch adveralabs-mysql --tier=db-n1-standard-1
   ```

2. **Cloud Run**: Increase memory/CPU
   ```bash
   gcloud run services update adveralabs-web \
       --region us-central1 \
       --memory 1Gi \
       --cpu 2
   ```

## Monitoring

Set up monitoring:

```bash
# Enable Cloud Monitoring
gcloud services enable monitoring.googleapis.com

# View logs
gcloud run services logs read adveralabs-web --region us-central1 --limit 50
```

## Cleanup

To remove all resources:

```bash
# Delete Cloud Run service
gcloud run services delete adveralabs-web --region us-central1

# Delete Cloud SQL instance (WARNING: This deletes all data)
gcloud sql instances delete adveralabs-mysql

# Delete Artifact Registry repository
gcloud artifacts repositories delete adveralabs-repo --location us-central1

# Delete service account
gcloud iam service-accounts delete adveralabs-sa@your-project-id.iam.gserviceaccount.com
```

## Support

For issues or questions:
1. Check Cloud Run logs
2. Review GCP documentation
3. Check Django application logs in Cloud Run


# Google Cloud Platform Deployment

Complete deployment setup for Advera Labs Django website to Google Cloud Platform using Cloud Run and Cloud SQL MySQL.

## 🚀 Quick Start

```bash
# 1. Set your GCP project ID
export GCP_PROJECT_ID="your-project-id"

# 2. Run quick deploy (does everything)
./deploy/quick-deploy.sh
```

## 📋 Prerequisites

1. **Google Cloud SDK (gcloud)**
   ```bash
   # Install from: https://cloud.google.com/sdk/docs/install
   gcloud --version
   ```

2. **Docker**
   ```bash
   # Install from: https://docs.docker.com/get-docker/
   docker --version
   ```

3. **Authentication**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

## 📁 Files Created

### Deployment Scripts
- `deploy/gcp-setup.sh` - Initial GCP resource setup
- `deploy/build-and-deploy.sh` - Build and deploy to Cloud Run
- `deploy/run-migrations.sh` - Run Django migrations
- `deploy/create-superuser.sh` - Create Django admin user
- `deploy/quick-deploy.sh` - All-in-one deployment script

### Configuration Files
- `Dockerfile` - Docker image configuration
- `.dockerignore` - Files to exclude from Docker build
- `.gcloudignore` - Files to exclude from GCP uploads
- `deploy/cloudbuild.yaml` - Cloud Build CI/CD configuration

### Updated Files
- `adveralabs/settings.py` - Added Cloud SQL MySQL support
- `requirements.txt` - Added gunicorn, mysqlclient, PyMySQL

## 🏗️ Architecture

```
┌─────────────────┐
│   Cloud Run     │  ← Django Application (Container)
│   (Web Server)  │
└────────┬────────┘
         │
         │ Cloud SQL Proxy
         │
┌────────▼────────┐
│   Cloud SQL     │  ← MySQL Database
│   (MySQL 8.0)  │
└─────────────────┘
```

## 📝 Step-by-Step Deployment

### Step 1: Initial Setup

Creates all GCP resources:
- Cloud SQL MySQL instance
- Database and user
- Service account with permissions
- Artifact Registry repository
- VPC connector
- Secret Manager secrets

```bash
./deploy/gcp-setup.sh
```

### Step 2: Build and Deploy

Builds Docker image and deploys to Cloud Run:

```bash
./deploy/build-and-deploy.sh
```

### Step 3: Run Migrations

Runs Django database migrations:

```bash
./deploy/run-migrations.sh
```

### Step 4: Create Superuser

Creates Django admin superuser:

```bash
./deploy/create-superuser.sh
```

## 🔧 Configuration

### Environment Variables

Set these before running scripts:

```bash
export GCP_PROJECT_ID="your-project-id"      # Required
export GCP_REGION="us-central1"              # Optional (default: us-central1)
export GCP_ZONE="us-central1-a"             # Optional (default: us-central1-a)
export DB_PASSWORD="secure-password"        # Optional (auto-generated if not set)
```

### Cloud SQL Configuration

- **Instance Name**: `adveralabs-mysql`
- **Database**: `adveralabs_db`
- **User**: `adveralabs_user`
- **Tier**: `db-f1-micro` (can be upgraded)
- **Storage**: 20GB SSD with auto-increase
- **Backup**: Daily at 3:00 AM UTC

### Cloud Run Configuration

- **Service Name**: `adveralabs-web`
- **Memory**: 512Mi
- **CPU**: 1
- **Timeout**: 300 seconds
- **Max Instances**: 10
- **Min Instances**: 0 (scales to zero)
- **Port**: 8080

## 🔐 Security

- **Secrets**: Database password stored in Secret Manager
- **Service Account**: Least-privilege IAM roles
- **HTTPS**: Automatically provided by Cloud Run
- **Database**: Encrypted connections via Cloud SQL Proxy

## 💰 Cost Estimation

Approximate monthly costs (low traffic):

- **Cloud SQL (db-f1-micro)**: ~$7-10/month
- **Cloud Run**: ~$0.40 per million requests
- **Artifact Registry**: ~$0.10 per GB stored
- **VPC Connector**: ~$10/month

**Total**: ~$20-30/month for low traffic

## 🔍 Monitoring

### View Logs

```bash
# Cloud Run service logs
gcloud run services logs read adveralabs-web --region us-central1 --limit 50

# Cloud SQL logs
gcloud sql operations list --instance=adveralabs-mysql
```

### Get Service URL

```bash
gcloud run services describe adveralabs-web \
    --region us-central1 \
    --format="value(status.url)"
```

## 🚨 Troubleshooting

### Database Connection Issues

1. Check Cloud SQL instance status:
   ```bash
   gcloud sql instances describe adveralabs-mysql
   ```

2. Verify connection name:
   ```bash
   gcloud sql instances describe adveralabs-mysql --format="value(connectionName)"
   ```

3. Check service account permissions:
   ```bash
   gcloud projects get-iam-policy $GCP_PROJECT_ID \
       --flatten="bindings[].members" \
       --filter="bindings.members:serviceAccount:adveralabs-sa@*"
   ```

### Build Failures

1. Verify Docker is running:
   ```bash
   docker ps
   ```

2. Check Artifact Registry access:
   ```bash
   gcloud auth configure-docker us-central1-docker.pkg.dev
   ```

### Deployment Issues

1. Check Cloud Run service status:
   ```bash
   gcloud run services describe adveralabs-web --region us-central1
   ```

2. View recent logs:
   ```bash
   gcloud run services logs read adveralabs-web --region us-central1 --limit 100
   ```

## 📈 Scaling

### Upgrade Cloud SQL

```bash
gcloud sql instances patch adveralabs-mysql --tier=db-n1-standard-1
```

### Scale Cloud Run

```bash
gcloud run services update adveralabs-web \
    --region us-central1 \
    --memory 1Gi \
    --cpu 2 \
    --max-instances 20
```

## 🧹 Cleanup

To remove all resources:

```bash
# Delete Cloud Run service
gcloud run services delete adveralabs-web --region us-central1

# Delete Cloud SQL instance (WARNING: Deletes all data)
gcloud sql instances delete adveralabs-mysql

# Delete Artifact Registry
gcloud artifacts repositories delete adveralabs-repo --location us-central1

# Delete service account
gcloud iam service-accounts delete adveralabs-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com
```

## 🔄 CI/CD with Cloud Build

Set up automated deployments:

```bash
# Create Cloud Build trigger
gcloud builds triggers create github \
    --name="adveralabs-deploy" \
    --repo-name="your-repo" \
    --repo-owner="your-username" \
    --branch-pattern="^main$" \
    --build-config="deploy/cloudbuild.yaml"
```

## 📚 Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud SQL Documentation](https://cloud.google.com/sql/docs)
- [Django on Cloud Run](https://cloud.google.com/python/django/run)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## ✅ Verification Checklist

After deployment, verify:

- [ ] Cloud Run service is running
- [ ] Database migrations completed
- [ ] Superuser created successfully
- [ ] Website is accessible via Cloud Run URL
- [ ] Static files are being served
- [ ] Database connection is working
- [ ] HTTPS is enabled
- [ ] Logs are accessible

## 🆘 Support

For issues:
1. Check Cloud Run logs
2. Review GCP documentation
3. Verify all environment variables are set correctly
4. Ensure billing is enabled on your GCP project


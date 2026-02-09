# GitHub Actions CI/CD Setup

This directory contains GitHub Actions workflows for automated deployment to Google Cloud Platform.

## Workflow: Deploy to Google Cloud Run

The `deploy.yml` workflow automatically:
1. Builds a Docker image when code is pushed to `main` branch
2. Pushes the image to Google Artifact Registry
3. Deploys to Cloud Run
4. Runs database migrations

## Setup Instructions

### 1. Create Service Account Key

First, create a service account key for GitHub Actions:

```bash
# Set your project ID
export GCP_PROJECT_ID="your-project-id"

# Create a service account for GitHub Actions
gcloud iam service-accounts create github-actions-sa \
    --display-name="GitHub Actions Service Account" \
    --project=$GCP_PROJECT_ID

# Grant necessary permissions
gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
    --member="serviceAccount:github-actions-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
    --member="serviceAccount:github-actions-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
    --member="serviceAccount:github-actions-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/cloudsql.client"

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
    --member="serviceAccount:github-actions-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"

# Create and download key
gcloud iam service-accounts keys create github-actions-key.json \
    --iam-account=github-actions-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com
```

### 2. Add GitHub Secrets

Go to your GitHub repository:
1. Navigate to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add the following secrets:

#### Required Secrets:

- **`GCP_PROJECT_ID`**: Your Google Cloud project ID
  - Example: `adveralabs-prod`

- **`GCP_SA_KEY`**: The service account key JSON content
  - Copy the entire contents of `github-actions-key.json` file
  - Paste it as the secret value

### 3. Verify Setup

After adding the secrets, the workflow will automatically run on:
- Every push to the `main` branch
- Manual trigger via GitHub Actions UI

### 4. Monitor Deployments

- View workflow runs: **Actions** tab in GitHub
- View Cloud Run logs: Google Cloud Console → Cloud Run
- Check deployment status: GitHub Actions workflow page

## Workflow Triggers

The workflow runs on:
- **Push to main**: Automatically deploys on every commit
- **Manual trigger**: Use "Run workflow" button in GitHub Actions

## Troubleshooting

### Authentication Issues

If you see authentication errors:
1. Verify `GCP_SA_KEY` secret is correctly set
2. Check service account has required permissions
3. Ensure project ID matches your GCP project

### Build Failures

If Docker build fails:
1. Check Dockerfile syntax
2. Verify all dependencies in requirements.txt
3. Review build logs in GitHub Actions

### Deployment Failures

If Cloud Run deployment fails:
1. Check Cloud SQL instance is running
2. Verify connection name is correct
3. Ensure secrets are accessible
4. Review Cloud Run logs

### Migration Failures

If migrations fail:
1. Check database connection
2. Verify DB_PASSWORD secret exists
3. Review migration job logs

## Security Best Practices

1. **Never commit secrets**: All sensitive data is in GitHub Secrets
2. **Rotate keys regularly**: Update service account keys periodically
3. **Least privilege**: Service account only has necessary permissions
4. **Monitor access**: Review service account usage regularly

## Manual Deployment

If you need to deploy manually without GitHub:

```bash
./deploy/quick-deploy.sh
```

## Customization

To customize the workflow:
1. Edit `.github/workflows/deploy.yml`
2. Adjust environment variables in the `env` section
3. Modify deployment steps as needed


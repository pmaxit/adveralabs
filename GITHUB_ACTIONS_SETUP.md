# GitHub Actions CI/CD Setup Guide

This guide will help you set up automatic deployment to Google Cloud Run whenever you push code to GitHub.

## Quick Setup

Run the setup script:

```bash
export GCP_PROJECT_ID="your-project-id"
./setup-github-actions.sh
```

This will:
1. Create a service account for GitHub Actions
2. Grant necessary permissions
3. Generate a service account key

## Manual Setup Steps

### Step 1: Create Service Account

```bash
export GCP_PROJECT_ID="your-project-id"

# Create service account
gcloud iam service-accounts create github-actions-sa \
    --display-name="GitHub Actions Service Account" \
    --project=$GCP_PROJECT_ID

# Grant permissions
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

gcloud projects add-iam-policy-binding $GCP_PROJECT_ID \
    --member="serviceAccount:github-actions-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"

# Create key
gcloud iam service-accounts keys create github-actions-key.json \
    --iam-account=github-actions-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com
```

### Step 2: Add GitHub Secrets

1. Go to your GitHub repository: https://github.com/pmaxit/adveralabs
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

#### Add `GCP_PROJECT_ID`:
- **Name**: `GCP_PROJECT_ID`
- **Value**: Your GCP project ID (e.g., `adveralabs-prod`)

#### Add `GCP_SA_KEY`:
- **Name**: `GCP_SA_KEY`
- **Value**: Copy the entire contents of `github-actions-key.json`:
  ```bash
  cat github-actions-key.json
  ```
  Paste the entire JSON content as the secret value.

### Step 3: Verify Setup

1. Check that the workflow file exists: `.github/workflows/deploy.yml`
2. Push a commit to trigger the workflow:
   ```bash
   git add .
   git commit -m "Add GitHub Actions workflow"
   git push origin main
   ```
3. Go to the **Actions** tab in GitHub to see the workflow run

## How It Works

### Workflow Triggers

The workflow automatically runs when:
- Code is pushed to the `main` branch
- You manually trigger it from the Actions tab

### What Happens

1. **Checkout**: GitHub Actions checks out your code
2. **Authenticate**: Uses the service account key to authenticate with GCP
3. **Build**: Builds Docker image from your Dockerfile
4. **Push**: Pushes image to Google Artifact Registry
5. **Deploy**: Deploys to Cloud Run with latest image
6. **Migrate**: Runs database migrations automatically
7. **Notify**: Shows deployment status in GitHub Actions

### Workflow File

The workflow is defined in `.github/workflows/deploy.yml`. It:
- Uses `google-github-actions/setup-gcloud` for authentication
- Builds and pushes Docker images
- Deploys to Cloud Run
- Runs migrations via Cloud Run Jobs

## Monitoring

### View Workflow Runs

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. Select a workflow run to see details

### View Deployment Logs

- **GitHub**: Actions tab → Select workflow run
- **Google Cloud**: Cloud Run → Select service → Logs tab

### Check Deployment Status

```bash
# Get service URL
gcloud run services describe adveralabs-web \
    --region us-central1 \
    --format="value(status.url)"
```

## Troubleshooting

### Workflow Fails to Start

- Check that secrets are set correctly
- Verify repository has Actions enabled
- Check workflow file syntax

### Authentication Errors

- Verify `GCP_SA_KEY` secret contains valid JSON
- Check service account has required permissions
- Ensure project ID matches

### Build Failures

- Check Dockerfile syntax
- Verify all dependencies in requirements.txt
- Review build logs in Actions tab

### Deployment Failures

- Verify Cloud SQL instance is running
- Check connection name is correct
- Review Cloud Run logs
- Ensure secrets are accessible

### Migration Failures

- Check database connection settings
- Verify DB_PASSWORD secret exists
- Review migration job logs

## Security

### Best Practices

1. **Never commit keys**: The `github-actions-key.json` file is in `.gitignore`
2. **Rotate keys**: Update service account keys periodically
3. **Least privilege**: Service account only has necessary permissions
4. **Monitor usage**: Review service account activity regularly

### Key Rotation

To rotate the service account key:

```bash
# Delete old key
gcloud iam service-accounts keys list \
    --iam-account=github-actions-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com

# Create new key
gcloud iam service-accounts keys create github-actions-key.json \
    --iam-account=github-actions-sa@$GCP_PROJECT_ID.iam.gserviceaccount.com

# Update GitHub secret GCP_SA_KEY with new key content
```

## Customization

### Change Deployment Branch

Edit `.github/workflows/deploy.yml`:

```yaml
on:
  push:
    branches:
      - main  # Change to your branch name
```

### Add Environment Variables

Add to the `env` section or use `--set-env-vars` in deployment step.

### Skip Migrations

Remove or comment out the "Run database migrations" step.

### Add Notifications

Add notification steps (Slack, email, etc.) after deployment.

## Manual Deployment

If you need to deploy without GitHub Actions:

```bash
./deploy/quick-deploy.sh
```

## Support

For issues:
1. Check GitHub Actions logs
2. Review Cloud Run logs
3. Verify secrets are set correctly
4. Check service account permissions


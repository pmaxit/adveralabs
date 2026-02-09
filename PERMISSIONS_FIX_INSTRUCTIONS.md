# Fix GitHub Actions Permissions - Manual Instructions

The automated script requires IAM admin permissions. If you don't have those, follow these manual steps or ask your GCP project admin to run the commands.

## Required Permissions

The GitHub Actions service account (`github-actions-sa@YOUR-PROJECT-ID.iam.gserviceaccount.com`) needs these roles:

1. **Cloud Run Admin** - Deploy and manage Cloud Run services
2. **Cloud Run Developer** - Create and execute Cloud Run Jobs (for migrations)
3. **Artifact Registry Writer** - Push Docker images
4. **Artifact Registry Reader** - Pull Docker images
5. **Cloud SQL Client** - Connect to Cloud SQL
6. **Cloud SQL Viewer** - View Cloud SQL instances
7. **Service Account User** - Use service accounts
8. **Secret Manager Secret Accessor** - Access secrets
9. **Storage Admin** - Access Artifact Registry storage

## Manual Fix Commands

Replace `YOUR-PROJECT-ID` with your actual GCP project ID:

```bash
export PROJECT_ID="YOUR-PROJECT-ID"
export SERVICE_ACCOUNT="github-actions-sa@${PROJECT_ID}.iam.gserviceaccount.com"

# Cloud Run permissions
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/run.developer"

# Artifact Registry permissions
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/artifactregistry.reader"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/storage.admin"

# Cloud SQL permissions
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/cloudsql.client"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/cloudsql.viewer"

# Other permissions
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/iam.serviceAccountUser"

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="roles/secretmanager.secretAccessor"
```

## Verify Permissions

After granting permissions, verify they're set correctly:

```bash
./verify-github-actions-permissions.sh
```

## Alternative: Use GCP Console

If you prefer using the web UI:

1. Go to: https://console.cloud.google.com/iam-admin/iam
2. Select your project
3. Find the service account: `github-actions-sa@YOUR-PROJECT-ID.iam.gserviceaccount.com`
4. Click the pencil icon to edit
5. Click "ADD ANOTHER ROLE"
6. Add each role listed above
7. Click "SAVE"

## Troubleshooting

### "Permission denied" error
- You need the `roles/resourcemanager.projectIamAdmin` role
- Or ask your GCP project admin to run the commands
- Or use the GCP Console if you have UI access

### Service account doesn't exist
- Run `./setup-github-actions.sh` first to create it
- Or create it manually in GCP Console

### Project not found
- Verify the project ID is correct: `gcloud projects list`
- Make sure you have access to the project
- Check billing is enabled


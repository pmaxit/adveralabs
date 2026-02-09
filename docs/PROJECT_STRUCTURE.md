# Advera Labs - Project Structure & Documentation

## Overview

Advera Labs is a cross-channel ad optimization platform that intelligently manages ad spend across Facebook and Google Ads. The project consists of:
- **Backend API**: FastAPI-based service with Pydantic AI agents for ad optimization
- **Frontend Website**: Django-based marketing website
- **Deployment**: Automated CI/CD pipeline to Google Cloud Platform

## Project Architecture

```
adveralabs/
├── backend/              # FastAPI backend with AI agents
├── website/              # Django marketing website
├── deploy/               # GCP deployment scripts
├── docs/                 # Documentation
├── examples/             # Example usage scripts
├── tests/                # Test suite
└── .github/              # GitHub Actions workflows
```

---

## Directory Structure

### `/backend/` - FastAPI Backend

**Purpose**: Core ad optimization engine with AI-powered agents

#### `/backend/agents/` - Pydantic AI Agents

| File | Purpose | Key Features |
|------|---------|--------------|
| `ad_optimization_agent.py` | Core budget allocation agent | Multi-armed bandit strategies, cross-channel optimization, profit/LTV-based allocation |
| `roi_audit_agent.py` | ROI health analysis | Detects tracking issues, misconfigurations, performance problems |
| `signal_generation_agent.py` | Conversion signal generation | Converts business events to high-quality ad platform signals |
| `analytics_agent.py` | Marketing analytics | Performance analysis, report generation |
| `campaign_agent.py` | Campaign management | Campaign creation, optimization, A/B testing |
| `content_agent.py` | Content generation | Content calendar, content creation |
| `seo_agent.py` | SEO optimization | Keyword research, SEO analysis |
| `social_media_agent.py` | Social media management | Posting, analytics, hashtag research |
| `client_communication_agent.py` | Client communication | Proposal generation, client updates |
| `base_agent.py` | Base agent class | Common functionality for all agents |

**Key Models**:
- `ArmState`: Represents a campaign/adset with metrics (spend, revenue, conversions, LTV, profit margin)
- `BudgetAllocationRequest/Response`: Budget allocation requests and results
- `CrossChannelOptimizationRequest/Response`: Cross-platform optimization

#### `/backend/services/` - Business Logic Services

| File | Purpose |
|------|---------|
| `optimization_service.py` | Orchestrates optimization loop (fetch → allocate → apply) |
| `optimization_strategies.py` | Multi-armed bandit algorithms (Epsilon-Greedy, UCB, Thompson Sampling, Adaptive) |
| `llm_service.py` | LLM service wrapper for AI operations |

#### `/backend/services/integrations/` - Platform Integrations

| File | Purpose | Key Methods |
|------|---------|-------------|
| `facebook_ads.py` | Facebook Ads API integration | `get_insights()`, `update_adset_budget()`, `send_conversion_event()` |
| `google_ads.py` | Google Ads API integration | `get_campaign_insights()`, `update_campaign_budget()`, `send_offline_conversion()` |
| `analytics.py` | Analytics platform integration | Data collection and analysis |

#### `/backend/api/` - FastAPI Application

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app initialization |
| `routes/agents.py` | API endpoints for all agents |
| `routes/tasks.py` | Task management endpoints |

**Key Endpoints**:
- `POST /api/v1/agents/ad-optimization/allocate-budget`: Allocate budget across campaigns
- `POST /api/v1/agents/ad-optimization/cross-channel`: Cross-channel optimization
- `POST /api/v1/agents/ad-optimization/run-optimization`: Full optimization cycle
- `POST /api/v1/agents/roi-audit/analyze`: ROI health analysis

#### `/backend/models/` - Data Models

| File | Purpose |
|------|---------|
| `schemas.py` | Pydantic models for API requests/responses |
| `database.py` | SQLAlchemy database models |

#### `/backend/config/` - Configuration

| File | Purpose |
|------|---------|
| `settings.py` | Application configuration and environment variables |

---

### `/website/` - Django Marketing Website

**Purpose**: Marketing website for Advera Labs

#### Structure

| Directory/File | Purpose |
|----------------|---------|
| `views.py` | Django view functions for all pages (home, blog, about, contact, etc.) |
| `urls.py` | URL routing for the website app |
| `apps.py` | Django app configuration |
| `templates/website/` | HTML templates (base.html, home.html, blog.html, etc.) |
| `static/website/` | Static files (CSS, JS, images) |

**Key Pages**:
- Home (`home.html`): Main landing page with features, pricing, ROI calculator
- Blog (`blog.html`, `blog_post.html`): Research articles on ad optimization
- About (`about.html`): Company information
- Contact (`contact.html`): Contact form
- Documentation (`documentation.html`): API documentation
- Careers (`careers.html`): Job listings
- Support (`support.html`): Support resources
- Privacy (`privacy.html`): Privacy policy

**Blog Articles**: 10 research articles covering:
- Multi-armed bandit algorithms
- Reinforcement learning in advertising
- Bayesian optimization
- Combinatorial bandits
- Cross-channel optimization

---

### `/deploy/` - Deployment Scripts

**Purpose**: Scripts for deploying to Google Cloud Platform

| Script | Purpose | Key Operations |
|--------|---------|----------------|
| `gcp-setup.sh` | Initial GCP resource setup | Creates Cloud SQL, service accounts, Artifact Registry, VPC connector, secrets |
| `build-and-deploy.sh` | Build and deploy to Cloud Run | Builds Docker image, pushes to Artifact Registry, deploys to Cloud Run |
| `run-migrations.sh` | Run database migrations | Executes Django migrations via Cloud Run Jobs |
| `create-superuser.sh` | Create Django admin user | Creates superuser via Cloud Run Jobs |
| `verify-deployment.sh` | Verify deployment | Checks service health and connectivity |
| `quick-deploy.sh` | All-in-one deployment | Runs setup, build, deploy, migrations in sequence |
| `fix-existing-jobs.sh` | Fix Cloud Run Jobs | Updates existing Cloud Run Jobs configuration |
| `cloudbuild.yaml` | Cloud Build CI/CD config | Automated build and deployment configuration |

**GCP Resources Created**:
- Cloud SQL MySQL instance (`adveralabs-mysql`)
- Cloud Run service (`adveralabs-web`)
- Artifact Registry repository (`adveralabs-repo`)
- Service account (`adveralabs-sa`)
- VPC Connector for database access
- Secret Manager for sensitive data

---

### `/docs/` - Documentation

| File | Purpose |
|------|---------|
| `startup-plan.md` | Original startup business plan and system design |
| `TASK_PLAN.md` | Implementation task breakdown |
| `IMPLEMENTATION_SUMMARY.md` | Summary of implemented features |
| `COMPETITOR_ANALYSIS.md` | Competitive analysis of similar platforms |
| `PROJECT_STRUCTURE.md` | This file - comprehensive project documentation |

---

### Root Level Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Docker image definition for Django app |
| `docker-compose.yml` | Local development Docker setup |
| `requirements.txt` | Python dependencies |
| `manage.py` | Django management script |
| `alembic.ini` | Database migration configuration |
| `pytest.ini` | Test configuration |
| `.gitignore` | Git ignore patterns |
| `.gcloudignore` | GCP deployment ignore patterns |

---

## Deployment Scripts (Root Level)

| Script | Purpose |
|--------|---------|
| `setup-github-actions.sh` | Creates GitHub Actions service account and grants permissions |
| `fix-github-actions-permissions.sh` | Fixes/updates GitHub Actions service account permissions |
| `verify-github-actions-permissions.sh` | Verifies all required permissions are granted |

---

## GitHub Actions Workflow

**File**: `.github/workflows/deploy.yml`

**Purpose**: Automated CI/CD pipeline that triggers on every push to `main` branch

**Workflow Steps**:
1. Checkout code
2. Authenticate to Google Cloud
3. Configure Docker for Artifact Registry
4. Get Cloud SQL connection name
5. Build Docker image
6. Push to Artifact Registry
7. Deploy to Cloud Run
8. Run database migrations (via Cloud Run Job)
9. Deployment summary

**Required Secrets**:
- `GCP_PROJECT_ID`: Google Cloud project ID
- `GCP_SA_KEY`: Service account JSON key for authentication

**Service Account Permissions**:
- `roles/run.admin`: Deploy Cloud Run services
- `roles/run.developer`: Create/execute Cloud Run Jobs
- `roles/artifactregistry.writer`: Push Docker images
- `roles/artifactregistry.reader`: Pull Docker images
- `roles/cloudsql.client`: Connect to Cloud SQL
- `roles/cloudsql.viewer`: View Cloud SQL instances
- `roles/iam.serviceAccountUser`: Use service accounts
- `roles/secretmanager.secretAccessor`: Access secrets
- `roles/storage.admin`: Access Artifact Registry storage

---

## Django Project Structure

### `/adveralabs/` - Django Project Root

| File | Purpose |
|------|---------|
| `settings.py` | Django project settings (database, static files, security) |
| `urls.py` | Main URL routing |
| `wsgi.py` | WSGI configuration for deployment |

**Key Settings**:
- Database: SQLite locally, MySQL (Cloud SQL) in production
- Static files: Collected to `staticfiles/` for production
- Security: HTTPS redirect, secure cookies in production
- Environment-based configuration via `USE_CLOUD_SQL` flag

---

## Key Behaviors & Workflows

### 1. Ad Optimization Workflow

```
User Request → API Endpoint → Optimization Service
    ↓
Fetch Arm States (Facebook + Google)
    ↓
Normalize to ArmState objects
    ↓
Ad Optimization Agent (Pydantic AI)
    ↓
Multi-Armed Bandit Strategy Selection
    ↓
Budget Allocation
    ↓
Apply Changes to Platforms
    ↓
Return Results
```

### 2. Deployment Workflow

```
Code Push to main → GitHub Actions Trigger
    ↓
Authenticate to GCP
    ↓
Build Docker Image
    ↓
Push to Artifact Registry
    ↓
Deploy to Cloud Run
    ↓
Run Database Migrations (Cloud Run Job)
    ↓
Service Available
```

### 3. Local Development Workflow

```bash
# Backend (FastAPI)
cd backend
uvicorn api.main:app --reload

# Frontend (Django)
python manage.py runserver

# Database migrations
python manage.py migrate
```

### 4. Database Configuration

**Local**: SQLite (`db.sqlite3`)
**Production**: MySQL on Cloud SQL
- Instance: `adveralabs-mysql`
- Database: `adveralabs_db`
- User: `adveralabs_user`
- Connection: Via VPC Connector (Unix socket)

**Switch**: Controlled by `USE_CLOUD_SQL` environment variable

---

## Environment Variables

### Backend (FastAPI)
- `OPENAI_API_KEY`: OpenAI API key for Pydantic AI
- `FACEBOOK_ACCESS_TOKEN`: Facebook Ads API token
- `GOOGLE_ADS_CUSTOMER_ID`: Google Ads customer ID
- `DATABASE_URL`: Database connection string

### Django (Website)
- `DJANGO_SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `USE_CLOUD_SQL`: Use Cloud SQL (True/False)
- `DB_HOST`: Database host (Cloud SQL connection name)
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password (from Secret Manager)

---

## Multi-Armed Bandit Strategies

**File**: `backend/services/optimization_strategies.py`

| Strategy | Purpose | Use Case |
|----------|---------|----------|
| `EpsilonGreedy` | Simple exploration/exploitation | General purpose, easy to understand |
| `UCB` (Upper Confidence Bound) | Optimistic exploration | When you want to explore promising arms |
| `ThompsonSampling` | Bayesian approach | When you have prior knowledge |
| `Adaptive` | Contextual bandit | When arms have different contexts |

---

## API Endpoints Summary

### Ad Optimization
- `POST /api/v1/agents/ad-optimization/allocate-budget`
- `POST /api/v1/agents/ad-optimization/cross-channel`
- `POST /api/v1/agents/ad-optimization/run-optimization`
- `GET /api/v1/agents/ad-optimization/fetch-arms`

### ROI Audit
- `POST /api/v1/agents/roi-audit/analyze`

### Other Agents
- Various endpoints for SEO, Content, Social Media, Analytics, Campaign, Client Communication agents

---

## Testing

**Test Files**: `/tests/`
- `test_api.py`: API endpoint tests
- `test_base_agent.py`: Base agent tests

**Run Tests**:
```bash
pytest
```

---

## Key Design Decisions

1. **Dual Framework**: FastAPI for backend API, Django for marketing website
2. **Pydantic AI**: All agents use Pydantic AI for intelligent decision-making
3. **Multi-Armed Bandit**: Core optimization uses bandit algorithms
4. **Cloud-Native**: Designed for Google Cloud Platform deployment
5. **CI/CD**: Automated deployment via GitHub Actions
6. **Database Flexibility**: SQLite for local dev, MySQL for production
7. **Service Account Pattern**: Separate service accounts for different operations

---

## Common Tasks

### Add a New Agent
1. Create file in `backend/agents/`
2. Inherit from `BaseAgent`
3. Define request/response models
4. Add endpoint in `backend/api/routes/agents.py`

### Deploy to Production
1. Push to `main` branch (triggers GitHub Actions)
2. Or manually: `./deploy/quick-deploy.sh`

### Run Migrations
```bash
./deploy/run-migrations.sh
```

### Fix Permissions
```bash
./fix-github-actions-permissions.sh
./verify-github-actions-permissions.sh
```

### View Logs
```bash
# Cloud Run logs
gcloud run services logs read adveralabs-web --region us-central1

# GitHub Actions logs
# View in GitHub Actions tab
```

---

## File Naming Conventions

- **Agents**: `*_agent.py` (e.g., `ad_optimization_agent.py`)
- **Services**: `*_service.py` (e.g., `optimization_service.py`)
- **Integrations**: Platform name (e.g., `facebook_ads.py`)
- **Scripts**: `kebab-case.sh` (e.g., `build-and-deploy.sh`)
- **Templates**: `snake_case.html` (e.g., `blog_post.html`)

---

## Dependencies

**Backend**:
- `fastapi`: Web framework
- `pydantic-ai`: AI agent framework
- `openai`: OpenAI API client
- `sqlalchemy`: Database ORM

**Django**:
- `django`: Web framework
- `gunicorn`: WSGI server
- `mysqlclient`: MySQL database driver

**Deployment**:
- `docker`: Containerization
- `gcloud`: Google Cloud SDK

---

## Security Considerations

1. **Secrets**: Stored in Google Secret Manager, not in code
2. **Service Accounts**: Least-privilege IAM roles
3. **HTTPS**: Enforced in production
4. **Database**: Encrypted connections via Cloud SQL
5. **Environment Variables**: Sensitive data not in env vars

---

## Troubleshooting Guide

### Deployment Issues
- Check service account permissions: `./verify-github-actions-permissions.sh`
- View Cloud Run logs: `gcloud run services logs read adveralabs-web --region us-central1`
- Check Cloud SQL status: `gcloud sql instances describe adveralabs-mysql`

### Database Connection Issues
- Verify `USE_CLOUD_SQL=True` in production
- Check VPC Connector is active
- Verify service account has `roles/cloudsql.client`

### Build Failures
- Check Docker is running
- Verify Artifact Registry access: `gcloud auth configure-docker us-central1-docker.pkg.dev`
- Check build logs in Cloud Build

---

## Next Steps / TODO

1. Complete cross-channel optimization agent with marginal return analysis
2. Implement automation rules engine (budget scaling, creative testing)
3. Add experimentation framework for A/B testing
4. Production API key setup for Facebook/Google Ads
5. Add monitoring and alerting
6. Implement rate limiting and error handling
7. Add comprehensive test coverage

---

## Related Documentation

- `docs/startup-plan.md`: Original business plan
- `docs/TASK_PLAN.md`: Implementation roadmap
- `docs/IMPLEMENTATION_SUMMARY.md`: Feature summary
- `deploy/README.md`: Deployment guide
- `IMPLEMENTATION_NOTES.md`: Implementation notes
- `website/README.md`: Website documentation

---

## Contact & Support

For questions or issues:
1. Check relevant documentation files
2. Review GitHub Actions logs
3. Check Cloud Run logs
4. Review GCP console for resource status

---

*Last Updated: 2025-02-20*
*Maintained by: Advera Labs Team*


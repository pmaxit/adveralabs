# Digital Marketing Agent System

A comprehensive backend system using Pydantic AI for automating digital marketing operations, with a focus on **cross-channel ad optimization** for Facebook and Google Ads.

## Core Concept

This system implements a **cross-channel performance layer** that:
- Feeds platforms higher-quality signals (conversion, value, LTV) than advertisers can today
- Optimizes at the business level (profit, LTV, inventory, margin) instead of per-platform CPA/ROAS
- Automates tedious operations (budget shifts, testing, negative signals) on top of Google/Meta's own automation

Think "smart CDP + bidding brain + experimentation engine" that orchestrates Facebook and Google, not replaces them.

## Features

### Ad Optimization (Core)
- **Ad Optimization Agent**: Cross-channel budget allocation using multi-armed bandit principles
- **Budget Allocation**: Intelligent budget distribution across campaigns and platforms
- **Platform Integration**: Direct integration with Facebook Ads API and Google Ads API
- **Conversion Signal Generation**: Send high-quality conversion signals back to platforms
- **Optimization Loop**: Automated daily optimization cycles

### Marketing Agents
- **SEO Agent**: Keyword research and SEO analysis
- **Content Agent**: Content generation and content calendar management
- **Social Media Agent**: Social media posting, analytics, and hashtag research
- **Analytics Agent**: Marketing performance analysis and report generation
- **Campaign Agent**: Campaign creation, optimization, and A/B testing
- **Client Communication Agent**: Proposal generation, client updates, and onboarding

## Project Structure

```
backend/
├── agents/          # Pydantic AI agents
├── models/          # Database models and schemas
├── api/             # FastAPI application and routes
├── services/        # External service integrations
└── config/          # Configuration management
```

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

3. **Set up database:**
```bash
# Create database migrations
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

4. **Run the application:**
```bash
uvicorn backend.api.main:app --reload
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

See `.env.example` for all required environment variables.

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black backend/
isort backend/
```

## License

MIT

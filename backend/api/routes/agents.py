"""Agent API routes."""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session

from backend.models.database import get_db
from backend.models.schemas import TaskCreate, TaskResponse
from backend.agents.seo_agent import SEOAgent, SEOAnalysisRequest, KeywordResearchRequest
from backend.agents.content_agent import ContentAgent, ContentRequest, ContentCalendarRequest
from backend.agents.social_media_agent import (
    SocialMediaAgent,
    SocialPostRequest,
    SocialAnalyticsRequest,
    HashtagResearchRequest
)
from backend.agents.analytics_agent import AnalyticsAgent, AnalyticsRequest, ReportRequest
from backend.agents.campaign_agent import (
    CampaignAgent,
    CampaignRequest,
    CampaignOptimizationRequest,
    ABTestRequest
)
from backend.agents.client_communication_agent import (
    ClientCommunicationAgent,
    ProposalRequest,
    ClientUpdateRequest,
    MeetingSummaryRequest,
    OnboardingRequest
)
from backend.agents.ad_optimization_agent import (
    AdOptimizationAgent,
    BudgetAllocationRequest,
    CrossChannelOptimizationRequest
)
from backend.agents.roi_audit_agent import (
    ROIAuditAgent,
    ROIAuditRequest
)
from backend.services.optimization_service import OptimizationService

router = APIRouter()

# Initialize agents
seo_agent = SEOAgent()
content_agent = ContentAgent()
social_media_agent = SocialMediaAgent()
analytics_agent = AnalyticsAgent()
campaign_agent = CampaignAgent()
client_communication_agent = ClientCommunicationAgent()
ad_optimization_agent = AdOptimizationAgent()
roi_audit_agent = ROIAuditAgent()
optimization_service = OptimizationService()


# SEO Agent Endpoints
@router.post("/seo/analyze", response_model=Dict[str, Any])
async def analyze_seo(request: SEOAnalysisRequest):
    """Perform SEO analysis."""
    try:
        result = await seo_agent.analyze_seo(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/seo/keyword-research", response_model=Dict[str, Any])
async def research_keywords(request: KeywordResearchRequest):
    """Research keywords."""
    try:
        result = await seo_agent.research_keywords(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Content Agent Endpoints
@router.post("/content/generate", response_model=Dict[str, Any])
async def generate_content(request: ContentRequest):
    """Generate marketing content."""
    try:
        result = await content_agent.generate_content(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/content/calendar", response_model=Dict[str, Any])
async def create_content_calendar(request: ContentCalendarRequest):
    """Create content calendar."""
    try:
        result = await content_agent.create_content_calendar(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Social Media Agent Endpoints
@router.post("/social-media/post", response_model=Dict[str, Any])
async def create_social_post(request: SocialPostRequest):
    """Create a social media post."""
    try:
        result = await social_media_agent.create_post(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/social-media/analytics", response_model=Dict[str, Any])
async def get_social_analytics(request: SocialAnalyticsRequest):
    """Get social media analytics."""
    try:
        result = await social_media_agent.get_analytics(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/social-media/hashtags", response_model=Dict[str, Any])
async def research_hashtags(request: HashtagResearchRequest):
    """Research hashtags."""
    try:
        result = await social_media_agent.research_hashtags(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Analytics Agent Endpoints
@router.post("/analytics/analyze", response_model=Dict[str, Any])
async def analyze_analytics(request: AnalyticsRequest):
    """Analyze marketing performance."""
    try:
        result = await analytics_agent.analyze(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analytics/report", response_model=Dict[str, Any])
async def generate_report(request: ReportRequest):
    """Generate marketing report."""
    try:
        result = await analytics_agent.generate_report(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Campaign Agent Endpoints
@router.post("/campaign/create", response_model=Dict[str, Any])
async def create_campaign(request: CampaignRequest):
    """Create a marketing campaign."""
    try:
        result = await campaign_agent.create_campaign(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/campaign/optimize", response_model=Dict[str, Any])
async def optimize_campaign(request: CampaignOptimizationRequest):
    """Optimize a campaign."""
    try:
        result = await campaign_agent.optimize_campaign(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/campaign/ab-test", response_model=Dict[str, Any])
async def create_ab_test(request: ABTestRequest):
    """Create an A/B test."""
    try:
        result = await campaign_agent.create_ab_test(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Client Communication Agent Endpoints
@router.post("/client/proposal", response_model=Dict[str, Any])
async def generate_proposal(request: ProposalRequest):
    """Generate a client proposal."""
    try:
        result = await client_communication_agent.generate_proposal(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/client/update", response_model=Dict[str, Any])
async def generate_client_update(request: ClientUpdateRequest):
    """Generate a client update."""
    try:
        result = await client_communication_agent.generate_update(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/client/meeting-summary", response_model=Dict[str, Any])
async def generate_meeting_summary(request: MeetingSummaryRequest):
    """Generate a meeting summary."""
    try:
        result = await client_communication_agent.generate_meeting_summary(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/client/onboarding", response_model=Dict[str, Any])
async def create_onboarding(request: OnboardingRequest):
    """Create client onboarding materials."""
    try:
        result = await client_communication_agent.create_onboarding(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Ad Optimization Agent Endpoints
@router.post("/ad-optimization/allocate-budget", response_model=Dict[str, Any])
async def allocate_budget(request: BudgetAllocationRequest):
    """Allocate budget across campaigns/adsets."""
    try:
        result = await ad_optimization_agent.allocate_budget(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ad-optimization/cross-channel", response_model=Dict[str, Any])
async def optimize_cross_channel(request: CrossChannelOptimizationRequest):
    """Optimize budgets across channels."""
    try:
        result = await ad_optimization_agent.optimize_cross_channel(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ad-optimization/run-optimization", response_model=Dict[str, Any])
async def run_optimization(
    account_id: str,
    total_budget: float,
    facebook_account_id: Optional[str] = None,
    google_customer_id: Optional[str] = None,
    time_window: str = "yesterday",
    optimization_goal: str = "roas"
):
    """Run a single optimization cycle (fetch data, allocate budget)."""
    try:
        result = await optimization_service.optimize_once(
            account_id=account_id,
            total_budget=total_budget,
            facebook_account_id=facebook_account_id,
            google_customer_id=google_customer_id,
            time_window=time_window,
            optimization_goal=optimization_goal
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ad-optimization/fetch-arms", response_model=List[Dict[str, Any]])
async def fetch_arms(
    facebook_account_id: Optional[str] = None,
    google_customer_id: Optional[str] = None,
    time_window: str = "yesterday"
):
    """Fetch arm states from platforms."""
    try:
        arms = await optimization_service.fetch_arm_states(
            facebook_account_id=facebook_account_id,
            google_customer_id=google_customer_id,
            time_window=time_window
        )
        return [arm.model_dump() for arm in arms]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ad-optimization/roi-audit", response_model=Dict[str, Any])
async def perform_roi_audit(request: ROIAuditRequest):
    """Perform ROI audit to detect tracking and configuration issues."""
    try:
        result = await roi_audit_agent.audit(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_agent_status():
    """Get status of all agents."""
    return {
        "seo_agent": seo_agent.analysis_agent.get_status(),
        "content_agent": content_agent.generation_agent.get_status(),
        "social_media_agent": social_media_agent.posting_agent.get_status(),
        "analytics_agent": analytics_agent.analysis_agent.get_status(),
        "campaign_agent": campaign_agent.creation_agent.get_status(),
        "client_communication_agent": client_communication_agent.proposal_agent.get_status(),
        "ad_optimization_agent": ad_optimization_agent.budget_agent.get_status()
    }

"""Campaign Management Agent for creating and optimizing marketing campaigns."""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

from backend.agents.base_agent import BaseAgent


class CampaignRequest(BaseModel):
    """Request model for campaign creation."""
    campaign_type: Literal["search", "display", "social", "email", "multi_channel"] = Field(
        ...,
        description="Type of campaign"
    )
    budget: float = Field(..., gt=0, description="Campaign budget")
    target_audience: Dict[str, Any] = Field(..., description="Target audience parameters")
    objectives: List[str] = Field(..., description="Campaign objectives")
    channels: List[str] = Field(..., description="Marketing channels")
    duration_days: Optional[int] = Field(
        default=None,
        description="Campaign duration in days"
    )


class CampaignResponse(BaseModel):
    """Response model for campaign creation."""
    campaign_id: Optional[str] = Field(default=None, description="Generated campaign ID")
    estimated_reach: int = Field(default=0, description="Estimated audience reach")
    cost_per_acquisition: Optional[float] = Field(
        default=None,
        description="Estimated cost per acquisition"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Campaign optimization recommendations"
    )
    budget_allocation: Dict[str, float] = Field(
        default_factory=dict,
        description="Recommended budget allocation across channels"
    )
    expected_metrics: Dict[str, Any] = Field(
        default_factory=dict,
        description="Expected performance metrics"
    )


class CampaignOptimizationRequest(BaseModel):
    """Request model for campaign optimization."""
    campaign_id: str = Field(..., description="Campaign ID to optimize")
    performance_data: Dict[str, Any] = Field(..., description="Current performance data")
    constraints: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optimization constraints"
    )
    optimization_goal: Literal["roi", "conversions", "reach", "engagement"] = Field(
        default="roi",
        description="Optimization goal"
    )


class Optimization(BaseModel):
    """Optimization recommendation model."""
    type: str = Field(..., description="Type of optimization")
    description: str = Field(..., description="Optimization description")
    expected_impact: str = Field(..., description="Expected impact")
    priority: Literal["high", "medium", "low"] = Field(..., description="Priority level")


class CampaignOptimizationResponse(BaseModel):
    """Response model for campaign optimization."""
    optimizations: List[Optimization] = Field(
        default_factory=list,
        description="Optimization recommendations"
    )
    budget_reallocation: Dict[str, float] = Field(
        default_factory=dict,
        description="Recommended budget reallocation"
    )
    bid_adjustments: Dict[str, float] = Field(
        default_factory=dict,
        description="Recommended bid adjustments"
    )
    expected_improvement: Dict[str, Any] = Field(
        default_factory=dict,
        description="Expected performance improvement"
    )


class ABTestRequest(BaseModel):
    """Request model for A/B test creation."""
    campaign_id: str = Field(..., description="Campaign ID")
    test_variants: List[Dict[str, Any]] = Field(..., description="Test variants")
    test_metric: str = Field(..., description="Metric to test")
    duration_days: int = Field(..., description="Test duration")


class ABTestResponse(BaseModel):
    """Response model for A/B test."""
    test_id: Optional[str] = Field(default=None, description="Test ID")
    winning_variant: Optional[str] = Field(default=None, description="Winning variant")
    confidence_level: Optional[float] = Field(default=None, description="Statistical confidence")
    recommendations: List[str] = Field(
        default_factory=list,
        description="Test recommendations"
    )


class CampaignAgent:
    """Campaign management and optimization agent."""
    
    def __init__(self):
        """Initialize campaign agent."""
        self.creation_agent = BaseAgent(
            agent_type="campaign_creation",
            system_prompt="""You are a marketing campaign strategist. Create effective marketing 
            campaigns across multiple channels. Consider budget allocation, target audience, 
            campaign objectives, and expected performance metrics. Provide actionable 
            recommendations for campaign success.""",
            request_type=CampaignRequest,
            response_type=CampaignResponse
        )
        
        self.optimization_agent = BaseAgent(
            agent_type="campaign_optimization",
            system_prompt="""You are a campaign optimization expert. Analyze campaign performance 
            data and provide data-driven optimization recommendations. Focus on improving ROI, 
            conversion rates, and cost efficiency through budget reallocation, bid adjustments, 
            and targeting refinements.""",
            request_type=CampaignOptimizationRequest,
            response_type=CampaignOptimizationResponse
        )
        
        self.abtest_agent = BaseAgent(
            agent_type="ab_testing",
            system_prompt="""You are an A/B testing specialist. Design and analyze A/B tests 
            for marketing campaigns. Provide statistical analysis, identify winning variants, 
            and recommend implementation strategies.""",
            request_type=ABTestRequest,
            response_type=ABTestResponse
        )
    
    async def create_campaign(self, request: CampaignRequest) -> CampaignResponse:
        """Create a marketing campaign."""
        self.creation_agent.initialize()
        return await self.creation_agent.execute(request)
    
    async def optimize_campaign(
        self,
        request: CampaignOptimizationRequest
    ) -> CampaignOptimizationResponse:
        """Optimize a campaign."""
        self.optimization_agent.initialize()
        return await self.optimization_agent.execute(request)
    
    async def create_ab_test(self, request: ABTestRequest) -> ABTestResponse:
        """Create an A/B test."""
        self.abtest_agent.initialize()
        return await self.abtest_agent.execute(request)

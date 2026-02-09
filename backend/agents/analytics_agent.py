"""Analytics Agent for marketing performance analysis and reporting."""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

from backend.agents.base_agent import BaseAgent


class AnalyticsRequest(BaseModel):
    """Request model for analytics data."""
    date_range: Dict[str, str] = Field(
        ...,
        description="Date range (start_date, end_date)"
    )
    metrics: List[str] = Field(..., description="Metrics to retrieve")
    dimensions: Optional[List[str]] = Field(
        default=None,
        description="Dimensions for data segmentation"
    )
    filters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Filters to apply"
    )


class DataPoint(BaseModel):
    """Data point model."""
    date: str
    value: float
    label: Optional[str] = None


class Trend(BaseModel):
    """Trend analysis model."""
    metric: str
    direction: Literal["up", "down", "stable"]
    percentage_change: float
    significance: str


class Insight(BaseModel):
    """Insight model."""
    title: str
    description: str
    impact: Literal["high", "medium", "low"]
    recommendation: Optional[str] = None


class AnalyticsResponse(BaseModel):
    """Response model for analytics data."""
    data_points: List[DataPoint] = Field(
        default_factory=list,
        description="Time series data points"
    )
    trends: List[Trend] = Field(
        default_factory=list,
        description="Trend analysis"
    )
    insights: List[Insight] = Field(
        default_factory=list,
        description="Key insights"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Actionable recommendations"
    )
    summary_stats: Dict[str, float] = Field(
        default_factory=dict,
        description="Summary statistics"
    )


class ReportRequest(BaseModel):
    """Request model for report generation."""
    report_type: Literal["performance", "campaign", "client", "custom"] = Field(
        ...,
        description="Type of report"
    )
    format: Literal["json", "pdf", "html"] = Field(
        default="json",
        description="Report format"
    )
    date_range: Dict[str, str] = Field(..., description="Date range")
    client_id: Optional[int] = Field(default=None, description="Client ID")
    campaign_id: Optional[int] = Field(default=None, description="Campaign ID")
    include_visualizations: bool = Field(default=True, description="Include charts/graphs")


class Visualization(BaseModel):
    """Visualization model."""
    type: str = Field(..., description="Chart type (line, bar, pie, etc.)")
    data: Dict[str, Any] = Field(..., description="Chart data")
    title: str = Field(..., description="Chart title")
    description: Optional[str] = None


class ReportResponse(BaseModel):
    """Response model for report generation."""
    report_data: Dict[str, Any] = Field(..., description="Report data")
    visualizations: List[Visualization] = Field(
        default_factory=list,
        description="Data visualizations"
    )
    key_insights: List[str] = Field(
        default_factory=list,
        description="Key insights summary"
    )
    executive_summary: Optional[str] = Field(
        default=None,
        description="Executive summary"
    )


class AnalyticsAgent:
    """Marketing analytics and reporting agent."""
    
    def __init__(self):
        """Initialize analytics agent."""
        self.analysis_agent = BaseAgent(
            agent_type="analytics_analysis",
            system_prompt="""You are a marketing analytics expert. Analyze marketing performance 
            data, identify trends, detect anomalies, and provide actionable insights. Focus on 
            key metrics like ROI, conversion rates, engagement, and cost efficiency.""",
            request_type=AnalyticsRequest,
            response_type=AnalyticsResponse
        )
        
        self.report_agent = BaseAgent(
            agent_type="report_generation",
            system_prompt="""You are a marketing report specialist. Generate comprehensive 
            marketing reports with clear visualizations, key insights, and executive summaries. 
            Make reports actionable and easy to understand for both technical and non-technical 
            audiences.""",
            request_type=ReportRequest,
            response_type=ReportResponse
        )
    
    async def analyze(self, request: AnalyticsRequest) -> AnalyticsResponse:
        """Analyze marketing performance."""
        self.analysis_agent.initialize()
        return await self.analysis_agent.execute(request)
    
    async def generate_report(self, request: ReportRequest) -> ReportResponse:
        """Generate marketing report."""
        self.report_agent.initialize()
        return await self.report_agent.execute(request)

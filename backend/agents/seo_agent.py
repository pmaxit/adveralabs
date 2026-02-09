"""SEO Agent for keyword research and SEO analysis."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from backend.agents.base_agent import BaseAgent


class SEOAnalysisRequest(BaseModel):
    """Request model for SEO analysis."""
    keyword: str = Field(..., description="Primary keyword to analyze")
    url: str = Field(..., description="URL to analyze")
    competitor_urls: Optional[List[str]] = Field(
        default=None,
        description="Competitor URLs for comparison"
    )


class SEOAnalysisResponse(BaseModel):
    """Response model for SEO analysis."""
    keyword_density: Dict[str, float] = Field(
        default_factory=dict,
        description="Keyword density analysis"
    )
    meta_tags: Dict[str, str] = Field(
        default_factory=dict,
        description="Meta tags analysis (title, description, etc.)"
    )
    backlinks: Optional[int] = Field(
        default=None,
        description="Estimated backlink count"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="SEO optimization recommendations"
    )
    on_page_score: Optional[float] = Field(
        default=None,
        description="On-page SEO score (0-100)"
    )


class KeywordResearchRequest(BaseModel):
    """Request model for keyword research."""
    industry: str = Field(..., description="Industry or niche")
    target_audience: str = Field(..., description="Target audience description")
    location: Optional[str] = Field(
        default=None,
        description="Geographic location for local SEO"
    )
    max_keywords: int = Field(default=20, description="Maximum number of keywords to return")


class KeywordData(BaseModel):
    """Individual keyword data."""
    keyword: str
    search_volume: Optional[int] = None
    difficulty: Optional[float] = Field(default=None, ge=0, le=100)
    cpc: Optional[float] = Field(default=None, description="Cost per click")
    opportunity_score: Optional[float] = Field(default=None, ge=0, le=100)


class KeywordResearchResponse(BaseModel):
    """Response model for keyword research."""
    keywords: List[KeywordData] = Field(
        default_factory=list,
        description="List of researched keywords"
    )
    opportunities: List[str] = Field(
        default_factory=list,
        description="Keyword opportunities and insights"
    )


class SEOAgent:
    """SEO analysis and keyword research agent."""
    
    def __init__(self):
        """Initialize SEO agent."""
        self.analysis_agent = BaseAgent(
            agent_type="seo_analysis",
            system_prompt="""You are an expert SEO analyst. Analyze websites for SEO optimization 
            opportunities. Provide detailed keyword density analysis, meta tag recommendations, 
            backlink insights, and actionable optimization suggestions.""",
            request_type=SEOAnalysisRequest,
            response_type=SEOAnalysisResponse
        )
        
        self.keyword_agent = BaseAgent(
            agent_type="keyword_research",
            system_prompt="""You are an expert keyword researcher. Research and analyze keywords 
            based on industry, target audience, and location. Provide keyword suggestions with 
            search volume estimates, difficulty scores, and opportunity analysis.""",
            request_type=KeywordResearchRequest,
            response_type=KeywordResearchResponse
        )
    
    async def analyze_seo(self, request: SEOAnalysisRequest) -> SEOAnalysisResponse:
        """Perform SEO analysis."""
        self.analysis_agent.initialize()
        return await self.analysis_agent.execute(request)
    
    async def research_keywords(
        self,
        request: KeywordResearchRequest
    ) -> KeywordResearchResponse:
        """Research keywords."""
        self.keyword_agent.initialize()
        return await self.keyword_agent.execute(request)

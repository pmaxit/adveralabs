"""Social Media Agent for managing social media posts and analytics."""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

from backend.agents.base_agent import BaseAgent


class SocialPostRequest(BaseModel):
    """Request model for social media post creation."""
    platform: str = Field(..., description="Social media platform")
    content: str = Field(..., description="Post content")
    media_urls: Optional[List[str]] = Field(
        default=None,
        description="URLs of media files to attach"
    )
    scheduled_time: Optional[str] = Field(
        default=None,
        description="Scheduled posting time (ISO format)"
    )
    hashtags: Optional[List[str]] = Field(
        default=None,
        description="Hashtags to include"
    )


class SocialPostResponse(BaseModel):
    """Response model for social media post."""
    post_id: Optional[str] = Field(default=None, description="Platform post ID")
    engagement_metrics: Dict[str, Any] = Field(
        default_factory=dict,
        description="Estimated engagement metrics"
    )
    best_posting_times: List[str] = Field(
        default_factory=list,
        description="Recommended posting times"
    )
    suggested_hashtags: List[str] = Field(
        default_factory=list,
        description="Suggested hashtags for better reach"
    )


class SocialAnalyticsRequest(BaseModel):
    """Request model for social media analytics."""
    platform: str = Field(..., description="Social media platform")
    date_range: Dict[str, str] = Field(
        ...,
        description="Date range for analytics (start_date, end_date)"
    )
    metrics: List[str] = Field(
        default_factory=list,
        description="Metrics to retrieve"
    )


class SocialAnalyticsResponse(BaseModel):
    """Response model for social media analytics."""
    impressions: int = Field(default=0, description="Total impressions")
    engagement_rate: float = Field(default=0.0, description="Engagement rate percentage")
    reach: int = Field(default=0, description="Total reach")
    demographics: Dict[str, Any] = Field(
        default_factory=dict,
        description="Audience demographics"
    )
    top_posts: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Top performing posts"
    )


class HashtagResearchRequest(BaseModel):
    """Request model for hashtag research."""
    topic: str = Field(..., description="Topic or keyword")
    platform: str = Field(..., description="Social media platform")
    max_hashtags: int = Field(default=10, description="Maximum number of hashtags")


class HashtagData(BaseModel):
    """Hashtag data model."""
    hashtag: str
    popularity_score: Optional[float] = None
    estimated_reach: Optional[int] = None


class HashtagResearchResponse(BaseModel):
    """Response model for hashtag research."""
    hashtags: List[HashtagData] = Field(
        default_factory=list,
        description="Researched hashtags"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Hashtag usage recommendations"
    )


class SocialMediaAgent:
    """Social media management agent."""
    
    def __init__(self):
        """Initialize social media agent."""
        self.posting_agent = BaseAgent(
            agent_type="social_posting",
            system_prompt="""You are a social media expert. Create engaging social media posts 
            optimized for different platforms. Consider platform-specific best practices, 
            optimal posting times, hashtag strategies, and engagement optimization.""",
            request_type=SocialPostRequest,
            response_type=SocialPostResponse
        )
        
        self.analytics_agent = BaseAgent(
            agent_type="social_analytics",
            system_prompt="""You are a social media analytics expert. Analyze social media 
            performance data, identify trends, and provide insights on engagement, reach, 
            demographics, and content performance.""",
            request_type=SocialAnalyticsRequest,
            response_type=SocialAnalyticsResponse
        )
        
        self.hashtag_agent = BaseAgent(
            agent_type="hashtag_research",
            system_prompt="""You are a hashtag research specialist. Research and recommend 
            effective hashtags for social media posts based on topic, platform, and target 
            audience. Consider hashtag popularity, relevance, and engagement potential.""",
            request_type=HashtagResearchRequest,
            response_type=HashtagResearchResponse
        )
    
    async def create_post(self, request: SocialPostRequest) -> SocialPostResponse:
        """Create a social media post."""
        self.posting_agent.initialize()
        return await self.posting_agent.execute(request)
    
    async def get_analytics(
        self,
        request: SocialAnalyticsRequest
    ) -> SocialAnalyticsResponse:
        """Get social media analytics."""
        self.analytics_agent.initialize()
        return await self.analytics_agent.execute(request)
    
    async def research_hashtags(
        self,
        request: HashtagResearchRequest
    ) -> HashtagResearchResponse:
        """Research hashtags."""
        self.hashtag_agent.initialize()
        return await self.hashtag_agent.execute(request)

"""Content Creation Agent for generating marketing content."""
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

from backend.agents.base_agent import BaseAgent


class ContentRequest(BaseModel):
    """Request model for content generation."""
    content_type: Literal["blog", "social", "email", "ad_copy", "landing_page"] = Field(
        ...,
        description="Type of content to generate"
    )
    topic: str = Field(..., description="Topic or subject matter")
    tone: str = Field(
        default="professional",
        description="Tone of voice (professional, casual, friendly, etc.)"
    )
    target_audience: str = Field(..., description="Target audience description")
    length: Optional[str] = Field(
        default=None,
        description="Desired length (e.g., 'short', 'medium', 'long', or word count)"
    )
    key_points: Optional[List[str]] = Field(
        default=None,
        description="Key points to include in the content"
    )


class ContentResponse(BaseModel):
    """Response model for content generation."""
    content: str = Field(..., description="Generated content")
    seo_keywords: List[str] = Field(
        default_factory=list,
        description="SEO keywords used in the content"
    )
    meta_description: Optional[str] = Field(
        default=None,
        description="Meta description for SEO"
    )
    call_to_action: Optional[str] = Field(
        default=None,
        description="Suggested call-to-action"
    )
    word_count: int = Field(default=0, description="Word count of generated content")
    readability_score: Optional[float] = Field(
        default=None,
        description="Readability score"
    )


class ContentBrief(BaseModel):
    """Content brief model."""
    brand_voice: str = Field(..., description="Brand voice description")
    key_messages: List[str] = Field(..., description="Key messages to convey")
    target_keywords: List[str] = Field(default_factory=list, description="Target SEO keywords")
    content_goals: List[str] = Field(..., description="Content goals and objectives")
    target_audience: str = Field(..., description="Target audience description")


class ContentCalendarRequest(BaseModel):
    """Request model for content calendar suggestions."""
    start_date: str = Field(..., description="Start date for calendar")
    end_date: str = Field(..., description="End date for calendar")
    content_types: List[str] = Field(default_factory=list, description="Types of content")
    topics: List[str] = Field(default_factory=list, description="Content topics")
    frequency: str = Field(default="weekly", description="Posting frequency")


class ContentCalendarItem(BaseModel):
    """Content calendar item."""
    date: str
    content_type: str
    topic: str
    suggested_title: str
    platform: Optional[str] = None


class ContentCalendarResponse(BaseModel):
    """Response model for content calendar."""
    calendar_items: List[ContentCalendarItem] = Field(
        default_factory=list,
        description="Suggested content calendar items"
    )


class ContentAgent:
    """Content creation and management agent."""
    
    def __init__(self):
        """Initialize content agent."""
        self.generation_agent = BaseAgent(
            agent_type="content_generation",
            system_prompt="""You are an expert content writer specializing in digital marketing. 
            Create engaging, SEO-optimized content for various formats including blog posts, 
            social media posts, email campaigns, and ad copy. Ensure content is tailored to 
            the target audience and aligns with brand voice.""",
            request_type=ContentRequest,
            response_type=ContentResponse
        )
        
        self.calendar_agent = BaseAgent(
            agent_type="content_calendar",
            system_prompt="""You are a content strategist. Create content calendars that align 
            with marketing goals, audience preferences, and optimal posting schedules. Suggest 
            topics, content types, and timing for maximum engagement.""",
            request_type=ContentCalendarRequest,
            response_type=ContentCalendarResponse
        )
    
    async def generate_content(self, request: ContentRequest) -> ContentResponse:
        """Generate marketing content."""
        self.generation_agent.initialize()
        return await self.generation_agent.execute(request)
    
    async def create_content_calendar(
        self,
        request: ContentCalendarRequest
    ) -> ContentCalendarResponse:
        """Create content calendar."""
        self.calendar_agent.initialize()
        return await self.calendar_agent.execute(request)

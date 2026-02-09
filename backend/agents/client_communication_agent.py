"""Client Communication Agent for proposals, updates, and client management."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from backend.agents.base_agent import BaseAgent


class ProposalRequest(BaseModel):
    """Request model for proposal generation."""
    client_info: Dict[str, Any] = Field(..., description="Client information")
    services: List[str] = Field(..., description="Services to propose")
    budget: Optional[float] = Field(default=None, description="Budget range")
    timeline: str = Field(..., description="Project timeline")
    objectives: List[str] = Field(default_factory=list, description="Project objectives")


class ProposalResponse(BaseModel):
    """Response model for proposal generation."""
    proposal_content: str = Field(..., description="Proposal content")
    pricing: Dict[str, Any] = Field(..., description="Pricing breakdown")
    deliverables: List[str] = Field(..., description="List of deliverables")
    timeline: Dict[str, str] = Field(..., description="Project timeline breakdown")
    next_steps: List[str] = Field(default_factory=list, description="Next steps")


class ClientUpdateRequest(BaseModel):
    """Request model for client update generation."""
    client_id: int = Field(..., description="Client ID")
    update_type: str = Field(
        ...,
        description="Type of update (performance, campaign, general)"
    )
    data: Dict[str, Any] = Field(..., description="Update data")
    include_metrics: bool = Field(default=True, description="Include performance metrics")


class ClientUpdateResponse(BaseModel):
    """Response model for client update."""
    update_content: str = Field(..., description="Update content")
    next_steps: List[str] = Field(..., description="Recommended next steps")
    recommendations: List[str] = Field(
        default_factory=list,
        description="Actionable recommendations"
    )
    key_highlights: List[str] = Field(
        default_factory=list,
        description="Key highlights"
    )


class MeetingSummaryRequest(BaseModel):
    """Request model for meeting summary generation."""
    meeting_notes: str = Field(..., description="Meeting notes")
    attendees: List[str] = Field(default_factory=list, description="Meeting attendees")
    date: str = Field(..., description="Meeting date")
    topics_discussed: List[str] = Field(default_factory=list, description="Topics discussed")


class MeetingSummaryResponse(BaseModel):
    """Response model for meeting summary."""
    summary: str = Field(..., description="Meeting summary")
    action_items: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Action items with owners"
    )
    decisions: List[str] = Field(default_factory=list, description="Decisions made")
    follow_ups: List[str] = Field(default_factory=list, description="Follow-up items")


class OnboardingRequest(BaseModel):
    """Request model for client onboarding."""
    client_info: Dict[str, Any] = Field(..., description="Client information")
    services: List[str] = Field(..., description="Services to onboard")
    preferences: Dict[str, Any] = Field(default_factory=dict, description="Client preferences")


class OnboardingResponse(BaseModel):
    """Response model for client onboarding."""
    welcome_message: str = Field(..., description="Welcome message")
    onboarding_steps: List[Dict[str, Any]] = Field(
        ...,
        description="Onboarding steps with details"
    )
    resources: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Helpful resources"
    )
    timeline: Dict[str, str] = Field(..., description="Onboarding timeline")


class ClientCommunicationAgent:
    """Client communication and management agent."""
    
    def __init__(self):
        """Initialize client communication agent."""
        self.proposal_agent = BaseAgent(
            agent_type="proposal_generation",
            system_prompt="""You are a business proposal expert. Create compelling, professional 
            marketing proposals that clearly communicate value propositions, services, pricing, 
            and timelines. Tailor proposals to client needs and objectives.""",
            request_type=ProposalRequest,
            response_type=ProposalResponse
        )
        
        self.update_agent = BaseAgent(
            agent_type="client_updates",
            system_prompt="""You are a client communication specialist. Create clear, 
            professional client updates that highlight performance, progress, and value. 
            Include actionable insights and next steps.""",
            request_type=ClientUpdateRequest,
            response_type=ClientUpdateResponse
        )
        
        self.meeting_agent = BaseAgent(
            agent_type="meeting_summaries",
            system_prompt="""You are a meeting documentation expert. Create concise, actionable 
            meeting summaries with clear action items, decisions, and follow-ups. Ensure 
            accountability and clarity.""",
            request_type=MeetingSummaryRequest,
            response_type=MeetingSummaryResponse
        )
        
        self.onboarding_agent = BaseAgent(
            agent_type="client_onboarding",
            system_prompt="""You are a client onboarding specialist. Create welcoming, 
            comprehensive onboarding experiences that set clear expectations, provide helpful 
            resources, and establish a strong foundation for client relationships.""",
            request_type=OnboardingRequest,
            response_type=OnboardingResponse
        )
    
    async def generate_proposal(self, request: ProposalRequest) -> ProposalResponse:
        """Generate a client proposal."""
        self.proposal_agent.initialize()
        return await self.proposal_agent.execute(request)
    
    async def generate_update(self, request: ClientUpdateRequest) -> ClientUpdateResponse:
        """Generate a client update."""
        self.update_agent.initialize()
        return await self.update_agent.execute(request)
    
    async def generate_meeting_summary(
        self,
        request: MeetingSummaryRequest
    ) -> MeetingSummaryResponse:
        """Generate a meeting summary."""
        self.meeting_agent.initialize()
        return await self.meeting_agent.execute(request)
    
    async def create_onboarding(self, request: OnboardingRequest) -> OnboardingResponse:
        """Create client onboarding materials."""
        self.onboarding_agent.initialize()
        return await self.onboarding_agent.execute(request)

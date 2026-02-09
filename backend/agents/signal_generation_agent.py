"""Signal Generation Agent for converting business events to high-quality platform signals."""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from backend.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class BusinessEvent(BaseModel):
    """Raw business event from internal systems."""
    event_type: str = Field(..., description="Event type (e.g., 'purchase', 'signup', 'trial_start')")
    event_id: str = Field(..., description="Unique event ID")
    user_id: str = Field(..., description="User identifier")
    timestamp: datetime = Field(..., description="Event timestamp")
    revenue: Optional[float] = Field(default=None, ge=0, description="Revenue amount")
    currency: str = Field(default="USD", description="Currency code")
    product_id: Optional[str] = Field(default=None, description="Product ID (for e-commerce)")
    subscription_id: Optional[str] = Field(default=None, description="Subscription ID (for SaaS)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional event metadata")


class LTVData(BaseModel):
    """Lifetime Value data for a user or cohort."""
    user_id: Optional[str] = Field(default=None, description="User ID")
    predicted_ltv: Optional[float] = Field(default=None, ge=0, description="Predicted LTV")
    historical_ltv: Optional[float] = Field(default=None, ge=0, description="Historical LTV")
    cohort_id: Optional[str] = Field(default=None, description="Cohort identifier")
    confidence_score: Optional[float] = Field(default=None, ge=0, le=1, description="LTV prediction confidence")


class SignalGenerationRequest(BaseModel):
    """Request model for signal generation."""
    events: List[BusinessEvent] = Field(..., description="Business events to convert")
    platform: Literal["facebook", "google", "both"] = Field(..., description="Target platform(s)")
    vertical: Literal["ecommerce", "saas", "leadgen", "other"] = Field(
        default="other",
        description="Business vertical"
    )
    ltv_data: Optional[List[LTVData]] = Field(default=None, description="LTV data for events")
    profit_margins: Optional[Dict[str, float]] = Field(
        default=None,
        description="Product ID to profit margin mapping"
    )
    qualification_rules: Optional[Dict[str, Any]] = Field(
        default=None,
        description="CRM qualification rules for lead classification"
    )


class PlatformSignal(BaseModel):
    """Platform-optimized conversion signal."""
    platform: Literal["facebook", "google"] = Field(..., description="Platform")
    event_name: str = Field(..., description="Platform event name")
    event_id: str = Field(..., description="Unique event ID")
    value: float = Field(..., ge=0, description="Conversion value")
    currency: str = Field(default="USD", description="Currency code")
    timestamp: datetime = Field(..., description="Event timestamp")
    user_data: Dict[str, str] = Field(default_factory=dict, description="User identifiers")
    custom_data: Dict[str, Any] = Field(default_factory=dict, description="Custom event data")
    classification: str = Field(..., description="Event classification (e.g., 'high_value_purchase')")
    reasoning: str = Field(..., description="Reasoning for classification and value")


class SignalGenerationResponse(BaseModel):
    """Response model for signal generation."""
    signals: List[PlatformSignal] = Field(..., description="Generated platform signals")
    issues_detected: List[str] = Field(
        default_factory=list,
        description="Issues detected (tracking, configuration, etc.)"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Recommendations for improvement"
    )
    total_value: float = Field(..., description="Total conversion value across all signals")
    signals_by_platform: Dict[str, int] = Field(
        default_factory=dict,
        description="Count of signals per platform"
    )


class SignalGenerationAgent:
    """Agent for generating high-quality conversion signals for ad platforms."""
    
    def __init__(self):
        """Initialize signal generation agent."""
        self.agent = BaseAgent(
            agent_type="signal_generation",
            system_prompt="""You are a conversion signal optimization agent. Your task is to transform 
            raw business events into high-quality conversion signals for ad platforms (Meta CAPI, 
            Google Enhanced Conversions).

            Responsibilities:
            1. Classify events by business value:
               - "high_value_purchase": Purchase with predicted LTV > threshold or high margin
               - "qualified_lead": Lead that meets CRM qualification rules
               - "purchase": Standard purchase event
               - "trial_start": SaaS trial start
               - "subscription": SaaS subscription conversion
               - "churn_risk_prevented": Reactivation campaign success
            
            2. Calculate appropriate conversion values:
               - For purchases: Use revenue * profit_margin if available, else revenue
               - For high-value purchases: Use predicted LTV or revenue * 1.5
               - For qualified leads: Use estimated lead value or LTV * qualification_rate
               - For SaaS: Use predicted LTV or subscription value
            
            3. Apply vertical-specific best practices:
               - E-commerce: Consider inventory, margins, product categories
               - SaaS: Focus on LTV, payback period, churn risk
               - Lead-gen: Qualification rules, lead scoring
            
            4. Flag potential issues:
               - Missing revenue/value for purchase events
               - Misconfigured event types
               - Broken tracking (missing user identifiers)
               - Low-quality events that shouldn't be sent
            
            5. Map events to platform-specific formats:
               - Meta CAPI: event_name, event_id, value, user_data, custom_data
               - Google Enhanced Conversions: conversion_action, gclid, value, user_data
            
            Your goal is to feed platforms better signals than they receive natively, enabling 
            more effective Smart Bidding and Advantage optimization.

            Provide clear reasoning for each classification and value calculation.""",
            request_type=SignalGenerationRequest,
            response_type=SignalGenerationResponse
        )
    
    async def generate_signals(
        self,
        request: SignalGenerationRequest
    ) -> SignalGenerationResponse:
        """Generate platform-optimized signals from business events."""
        try:
            self.agent.initialize()
            response = await self.agent.execute(request)
            logger.info(f"Generated {len(response.signals)} signals for {request.platform}")
            return response
        except Exception as e:
            logger.error(f"Signal generation failed: {e}")
            # Fallback to rule-based signal generation
            return await self._generate_signals_fallback(request)
    
    async def _generate_signals_fallback(
        self,
        request: SignalGenerationRequest
    ) -> SignalGenerationResponse:
        """Fallback rule-based signal generation."""
        signals = []
        issues = []
        total_value = 0.0
        
        for event in request.events:
            # Basic classification
            if event.event_type == "purchase":
                if event.revenue is None:
                    issues.append(f"Purchase event {event.event_id} missing revenue")
                    continue
                
                # Check if high-value purchase
                is_high_value = False
                value = event.revenue
                
                # Check LTV data
                ltv_data = None
                if request.ltv_data:
                    ltv_data = next(
                        (ltv for ltv in request.ltv_data if ltv.user_id == event.user_id),
                        None
                    )
                    if ltv_data and ltv_data.predicted_ltv and ltv_data.predicted_ltv > value * 1.5:
                        is_high_value = True
                        value = ltv_data.predicted_ltv
                
                # Check profit margins
                if request.profit_margins and event.metadata.get("product_id"):
                    margin = request.profit_margins.get(event.metadata["product_id"], 0.2)
                    value = event.revenue * margin
                
                classification = "high_value_purchase" if is_high_value else "purchase"
                event_name = "Purchase" if not is_high_value else "Purchase"
                
            elif event.event_type == "lead":
                # Check qualification rules
                is_qualified = False
                if request.qualification_rules:
                    # Simple qualification check
                    is_qualified = event.metadata.get("qualified", False)
                
                classification = "qualified_lead" if is_qualified else "lead"
                event_name = "Lead" if not is_qualified else "Lead"
                value = event.revenue or 10.0  # Default lead value
                
            elif event.event_type == "signup" or event.event_type == "trial_start":
                classification = "trial_start"
                event_name = "CompleteRegistration"
                value = event.revenue or 0.0
                
            else:
                classification = event.event_type
                event_name = event.event_type
                value = event.revenue or 0.0
            
            # Generate signals for requested platforms
            platforms = ["facebook", "google"] if request.platform == "both" else [request.platform]
            
            for platform in platforms:
                user_data = {
                    "email": event.metadata.get("email", ""),
                    "phone": event.metadata.get("phone", ""),
                }
                
                signal = PlatformSignal(
                    platform=platform,
                    event_name=event_name,
                    event_id=f"{event.event_id}_{platform}",
                    value=value,
                    currency=event.currency,
                    timestamp=event.timestamp,
                    user_data={k: v for k, v in user_data.items() if v},
                    custom_data=event.metadata,
                    classification=classification,
                    reasoning=f"Classified as {classification} based on event type and business rules"
                )
                signals.append(signal)
                total_value += value
        
        signals_by_platform = {}
        for signal in signals:
            signals_by_platform[signal.platform] = signals_by_platform.get(signal.platform, 0) + 1
        
        return SignalGenerationResponse(
            signals=signals,
            issues_detected=issues,
            recommendations=[
                "Consider implementing LTV prediction for better high-value purchase classification",
                "Set up CRM qualification rules for lead classification",
                "Add profit margin data for accurate value calculation"
            ] if not request.ltv_data or not request.qualification_rules else [],
            total_value=total_value,
            signals_by_platform=signals_by_platform
        )


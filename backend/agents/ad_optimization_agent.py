"""Ad Optimization Agent for cross-channel budget allocation and optimization."""
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime
import logging

from backend.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class ArmState(BaseModel):
    """Arm state representing a campaign/adset with enhanced metrics."""
    platform: Literal["facebook", "google"] = Field(..., description="Platform name")
    id: str = Field(..., description="Campaign or adset ID")
    campaign_id: Optional[str] = Field(default=None, description="Campaign ID")
    campaign_name: Optional[str] = Field(default=None, description="Campaign name")
    spend: float = Field(default=0.0, description="Total spend")
    revenue: float = Field(default=0.0, description="Attributed revenue")
    conversions: int = Field(default=0, description="Number of conversions")
    clicks: int = Field(default=0, description="Number of clicks")
    impressions: int = Field(default=0, description="Number of impressions")
    date: Optional[str] = Field(default=None, description="Date of the data")
    
    # Enhanced fields for business-level optimization
    ltv: Optional[float] = Field(default=None, description="Lifetime Value per customer")
    profit_margin: Optional[float] = Field(default=None, ge=0, le=1, description="Profit margin (0-1)")
    inventory_status: Optional[Literal["in_stock", "low_stock", "out_of_stock"]] = Field(
        default=None, description="Inventory status (for e-commerce)"
    )
    audience_quality_score: Optional[float] = Field(
        default=None, ge=0, le=1, description="Audience quality score (0-1)"
    )
    days_active: Optional[int] = Field(default=None, description="Days since campaign started")
    current_daily_budget: Optional[float] = Field(default=None, description="Current daily budget")
    
    @property
    def roas(self) -> float:
        """Calculate ROAS."""
        return self.revenue / self.spend if self.spend > 0 else 0.0
    
    @property
    def cpa(self) -> float:
        """Calculate CPA."""
        if self.conversions > 0:
            return self.spend / self.conversions
        return float('inf')
    
    @property
    def ctr(self) -> float:
        """Calculate CTR."""
        return (self.clicks / self.impressions * 100) if self.impressions > 0 else 0.0
    
    @property
    def profit(self) -> float:
        """Calculate profit (revenue * margin - spend)."""
        if self.profit_margin is not None:
            return (self.revenue * self.profit_margin) - self.spend
        # Default to 20% margin if not specified
        return (self.revenue * 0.2) - self.spend
    
    @property
    def profit_roas(self) -> float:
        """Calculate profit-based ROAS."""
        profit_val = self.profit
        return profit_val / self.spend if self.spend > 0 else 0.0
    
    @property
    def ltv_roas(self) -> float:
        """Calculate LTV-based ROAS."""
        if self.ltv is not None and self.conversions > 0:
            total_ltv = self.ltv * self.conversions
            return total_ltv / self.spend if self.spend > 0 else 0.0
        return self.roas  # Fallback to regular ROAS
    
    @property
    def has_sufficient_data(self) -> bool:
        """Check if arm has sufficient data for reliable optimization."""
        return self.conversions >= 10 and self.impressions >= 1000


class BudgetAllocationRequest(BaseModel):
    """Request model for budget allocation."""
    arms: List[ArmState] = Field(..., description="List of campaign/adset states")
    total_budget: float = Field(..., gt=0, description="Total budget to allocate")
    min_conversions: int = Field(
        default=10,
        description="Minimum conversions for reliable scoring"
    )
    max_change_ratio: float = Field(
        default=0.3,
        ge=0,
        le=1,
        description="Maximum budget change ratio per update"
    )
    optimization_goal: Literal["roas", "profit", "ltv", "cpa"] = Field(
        default="roas",
        description="Optimization goal"
    )
    strategy: Optional[Literal["epsilon_greedy", "ucb", "thompson_sampling", "adaptive", "intelligent"]] = Field(
        default="intelligent",
        description="Optimization strategy (intelligent uses Pydantic AI, others use bandit algorithms)"
    )


class BudgetAllocation(BaseModel):
    """Budget allocation for an arm."""
    arm_id: str = Field(..., description="Arm ID")
    platform: str = Field(..., description="Platform")
    current_budget: float = Field(..., description="Current budget")
    new_budget: float = Field(..., description="Allocated budget")
    change_percentage: float = Field(..., description="Percentage change")
    score: float = Field(..., description="Score used for allocation")
    reason: str = Field(..., description="Reason for allocation")


class BudgetAllocationResponse(BaseModel):
    """Response model for budget allocation."""
    allocations: List[BudgetAllocation] = Field(
        ...,
        description="Budget allocations per arm"
    )
    total_allocated: float = Field(..., description="Total budget allocated")
    expected_improvement: Dict[str, Any] = Field(
        default_factory=dict,
        description="Expected performance improvement"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Optimization recommendations"
    )


class ConversionSignalRequest(BaseModel):
    """Request model for sending conversion signals to platforms."""
    platform: Literal["facebook", "google"] = Field(..., description="Platform")
    event_name: str = Field(..., description="Event name (e.g., 'high_value_purchase')")
    event_id: str = Field(..., description="Unique event ID")
    value: float = Field(..., ge=0, description="Conversion value")
    currency: str = Field(default="USD", description="Currency code")
    timestamp: Optional[datetime] = Field(default=None, description="Event timestamp")
    user_data: Dict[str, str] = Field(
        default_factory=dict,
        description="User identifiers (email, phone, etc.)"
    )
    custom_data: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Custom event data"
    )


class ConversionSignalResponse(BaseModel):
    """Response model for conversion signal."""
    success: bool = Field(..., description="Whether signal was sent successfully")
    event_id: str = Field(..., description="Event ID")
    platform_response: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Platform API response"
    )
    error_message: Optional[str] = Field(
        default=None,
        description="Error message if failed"
    )


class CrossChannelOptimizationRequest(BaseModel):
    """Request model for cross-channel optimization."""
    account_id: str = Field(..., description="Account ID")
    total_budget: float = Field(..., gt=0, description="Total budget across platforms")
    time_window: str = Field(
        default="yesterday",
        description="Time window for performance data"
    )
    optimization_goal: Literal["roas", "profit", "ltv"] = Field(
        default="roas",
        description="Optimization goal"
    )
    include_recommendations: bool = Field(
        default=True,
        description="Include optimization recommendations"
    )


class CrossChannelOptimizationResponse(BaseModel):
    """Response model for cross-channel optimization."""
    budget_allocations: List[BudgetAllocation] = Field(
        ...,
        description="Budget allocations"
    )
    platform_summary: Dict[str, Dict[str, float]] = Field(
        default_factory=dict,
        description="Summary by platform"
    )
    expected_roas_improvement: Optional[float] = Field(
        default=None,
        description="Expected ROAS improvement percentage"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Optimization recommendations"
    )
    next_optimization_time: Optional[str] = Field(
        default=None,
        description="Recommended next optimization time"
    )


class AdOptimizationAgent:
    """Ad optimization agent for cross-channel budget allocation using Pydantic AI."""
    
    def __init__(self):
        """Initialize ad optimization agent."""
        self.budget_agent = BaseAgent(
            agent_type="budget_allocation",
            system_prompt="""You are an expert ad budget optimization agent. Your task is to allocate 
            budgets across campaigns and ad sets (arms) to maximize business outcomes.

            Key principles:
            1. Balance exploration (trying new opportunities) with exploitation (scaling winners)
            2. Consider statistical confidence - low conversion volume arms need exploration bonus
            3. Optimize for business-level metrics (profit, LTV) not just platform metrics (ROAS)
            4. Respect constraints: max budget change ratio (typically 30%), minimum spend thresholds
            5. Provide clear reasoning for each allocation decision

            When allocating:
            - Give exploration bonus (1.0-2.0x) to arms with < min_conversions conversions
            - Prioritize arms with high profit margins or LTV when optimization_goal is 'profit' or 'ltv'
            - Consider inventory status for e-commerce (reduce budget for out_of_stock items)
            - Account for audience quality scores
            - Ensure no single arm gets more than 50% of total budget unless clearly superior

            Provide specific, actionable recommendations for each allocation.""",
            request_type=BudgetAllocationRequest,
            response_type=BudgetAllocationResponse
        )
        
        self.cross_channel_agent = BaseAgent(
            agent_type="cross_channel_optimization",
            system_prompt="""You are a cross-channel ad optimization expert. Your task is to optimize 
            budgets across Facebook and Google Ads platforms to maximize overall business outcomes.

            Key considerations:
            1. Marginal returns: "If I add $x to Campaign A on Meta vs Campaign B on Google, 
               which yields more profit/ROAS?"
            2. Platform-specific performance patterns (Facebook often better for awareness, 
               Google for bottom-funnel)
            3. Unified business objectives (profit per day, not per-platform ROAS)
            4. Cross-platform budget coordination
            5. Platform-specific constraints and best practices

            Analyze the performance data and provide:
            - Budget allocations across platforms
            - Expected ROAS improvement
            - Specific recommendations for budget shifts
            - Platform-specific bid adjustment suggestions
            - Next optimization timing recommendation""",
            request_type=CrossChannelOptimizationRequest,
            response_type=CrossChannelOptimizationResponse
        )
    
    def score_arm(
        self,
        arm: ArmState,
        min_conversions: int = 10,
        optimization_goal: str = "roas"
    ) -> float:
        """Score an arm for budget allocation (fallback method)."""
        # Exploration bonus for low-data arms
        if arm.conversions < min_conversions:
            exploration_bonus = 1.5 if arm.impressions > 0 else 1.0
            return exploration_bonus
        
        # Score based on optimization goal
        if optimization_goal == "roas":
            base_score = arm.roas
        elif optimization_goal == "profit":
            base_score = arm.profit_roas if arm.profit_margin is not None else arm.roas * 0.8
        elif optimization_goal == "ltv":
            base_score = arm.ltv_roas if arm.ltv is not None else arm.roas * 1.2
        elif optimization_goal == "cpa":
            # Lower CPA is better, so invert
            base_score = 1.0 / arm.cpa if arm.cpa > 0 and arm.cpa != float('inf') else 0.0
        else:
            base_score = arm.roas
        
        # Apply modifiers
        if arm.inventory_status == "out_of_stock":
            base_score *= 0.1  # Heavily penalize out of stock
        elif arm.inventory_status == "low_stock":
            base_score *= 0.7  # Reduce budget for low stock
        
        if arm.audience_quality_score is not None:
            base_score *= (0.5 + arm.audience_quality_score)  # Boost by quality score
        
        return max(base_score, 0.0)
    
    async def allocate_budget(
        self,
        request: BudgetAllocationRequest
    ) -> BudgetAllocationResponse:
        """Allocate budget across arms using intelligent agent or bandit strategy."""
        # Use bandit strategy if specified (not "intelligent")
        if request.strategy and request.strategy != "intelligent":
            from backend.services.optimization_strategies import (
                OptimizationStrategyService,
                OptimizationStrategy
            )
            
            strategy_service = OptimizationStrategyService()
            strategy_map = {
                "epsilon_greedy": OptimizationStrategy.EPSILON_GREEDY,
                "ucb": OptimizationStrategy.UCB,
                "thompson_sampling": OptimizationStrategy.THOMPSON_SAMPLING,
                "adaptive": OptimizationStrategy.ADAPTIVE
            }
            
            strategy = strategy_map.get(request.strategy, OptimizationStrategy.UCB)
            allocations = strategy_service.allocate_with_strategy(
                request.arms,
                request.total_budget,
                strategy,
                request.optimization_goal
            )
            
            # Convert to BudgetAllocationResponse
            budget_allocations = []
            for arm in request.arms:
                new_budget = allocations.get(arm.id, 0.0)
                current_budget = arm.current_daily_budget or arm.spend
                change_pct = ((new_budget - current_budget) / current_budget * 100) if current_budget > 0 else 0.0
                
                budget_allocations.append(
                    BudgetAllocation(
                        arm_id=arm.id,
                        platform=arm.platform,
                        current_budget=current_budget,
                        new_budget=new_budget,
                        change_percentage=change_pct,
                        score=0.0,  # Strategy doesn't provide scores
                        reason=f"Allocated using {request.strategy} strategy"
                    )
                )
            
            return BudgetAllocationResponse(
                allocations=budget_allocations,
                total_allocated=sum(a.new_budget for a in budget_allocations),
                expected_improvement={
                    "method": request.strategy,
                    "estimated_improvement": "5-20%"
                },
                recommendations=[
                    f"Using {request.strategy} strategy for budget allocation",
                    "Monitor performance for 3-5 days before next optimization"
                ]
            )
        
        # Use intelligent Pydantic AI agent
        try:
            self.budget_agent.initialize()
            response = await self.budget_agent.execute(request)
            logger.info(f"Agent allocated budget across {len(request.arms)} arms")
            return response
        except Exception as e:
            logger.warning(f"Agent allocation failed, falling back to rule-based: {e}")
            # Fallback to rule-based allocation
            return await self._allocate_budget_fallback(request)
    
    async def _allocate_budget_fallback(
        self,
        request: BudgetAllocationRequest
    ) -> BudgetAllocationResponse:
        """Fallback rule-based budget allocation."""
        # Calculate scores
        scores = {}
        for arm in request.arms:
            score = self.score_arm(
                arm,
                request.min_conversions,
                request.optimization_goal
            )
            scores[arm.id] = max(score, 0.0)
        
        # Normalize scores and allocate budget
        total_score = sum(scores.values())
        if total_score == 0:
            # Equal allocation if no scores
            budget_per_arm = request.total_budget / len(request.arms)
            allocations = [
                BudgetAllocation(
                    arm_id=arm.id,
                    platform=arm.platform,
                    current_budget=arm.current_daily_budget or arm.spend,
                    new_budget=budget_per_arm,
                    change_percentage=0.0,
                    score=0.0,
                    reason="Equal allocation (no performance data)"
                )
                for arm in request.arms
            ]
        else:
            allocations = []
            for arm in request.arms:
                share = scores[arm.id] / total_score
                new_budget = request.total_budget * share
                current_budget = arm.current_daily_budget or arm.spend
                
                # Apply max change ratio constraint
                max_change = current_budget * request.max_change_ratio
                if abs(new_budget - current_budget) > max_change:
                    if new_budget > current_budget:
                        new_budget = current_budget + max_change
                    else:
                        new_budget = max(0, current_budget - max_change)
                
                change_pct = ((new_budget - current_budget) / current_budget * 100) if current_budget > 0 else 0.0
                
                # Generate reason
                if arm.conversions < request.min_conversions:
                    reason = f"Exploration allocation ({share*100:.1f}%) - low conversion volume"
                elif request.optimization_goal == "profit" and arm.profit_margin:
                    reason = f"Profit-optimized allocation ({share*100:.1f}%) - profit ROAS: {arm.profit_roas:.2f}"
                elif request.optimization_goal == "ltv" and arm.ltv:
                    reason = f"LTV-optimized allocation ({share*100:.1f}%) - LTV ROAS: {arm.ltv_roas:.2f}"
                else:
                    reason = f"ROAS-based allocation ({share*100:.1f}%) - ROAS: {arm.roas:.2f}"
                
                allocations.append(
                    BudgetAllocation(
                        arm_id=arm.id,
                        platform=arm.platform,
                        current_budget=current_budget,
                        new_budget=new_budget,
                        change_percentage=change_pct,
                        score=scores[arm.id],
                        reason=reason
                    )
                )
        
        return BudgetAllocationResponse(
            allocations=allocations,
            total_allocated=sum(a.new_budget for a in allocations),
            expected_improvement={
                "estimated_roas_improvement": "5-15%",
                "confidence": "medium",
                "method": "rule_based_fallback"
            },
            recommendations=[
                "Monitor performance for 3-5 days before next optimization",
                "Consider pausing arms with consistently low scores",
                "Increase budget for top performers gradually",
                "Review inventory status for e-commerce campaigns"
            ]
        )
    
    async def optimize_cross_channel(
        self,
        request: CrossChannelOptimizationRequest
    ) -> CrossChannelOptimizationResponse:
        """Optimize budgets across channels using intelligent agent."""
        try:
            self.cross_channel_agent.initialize()
            response = await self.cross_channel_agent.execute(request)
            logger.info(f"Cross-channel optimization completed for account {request.account_id}")
            return response
        except Exception as e:
            logger.error(f"Cross-channel optimization failed: {e}")
            raise

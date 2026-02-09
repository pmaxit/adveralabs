"""Optimization service for fetching data and running optimization loops."""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging

from backend.agents.ad_optimization_agent import ArmState, AdOptimizationAgent
from backend.services.integrations.facebook_ads import FacebookAdsIntegration
from backend.services.integrations.google_ads import GoogleAdsIntegration

logger = logging.getLogger(__name__)


class OptimizationService:
    """Service for running optimization loops and fetching platform data."""
    
    def __init__(self):
        """Initialize optimization service."""
        self.facebook_ads = FacebookAdsIntegration()
        self.google_ads = GoogleAdsIntegration()
        self.optimization_agent = AdOptimizationAgent()
    
    async def fetch_arm_states(
        self,
        facebook_account_id: Optional[str] = None,
        google_customer_id: Optional[str] = None,
        time_window: str = "yesterday",
        level: str = "campaign"
    ) -> List[ArmState]:
        """Fetch arm states from Facebook and Google platforms.
        
        Based on PDF pseudo code: fetch_arm_states(time_window)
        Returns normalized ArmState objects from both platforms.
        """
        arms = []
        
        # Fetch Facebook data
        if facebook_account_id:
            try:
                date_range = self._parse_time_window(time_window)
                fb_insights = await self.facebook_ads.get_insights(
                    account_id=facebook_account_id,
                    date_preset=time_window if time_window in ["yesterday", "last_7d", "last_30d"] else None,
                    level=level,
                    time_increment=1
                )
                
                for insight in fb_insights:
                    # Extract conversions from actions
                    conversions = 0
                    revenue = 0.0
                    actions = insight.get("actions", [])
                    action_values = insight.get("action_values", [])
                    
                    for action in actions:
                        if action.get("action_type") in ["purchase", "lead", "complete_registration"]:
                            conversions += int(action.get("value", 0))
                    
                    for av in action_values:
                        if av.get("action_type") in ["purchase"]:
                            revenue += float(av.get("value", 0))
                    
                    arm = ArmState(
                        platform="facebook",
                        id=insight.get("campaign_id", ""),
                        campaign_id=insight.get("campaign_id"),
                        campaign_name=insight.get("campaign_name", ""),
                        spend=float(insight.get("spend", 0)),
                        revenue=revenue,
                        conversions=conversions,
                        clicks=int(insight.get("clicks", 0)),
                        impressions=int(insight.get("impressions", 0)),
                        date=insight.get("date_start")
                    )
                    arms.append(arm)
            except Exception as e:
                logger.error(f"Error fetching Facebook data: {e}")
        
        # Fetch Google Ads data
        if google_customer_id:
            try:
                date_range = self._parse_time_window(time_window)
                google_insights = await self.google_ads.get_campaign_insights(
                    customer_id=google_customer_id,
                    date_range=date_range
                )
                
                for insight in google_insights:
                    metrics = insight.get("metrics", {})
                    campaign = insight.get("campaign", {})
                    
                    arm = ArmState(
                        platform="google",
                        id=str(campaign.get("id", "")),
                        campaign_id=str(campaign.get("id", "")),
                        campaign_name=campaign.get("name", ""),
                        spend=metrics.get("cost_micros", 0) / 1_000_000,  # Convert micros
                        revenue=metrics.get("conversion_value", 0.0),
                        conversions=int(metrics.get("conversions", 0)),
                        clicks=int(metrics.get("clicks", 0)),
                        impressions=int(metrics.get("impressions", 0)),
                        date=insight.get("segments", {}).get("date")
                    )
                    arms.append(arm)
            except Exception as e:
                logger.error(f"Error fetching Google Ads data: {e}")
        
        return arms
    
    def _parse_time_window(self, time_window: str) -> Dict[str, str]:
        """Parse time window string to date range."""
        today = datetime.now()
        
        if time_window == "yesterday":
            yesterday = today - timedelta(days=1)
            return {
                "start_date": yesterday.strftime("%Y-%m-%d"),
                "end_date": yesterday.strftime("%Y-%m-%d")
            }
        elif time_window == "last_7d":
            start = today - timedelta(days=7)
            return {
                "start_date": start.strftime("%Y-%m-%d"),
                "end_date": today.strftime("%Y-%m-%d")
            }
        elif time_window == "last_30d":
            start = today - timedelta(days=30)
            return {
                "start_date": start.strftime("%Y-%m-%d"),
                "end_date": today.strftime("%Y-%m-%d")
            }
        else:
            # Default to yesterday
            yesterday = today - timedelta(days=1)
            return {
                "start_date": yesterday.strftime("%Y-%m-%d"),
                "end_date": yesterday.strftime("%Y-%m-%d")
            }
    
    async def optimize_once(
        self,
        account_id: str,
        total_budget: float,
        facebook_account_id: Optional[str] = None,
        google_customer_id: Optional[str] = None,
        time_window: str = "yesterday",
        optimization_goal: str = "roas",
        min_conversions: int = 10,
        max_change_ratio: float = 0.3
    ) -> Dict[str, Any]:
        """Run one optimization cycle.
        
        Based on PDF pseudo code: optimize_once(account_id, total_budget)
        This is the main optimization loop that:
        1. Fetches arm states
        2. Allocates budget
        3. Applies budget changes (would need to be implemented)
        """
        # Fetch arm states
        arms = await self.fetch_arm_states(
            facebook_account_id=facebook_account_id,
            google_customer_id=google_customer_id,
            time_window=time_window
        )
        
        if not arms:
            return {
                "status": "no_data",
                "message": "No campaign data available for optimization"
            }
        
        # Allocate budget using intelligent agent
        from backend.agents.ad_optimization_agent import BudgetAllocationRequest
        
        allocation_request = BudgetAllocationRequest(
            arms=arms,
            total_budget=total_budget,
            min_conversions=min_conversions,
            max_change_ratio=max_change_ratio,
            optimization_goal=optimization_goal
        )
        
        allocation_result = await self.optimization_agent.allocate_budget(
            allocation_request
        )
        
        # In production, apply budget changes here:
        # await self.apply_budget_changes(allocation_result.allocations)
        
        return {
            "status": "success",
            "arms_processed": len(arms),
            "allocations": allocation_result.model_dump(),
            "timestamp": datetime.now().isoformat()
        }
    
    async def apply_budget_changes(
        self,
        allocations: List[Any],
        max_change_ratio: float = 0.3
    ) -> Dict[str, Any]:
        """Apply budget changes to platforms.
        
        Based on PDF pseudo code: apply_budget_changes(arms, new_budgets)
        This would update budgets via platform APIs.
        """
        results = []
        
        for allocation in allocations:
            try:
                if allocation.platform == "facebook":
                    # Update Facebook adset budget
                    await self.facebook_ads.update_adset_budget(
                        adset_id=allocation.arm_id,
                        daily_budget=allocation.new_budget
                    )
                    results.append({
                        "arm_id": allocation.arm_id,
                        "platform": "facebook",
                        "status": "success",
                        "new_budget": allocation.new_budget
                    })
                elif allocation.platform == "google":
                    # Update Google campaign budget
                    # Note: Would need budget_id mapping
                    logger.warning(f"Google budget update requires budget_id mapping for {allocation.arm_id}")
                    results.append({
                        "arm_id": allocation.arm_id,
                        "platform": "google",
                        "status": "pending",
                        "message": "Requires budget_id mapping"
                    })
            except Exception as e:
                logger.error(f"Error updating budget for {allocation.arm_id}: {e}")
                results.append({
                    "arm_id": allocation.arm_id,
                    "platform": allocation.platform,
                    "status": "error",
                    "error": str(e)
                })
        
        return {
            "updated": len([r for r in results if r.get("status") == "success"]),
            "failed": len([r for r in results if r.get("status") == "error"]),
            "results": results
        }
